from __future__ import print_function

import re
import csv
import sys
import argparse
import collections

import requests
import lxml.html


Record = collections.namedtuple('Record',
                                'date exercise string weight_lbs reps pr notes'
                               )


class FitocracyError(Exception):
    pass


class FitocracyClient(object):
    LOGIN_URL = 'https://www.fitocracy.com/accounts/login/'
    PERF_URL = 'https://www.fitocracy.com/profile/jpt/?performance'

    def __init__(self):
        self.session = requests.Session()

    def login(self, username, password):
        doc = lxml.html.fromstring(self.session.get(self.LOGIN_URL).content)
        token = doc.xpath('//input[@name="csrfmiddlewaretoken"]/@value')[0]
        resp = self.session.post(self.LOGIN_URL,
                                 {'username': username,
                                  'password': password,
                                  'csrfmiddlewaretoken': token},
                                 headers={'Referer': self.LOGIN_URL})
        if resp.status_code != 200:
            raise FitocracyError('{0} status code from fitocracy'.format(
                resp.status_code))
        user_id = re.findall("user_id = \"(\d+)\"", resp.content)
        if user_id:
            self.user_id = user_id[0]
            return True
        else:
            raise FitocracyError('login failed')

    def get_user_activities(self):
        """ returns list of count, id, name dicts """
        url = 'https://www.fitocracy.com/get_user_activities/{0}/'.format(
            self.user_id)
        return self.session.get(url).json()

    def get_activity_details(self, act_id):
        url = 'https://www.fitocracy.com/_get_activity_history_json/?activity-id={0}'.format(
            act_id)
        resp = self.session.get(url).json()
        # list of items
        #   id
        #   date
        #   actions
        #       action (effort{0-5}[_label], name)
        #       actiondate, actiontime
        #       effort{0-5}[_imperial,_metric][_string,_unit]
        #       is_pr
        #       notes
        #       string[_imperial,_metric]
        #       subgroup, subgroup_order, submitted, user
        records = []
        for item in resp:
            date = item['date']
            for action in item['actions']:
                records.append(Record(date,
                                      action['action']['name'],
                                      action['string'],
                                      action['effort0_imperial'],
                                      action['effort1_imperial'],
                                      action['is_pr'], action['notes']))
        return records


def get_activities(fc, ids, csv_output):
    fields = ('date', 'string', 'weight_lbs', 'reps', 'is_pr', 'notes')
    outfile = csv.writer(sys.stdout)
    if csv_output:
        outfile.writerow(fields)
    for id in ids:
        for detail in fc.get_activity_details(id):
            if csv_output:
                outfile.writerow(detail)
            else:
                print(*detail)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('username', help='fitocracy username')
    parser.add_argument('password', help='fitocracy password')
    parser.add_argument('id', help='fitocracy activity id', nargs='?')
    parser.add_argument('--csv', action='store_true',
                        help='generate CSV of data')
    parser.add_argument('--all', action='store_true', help='all activities')
    args = parser.parse_args()

    fc = FitocracyClient()
    fc.login(args.username, args.password)

    if args.all:
        all_ids = [act['id'] for act in fc.get_user_activities()]
        get_activities(fc, all_ids, args.csv)

    elif not args.id:
        _fmt_string = '{:<40} {:>10} {:>10}'
        activities = sorted(fc.get_user_activities(),
                            key=lambda i: -i['count'])
        print(_fmt_string.format('name', 'id', 'count'))
        for activity in activities:
            print(_fmt_string.format(activity['name'],
                                     activity['id'],
                                     activity['count']))
    else:
        get_activities(fc, [args.id], args.csv)

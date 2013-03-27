"""
    Code to scrape message listing from google groups

    Currently useful for analytics on group behavior, could be modified
    to export group (seeing as Google still doesn't provide a way to do
    so)

    Requires python 2.6
    scrapelib & lxml for archive scraping
    feedparser for latest activity scraping
"""

from collections import namedtuple
import datetime
import csv
import re

import scrapelib
import lxml.html
import feedparser

BASE_URL = 'http://groups.google.com/'
Thread = namedtuple("Thread", "title link author date num_messages")
Message = namedtuple("Message", "title thread_link order author date")

scraper = scrapelib.Scraper(requests_per_minute=4, cache_dir='/tmp/')

def _clean_date(string):
    """
    Handles 3 formats:
        * 10:06am
        * Mmm dd
        * Mmm dd yyyy
    """

    if re.match("\d{1,2}\:\d{2}[ap]m", string):
        date = datetime.date.today()
    elif re.match("[A-Z][a-z]{2} \d{1,2}$", string):
        parsed = datetime.datetime.strptime(string, "%b %d")
        date = parsed.replace(year=2010).date()
    elif re.match("[A-Z][a-z]{2} \d{1,2} \d{4}", string):
        parsed = datetime.datetime.strptime(string, "%b %d %Y")
        date = parsed.date()
    else:
        raise ValueError("could not parse date " + string)
    return date

def _str(element):
    return element.text_content().encode('utf-8').strip()


def scrape_archive(group):
    # gvc=2 forces topic list mode and tsc=2 forces sort by first message
    url = 'http://groups.google.com/group/{0}/topics?start={1}&sa=N&gvc=2&tsc=2'
    start = 0
    while 1:
        data = scraper.urlopen(url.format(group, start))
        doc = lxml.html.fromstring(data)
        for row in doc.xpath("//div[@class='maincontoutboxatt']/table/tr"):
            tds = row.xpath('td')

            title = _str(tds[1])

            if title and title != 'Topic':
                # last two characters are weird unicode cruft
                title = title[:-2]
                link = BASE_URL + tds[1].xpath('a')[0].get('href')

                # in format: N new of N
                num_messages = _str(tds[3]).rsplit(' ', 1)[-1]

                # note: can also get # of authors via text_content, perhaps add this?
                author = tds[4].text.encode('utf-8')

                # strip newline
                date = _clean_date(_str(tds[5]))
                yield Thread(title, link, author, date, num_messages)

        start += 30
        if not any([x.text.startswith('Older') for x in doc.xpath("//a[@class='uitl']")]):
            break

def scrape_archive_thread(url):
    n = 0
    while 1:
        data = scraper.urlopen(url)
        doc = lxml.html.fromstring(data)
        for header in doc.xpath('//table[@class="h msg_meta"]'):
            spans = header.cssselect('span.fontsize2')
            if spans:
                author = _str(spans[0])
                date = _str(spans[-1])
                yield n, author, date
                n += 1

        newer_links = doc.xpath('//a[text()="Newer >"]')
        if newer_links:
            url = BASE_URL + newer_links[0].get('href')
        else:
            break
    print url, n

def scrape_archive_to_csv(group):
    threads = csv.writer(open(group + '_threads.csv', 'w'))
    messages = csv.writer(open(group + '_messages.csv', 'w'))

    for t in scrape_archive(group):
        threads.writerow(t)
        if int(t.num_messages) > 1:
            for n, author, date in scrape_archive_thread(t.link):
                messages.writerow((t.title, t.link, n, author, date))
        else:
            messages.writerow((t.title, t.link, 0, t.author, t.date))

# once we have an archive we can stay up to date via RSS
def scrape_rss(group):
    url = 'http://groups.google.com/group/{0}/feed/atom_v1_0_msgs.xml?num=500'.format(group)
    for entry in feedparser.parse(url).entries:
        yield Message(entry.title, entry.link, entry.author, entry.updated)

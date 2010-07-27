#!/usr/bin/env python

import getpass
import hashlib
import json
import os
import urllib, urllib2

import argparse
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers

class DotstoreException(Exception):
    pass

def _configfile():
    return os.path.expanduser('~/.dotstore')

def _read_token():
    return json.loads(open(_configfile()).read())['token']

def _write_token(token):
    config = {'token':token}
    open(_configfile(), 'w').write(json.dumps(config, indent=2))

def _get_email_and_password(args):
    if not args.email:
        email = raw_input('Email: ')
    else:
        email = args.email
    password = getpass.getpass('Password: ')
    return {'email': email, 'password': password}

def _apicall(http_method, api_method, params=None, headers=None, token=None):
    if api_method.startswith('http://'):
        url = api_method
    else:
        url = 'http://127.0.0.1:8080/api/%s' % api_method
    if not params:
        params = {}
    if not headers:
        headers = {}
    if token:
        headers['x-dotstore-token'] = token

    try:
        if http_method == 'GET':
            url += '?' + urllib.urlencode(params)
            request = urllib2.Request(url, headers=headers)
        else:
            if isinstance(params, dict):
                params = urllib.urlencode(params)
            request = urllib2.Request(url, params, headers=headers)
        return urllib2.urlopen(request).read()
    except urllib2.HTTPError as e:
        raise DotstoreException(e.read())


def _get_list(token, symbol=False):
    resp = _apicall('GET', 'file_list', token=token)
    resp = json.loads(resp)

    if symbol:
        for info in resp:
            fname = os.path.expanduser(info['path'])
            if _sha1sum(fname) != info['hash']:
                if os.path.getmtime(fname) > info['mtime']:
                    symbol = '*'
                else:
                    symbol = '^'
            else:
                symbol = ' '
            info['symbol'] = symbol

    return resp

def _sha1sum(filename):
    return hashlib.sha1(open(filename).read()).hexdigest()

def register(args):
    params = _get_email_and_password(args)
    resp = _apicall('POST', 'register', params)
    _write_token(json.loads(resp)['token'])

def login(args):
    params = _get_email_and_password(args)
    resp = _apicall('GET', 'get_token', params)
    _write_token(json.loads(resp)['token'])

def _standardize_path(f):
    abspath = os.path.abspath(f)
    return abspath, abspath.replace(os.path.expanduser('~'), '~')

def _upload(abspath, canonpath, token):
    upload_url = _apicall('GET', 'get_upload_url', token=token)
    register_openers()
    body, headers = multipart_encode({'file': open(abspath),
                                      'path': canonpath,
                                      'mtime': os.path.getmtime(abspath)})
    _apicall('POST', upload_url, body, headers=headers, token=token)

def add(args):
    token = _read_token()
    remote_files = _get_list(token)

    for f in args.filename:
        abspath, canonpath = _standardize_path(f)

        if canonpath in [rf['path'] for rf in remote_files]:
            raise DotstoreException('file %s already tracked' % canonpath)

        if not os.path.exists(abspath):
            raise DotstoreException('no such file: %s' % canonpath)

        _upload(abspath, canonpath, token)
        print 'now tracking', canonpath

def status(args):
    token = _read_token()
    remote_files = _get_list(token, symbol=True)

    for finfo in remote_files:
        print ' %s  %s' % (finfo['symbol'], finfo['path'])

def sync(args):
    token = _read_token()
    remote_files = _get_list(token, symbol=True)

    for finfo in remote_files:
        if finfo['symbol'] == '*':
            print 'local changes to', finfo['path']
            print 'UPLOAD'
        elif finfo['symbol'] == '^':
            print 'remote changes to', finfo['path']
            print 'DOWNLOAD'

def main():
    parser = argparse.ArgumentParser(
        prog='dotstore.py',
        description="command line tool for tracking dotfiles")
    subparsers = parser.add_subparsers(help='subcommand help')

    register_parser = subparsers.add_parser('register', help='authenticate to dotstore')
    register_parser.set_defaults(func=register)
    register_parser.add_argument('-e', '--email', help='email')

    login_parser = subparsers.add_parser('login', help='authenticate to dotstore')
    login_parser.set_defaults(func=login)
    login_parser.add_argument('-e', '--email', help='email')

    add_parser = subparsers.add_parser('add', help='add a file to dotstore')
    add_parser.set_defaults(func=add)
    add_parser.add_argument('filename', help='filename to add', nargs='+')

    sync_parser = subparsers.add_parser('sync', help='sync files')
    sync_parser.set_defaults(func=sync)
    sync_parser.add_argument('filename', help='filename to sync', nargs='*')

    status_parser = subparsers.add_parser('status', help='get status')
    status_parser.set_defaults(func=status)
    status_parser.add_argument('filename', help='filename to get status on',
                               nargs='*')

    args = parser.parse_args()
    try:
        args.func(args)
    except DotstoreException as de:
        print 'Error:', de

if __name__ == '__main__':
    main()

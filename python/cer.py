#!/usr/bin/env python3
import os
import glob
import inspect
import argparse
from subprocess import check_output

# Config #############

CODE_DIR = '/home/james/code'
CONFIG_DIR = '/home/james/Dropbox/config'

REPOS = {
    'libs/jellyfish': 'git@github.com:sunlightlabs/jellyfish.git',
    'libs/scrapelib': 'git@github.com:sunlightlabs/scrapelib.git',
    'libs/django-markupfield': 'git@github.com:jamesturk/django-markupfield.git',
    'libs/validictory': 'git@github.com:jamesturk/django-markupfield.git',
    'go/src/github.com/jamesturk/go-jellyfish': 'git@github.com:jamesturk/go-jellyfish.git',
    #'openstates/openstates': 'git@github.com:sunlightlabs/openstates.git',
    #'openstates/openstates.org': 'git@github.com:sunlightlabs/openstates.org.git',
    #'openstates/billy': 'git@github.com:sunlightlabs/billy.git',
    #'ocd/imago': 'git@github.com:opencivicdata/imago.git',
    #'ocd/api': 'git@github.com:opencivicdata/api.opencivicdata.org.git',
    #'ocd/docs': 'git@github.com:opencivicdata/docs.opencivicdata.org.git',
    #'ocd/pupa': 'git@github.com:opencivicdata/pupa.git',
    #'ocd/ocd-division-ids': 'git@github.com:opencivicdata/ocd-division-ids.git',
    #'ocd/scrapers-us-municipal': 'git@github.com:opencivicdata/scrapers-us-municipal.git',
}

# command line helper #############

class Commands(object):
    def __init__(self):
        self.functions = {}
        self.parser = argparse.ArgumentParser()
        self.subparsers = self.parser.add_subparsers()

    def register(self, func):
        name = func.__name__
        sub = self.subparsers.add_parser(name)
        sub.set_defaults(func=func)
        for arg in inspect.getargspec(func).args:
            sub.add_argument(arg)

    def main(self):
        args = self.parser.parse_args()
        args.func()

commands = Commands()

# utilities ###############

def _clone(repo, dir):
    if os.path.exists(dir):
        print(dir, 'exists, skipping')
    else:
        check_output(['git', 'clone', repo, dir])


def _get_git_remote(gitdir):
    cwd = os.getcwd()
    os.chdir(gitdir)
    results = check_output(['git', 'remote', '-v'])
    pieces = results.split()
    check_next = False
    for piece in pieces:
        if piece == 'origin':
            check_next = True
        elif check_next:
            os.chdir(cwd)
            return piece
    os.chdir(cwd)


def _get_local_repos(dirname, prefix=''):
    repos = {}
    for dir in os.listdir(dirname):
        if prefix:
            dir = os.path.join(prefix, dir)
        if os.path.isdir(dir):
            if os.path.exists(dir + '/.git'):
                remote = _get_git_remote(dir)
                repos[dir] = remote
            else:
                repos.update(_get_local_repos(dir, prefix=dir))
    return repos


def _link(dir, dfdir):
    for df in glob.glob(dfdir):
        if df.endswith(('.git', '.config')):
            continue
        goodpath = os.path.join(dir, os.path.basename(df))
        if os.path.exists(goodpath):
            if os.path.samefile(df, goodpath):
                pass
            else:
                print('files differ {0} {1}'.format(df, goodpath))
        else:
            print('linking {0} to {1}'.format(df, goodpath))
            os.symlink(df, goodpath)

# commands ########

@commands.register
def checkout():
    localrepos = _get_local_repos(CODE_DIR)

    for dir, repo in REPOS.items():
        dir = os.path.join(CODE_DIR, dir)
        if dir not in localrepos:
            print('creating', dir)
            _clone(repo, dir)
        elif repo != localrepos[dir]:
            print('warning: {} exists but points to {} instead of {}'.format(
                dir, localrepos[dir], repo))
        else:
            print(dir, 'exists')

    for dir, repo in localrepos.items():
        if dir not in REPOS:
            print('warning: unmonitored checkout of {} -> {}'.format(dir, repo))


@commands.register
def syncdots():
    _link(os.path.expanduser('~/'),
          os.path.abspath(os.path.join(CONFIG_DIR, 'dotfiles/.*')))
    _link(os.path.expanduser('~/.config/'),
          os.path.abspath(os.path.join(CONFIG_DIR, 'dotfiles/.config/*')))


if __name__ == '__main__':
    commands.main()

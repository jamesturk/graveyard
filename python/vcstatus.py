#!/usr/bin/env python

import os

cmds = {'.svn': 'svn status',
 '.git': 'git ls-files --exclude-per-directory=.gitignore -X .git/info/exclude -X ~/.gitignore -d -m -o -t',
 '.bzr': 'bzr status -S'}

dirs = os.listdir('.')
for d in dirs:
    os.chdir(d)
    for vcdir,cmd in cmds.iteritems():
        if os.path.exists(vcdir):
            status = ['   '+line[:-1] for line in os.popen4(cmd)[1].readlines()]
            if status:
                print d,vcdir
                for sl in status:
                    print sl
            break
    else:
        print 'NO VC: ', d
    os.chdir('..')

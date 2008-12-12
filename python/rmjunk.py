#!/usr/bin/env python

import os
import re

junk_re = re.compile('^.+(\.pyc|\~)$')

print 'Removing junk files...'

for root,dirs,files in os.walk('.'):
    for file in files:
        if junk_re.match(file):
            f = os.path.join(root,file)
            print '  ',f
            os.remove(f)


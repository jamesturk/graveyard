#!/usr/bin/env python

import os

GAIM_LOG_DIR = '/home/james/.gaim/logs/aim'

def do_user(mySn, userSn):
    path = os.path.join(GAIM_LOG_DIR,mySn,userSn)
    dateSize = dict()
    logs = os.listdir(path)
    
    for log in logs:
        date = log[0:10]
        size = os.stat(os.path.join(path,log)).st_size
        
        if date in dateSize:
            dateSize[date] += size
        else: 
            dateSize[date] = size
    
    return dateSize
    
def do_users(pairs):
    userDict = dict()
    for mySn,user in pairs:
        userDict[user] = do_user(mySn, user)
    return userDict
    
def generate_csv(userDict):
    alldates = []
    for user in userDict:
        for date in userDict[user]:
            alldates.append(date)

    csv = 'Date,'
    for user in userDict:
        csv += user + ','
    csv += '\n'
    
    for date in sorted(set(alldates)):
        csv += date + ','
        for user in userDict:
            if date in userDict[user]:
                csv += str(userDict[user][date])
            else:
                csv += '0'
            csv += ','
        csv += '\n'
    return csv
    
print generate_csv(do_users([('jamespturk','oname'), ('jpt2433','oname')]))

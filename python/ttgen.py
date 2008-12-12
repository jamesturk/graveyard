#!/usr/bin/env python
import sys


def numToInputs(num,pad):
    b = []
    while num > 0:
        b.append(num & 1) 
        num >>= 1
        pad -= 1
    for i in range(pad):
        b.append(0)
    b.reverse()
    return b

def printTable(equ):
    chars = [chr(c) for c in range(ord('A'),ord('Z')+1)]    # generate a list of the capital chars A-Z
    var = [0 for i in range(26)]                            # define an 26 element array for variables
    
    equ = '(' + equ.upper() + ')'                       # convert to upper case & add parens
    
    numVars = 0
    for ch in equ:
        if ch in chars and var[ord(ch)-ord('A')] == 0:
            var[ord(ch)-ord('A')] = 1
            numVars += 1

    # prepare equation for solving
    
    equ = equ.replace('!','not ')                       # replace ! with not 
    equ = equ.replace('*',')*(').replace('+',')+(')     # add ()s before/after +/*
    # replace each character with var[#]
    for char in chars:
        equ = equ.replace(char, 'var['+str(chars.index(char))+']')

    # print table header
    for c in range(numVars):
        print chars[c],
    print '| S'
    print '='*(2*numVars+3)

    # print the rows
    for n in range(2**numVars):         # there are 2**numVars rows
        var = numToInputs(n,numVars)    # rows go sequentially from 0..2**numVars-1
        s = int(eval(equ) > 0)          # the trick: use python's eval to evaluate the equation string for the current equation
        for c in range(numVars):        # print variables in the row
            print var[c],               
        print '|',s                     # print the solution

def main():
    if  len(sys.argv) == 1:
        printTable(raw_input())
    elif len(sys.argv) == 2:
        printTable(sys.argv[1])
    else:
        print """Usage: ./ttgen equation"""

if __name__ == '__main__':
    main()

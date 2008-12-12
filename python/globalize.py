"""
globalize.py -- Because flat is better than nested.

    Version 0.1 - 18 September 2008

    James Turk <james.p.turk@gmail.com>
   
Features:
    Creates *unbelievable* speed benefits via preloading entire modules!
    No need to load modules in every file, if you use it one place it is loaded
        everywhere.  (Saves Typing & Reduces Code Size!)
    Django 1.0 Compatible!
    
Usage:
    >>> globalize("math")
    >>> math_sqrt(4)
    2.0
"""

from types import ModuleType

_globalized = set()

def globalize(modulename, module=None):
    if not module:
        module = __import__(modulename)
    _globalized.add(module)
    for key,val in module.__dict__.iteritems():
        newname = modulename+'_'+key
        if newname not in globals():
            if isinstance(val, ModuleType) and val not in _globalized:
                globalize(newname, val)
            else:
                globals()[newname] = val


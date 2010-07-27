from abc import ABCMeta
from collections import MutableMapping

from garfield.fields import Field, NoDefault

class ItemMetaclass(ABCMeta):
    """
        Metaclass for Items, primary purpose is to properly attach Fields
    """
    def __new__(cls, name, bases, attrs):
        try:
            if not filter(lambda b: issubclass(b, Item), bases):
                return super(ItemMetaclass, cls).__new__(cls, name, bases, attrs)
        except NameError:
            pass

        fields = {}

        # inherit parent fields
        for base in bases:
            if isinstance(base, ItemMetaclass):
                fields.update(base.fields)

        # get all field attributes
        for attrname, attr in attrs.items():
            if isinstance(attr, Field):
                attr.name = attrname
                fields[attrname] = attr

        attrs['fields'] = fields

        return super(ItemMetaclass, cls).__new__(cls, name, bases, attrs)

class Item(MutableMapping):
    __metaclass__ = ItemMetaclass

    def __init__(self):
        # set defaults
        for attrname, attr in self.fields.items():
            if attr.default != NoDefault:
                self.__dict__[attrname] = attr.default

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __delitem__(self, key):
        delattr(self, key)

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)


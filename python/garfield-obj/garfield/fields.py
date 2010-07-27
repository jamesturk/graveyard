import copy

class NoDefault:
    pass

class Field(object):
    """
        Base Field type, only to be declared inside of subclasses of Item
    """
    def __init__(self, default=NoDefault, validators=None):
        self.name = None
        self.default = default
        if validators:
            self.validators = copy.deepcopy(validators)
        else:
            self.validators = []

    def __get__(self, obj, cls):
        # called on class
        if obj is None:
            return self

        # cache value within obj.__dict__ for next time
        if self.name not in obj.__dict__:
            raise AttributeError("'%s' has no attribute '%s'" %
                                 (obj.__class__.__name__, self.name))

        return obj.__dict__[self.name]

    def __set__(self, obj, value):
        for validator in self.validators:
            if not validator(value):
                raise ValueError('validation failed')
        obj.__dict__[self.name] = value

    def __delete__(self, obj):
        try:
            del obj.__dict__[self.name]
        except KeyError:
            pass

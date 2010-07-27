import unittest

from garfield.fields import Field
from garfield import Item

class TestItem(Item):
    boring   = Field()
    default3 = Field(default=3)
    positive = Field(validators=[lambda x: x > 0])

class ItemTests(unittest.TestCase):

    def test_fields_list(self):
        self.assertTrue(hasattr(TestItem(), 'fields'))

    def test_normal_field(self):
        t = TestItem()
        t.boring = 8
        self.assertEqual(t.boring, 8)

    def test_default_field(self):
        t = TestItem()
        self.assertEqual(t.default3, 3)
        t.default3 = 'three'
        self.assertEqual(t.default3, 'three')

    def test_validator_field(self):
        t = TestItem()
        t.positive = 500
        self.assertEqual(t.positive, 500)
        def bad():
            t.positive = -500
        self.assertRaises(ValueError, bad)

    def test_nonspecified_field(self):
        t = TestItem()
        t.newfield = 'new'
        self.assertEqual(t.newfield, 'new')

    def test_nonspecified_field_dict(self):
        t = TestItem()
        # set as attr, retrieve as dict
        t.newfield = 'new'
        self.assertEqual(t['newfield'], 'new')
        # set as dict, retrieve as attr
        t['another'] = 'another'
        self.assertEqual('another', t.another)

    def test_dict_get(self):
        t = TestItem()
        self.assertEqual(t['default3'], 3)

    def test_dict_set(self):
        t = TestItem()
        t['boring'] = 'test'
        self.assertEqual(t.boring, 'test')
        self.assertEqual(t['boring'], 'test')

    def test_dict_set_validator(self):
        t = TestItem()
        def bad():
            t['positive'] = -500
        self.assertRaises(ValueError, bad)

    def test_dict_iter(self):
        t = TestItem()
        # initially only default is around
        keys = [key for key in t]
        self.assertEqual(keys, ['default3'])
        t.newbie = t.default3
        keys = [key for key in t]
        self.assertEqual(keys, ['newbie', 'default3'])

    def test_dict_len(self):
        t = TestItem()
        self.assertEqual(len(t), 1)     # 1 default is set

        t.newbie = 'x'
        self.assertEqual(len(t), 2)

        # back down
        del t.newbie
        self.assertEqual(len(t), 1)

        # deletion of 


if __name__ == '__main__':
    unittest.main()

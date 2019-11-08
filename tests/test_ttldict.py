"""
Unit tests for TTLDict
"""

from unittest import TestCase
from pyttl import TTLDict
import time


class TTLDictTest(TestCase):
    """ TTLDict tests """
    def test_update_no_ttl(self):
        """ Test update() call """
        ttl_dict = TTLDict()
        orig_dict = {'hello': 'world', 'int_val': 3}
        ttl_dict.update(orig_dict)
        self.assertEqual(sorted(orig_dict.items()), sorted(ttl_dict.items()))

    def test_len_clears_expired_items(self):
        """ Test that calling len() removes expired items """
        ttl_dict = TTLDict()
        ttl_dict.setex('a', -1, 1)
        ttl_dict.setex('b', -1, 1)
        self.assertEqual(list(ttl_dict.data.keys()), sorted(['a', 'b']))
        self.assertEqual(len(ttl_dict), 0)
        self.assertEqual(list(ttl_dict.data.keys()), [])

    def test_set_ttl_get_ttl(self):
        """ Test set_ttl() and get_ttl() """
        ttl_dict = TTLDict()
        ttl_dict.setex('foo', 120, 3)
        ttl_dict.setex('bar', 120, None)
        self.assertEqual(sorted(ttl_dict), ['bar', 'foo'])
        self.assertEqual(ttl_dict['foo'], 3)
        self.assertEqual(ttl_dict['bar'], None)
        self.assertEqual(len(ttl_dict), 2)
        ttl_dict.expire('foo', 3)
        ttl_foo = ttl_dict.ttl('foo')
        self.assertTrue(ttl_foo <= 3.0)
        ttl_bar = ttl_dict.ttl('bar')
        self.assertTrue(ttl_bar - ttl_foo > 100)

    def test_expire_key_error(self):
        """ Test that set_ttl() raises KeyError """
        ttl_dict = TTLDict()
        self.assertRaises(KeyError, ttl_dict.expire, 'missing', 10)

    def test_ttl_key_error(self):
        """ Test that get_ttl() raises KeyError """
        ttl_dict = TTLDict()
        self.assertRaises(KeyError, ttl_dict.ttl, 'missing')

    def test_iter_empty(self):
        """ Test that empty TTLDict can be iterated """
        ttl_dict = TTLDict()
        for key in ttl_dict:
            self.fail("Iterating empty dictionary gave a key %r" % (key,))

    def test_iter(self):
        """ Test that TTLDict can be iterated """
        ttl_dict = TTLDict()
        ttl_dict.update(zip(range(10), range(10)))
        self.assertEqual(len(ttl_dict), 10)
        for key in ttl_dict:
            self.assertEqual(key, ttl_dict[key])

    def test_ttl(self):
        """ Test is_expired() call """
        now = time.time()
        ttl_dict = TTLDict()
        ttl_dict.setex('a', 60, 1)
        ttl_dict.setex('b', 60, 2)
        self.assertTrue(ttl_dict.ttl('a') > 0)
        self.assertTrue(ttl_dict.ttl('a', now=now) > 0)
        self.assertTrue(ttl_dict.ttl('a', now=now+61) < 0)
        self.assertEqual(len(ttl_dict), 1)

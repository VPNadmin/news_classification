# test_with_unittest.py

from unittest import TestCase

class TryTesting(TestCase):
    def test_always_passes(self):
        self.assertTrue(True)

    # def test_always_fails(self):
    #     self.assertTrue(False,msg="yoyoyoyoy always fail wala to fail ho gyaa...")
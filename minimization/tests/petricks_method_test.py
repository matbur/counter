import unittest

from minimization import *


class TestPetricksMethod(unittest.TestCase):
    def test_gen_numbers(self):
        self.assertEqual(list(gen_numbers('0000')), ['0000'])
        self.assertEqual(list(gen_numbers('10-1')), ['1001', '1011'])
        self.assertEqual(list(gen_numbers('-0-1')), ['0001', '0011', '1001', '1011'])

    def test_join(self):
        self.assertEqual(join(['1-00'], ['0-11']), [{'1-00', '0-11'}])
        self.assertEqual(join(['--1-'], ['--1-']), [{'--1-'}])
        self.assertEqual(join(['1-1-', '0010'], ['--1-']), [{'--1-', '1-1-'}, {'--1-', '0010'}])


if __name__ == '__main__':
    unittest.main()

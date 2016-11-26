import unittest

from minimization import Petricks


class TestPetricks(unittest.TestCase):
    def test_gen_numbers(self):
        gen_numbers = Petricks._Petricks__gen_numbers
        self.assertEqual(list(gen_numbers('0000')), ['0000'])
        self.assertEqual(list(gen_numbers('10-1')), ['1001', '1011'])
        self.assertEqual(list(gen_numbers('-0-1')), ['0001', '0011', '1001', '1011'])

    def test_join(self):
        join = Petricks._Petricks__join
        self.assertEqual(join(['1-00'], ['0-11']), [{'1-00', '0-11'}])
        self.assertEqual(join(['--1-'], ['--1-']), [{'--1-'}])
        self.assertEqual(join(['1-1-', '0010'], ['--1-']), [{'--1-', '1-1-'}, {'--1-', '0010'}])

    def test_all(self):
        self.assertSetEqual(Petricks({'1--0', '-100', '1-1-', '10--'}, [4, 8, 10, 11, 12, 15]).get(),
                            {'1--0', '-100', '1-1-'})
        self.assertSetEqual(Petricks({'00-', '11-', '-01', '-10', '0-0', '1-1'}, [0, 1, 2, 5, 6, 7]).get(),
                            {'11-', '-01', '0-0'})

        if __name__ == '__main__':
            unittest.main()

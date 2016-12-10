import unittest

from minimization import D, J, JK, K, T


class TestFlipFlops(unittest.TestCase):
    def test_J_for_int(self):
        self.assertEqual(J(0, 0), 0)
        self.assertEqual(J(0, 1), 1)
        self.assertEqual(J(1, 0), '*')
        self.assertEqual(J(1, 1), '*')
        self.assertEqual(J('*', 0), '*')
        self.assertEqual(J(0, '*'), '*')
        self.assertEqual(J('*', 1), '*')
        self.assertEqual(J(1, '*'), '*')

    def test_J_for_string(self):
        self.assertEqual(J('0', '0'), 0)
        self.assertEqual(J('0', '1'), 1)
        self.assertEqual(J('1', '0'), '*')
        self.assertEqual(J('1', '1'), '*')
        self.assertEqual(J('*', '0'), '*')
        self.assertEqual(J('0', '*'), '*')
        self.assertEqual(J('*', '1'), '*')
        self.assertEqual(J('1', '*'), '*')

    def test_J_for_name(self):
        self.assertEqual(J.name, 'J')

    def test_K_for_int(self):
        self.assertEqual(K(0, 0), '*')
        self.assertEqual(K(0, 1), '*')
        self.assertEqual(K(1, 0), 1)
        self.assertEqual(K(1, 1), 0)
        self.assertEqual(K('*', 0), '*')
        self.assertEqual(K(0, '*'), '*')
        self.assertEqual(K('*', 1), '*')
        self.assertEqual(K(1, '*'), '*')

    def test_K_for_string(self):
        self.assertEqual(K('0', '0'), '*')
        self.assertEqual(K('0', '1'), '*')
        self.assertEqual(K('1', '0'), 1)
        self.assertEqual(K('1', '1'), 0)
        self.assertEqual(K('*', '0'), '*')
        self.assertEqual(K('0', '*'), '*')
        self.assertEqual(K('*', '1'), '*')
        self.assertEqual(K('1', '*'), '*')

    def test_K_for_name(self):
        self.assertEqual(K.name, 'K')

    def test_JK_for_int(self):
        self.assertEqual(JK(0, 0), (0, '*'))
        self.assertEqual(JK(0, 1), (1, '*'))
        self.assertEqual(JK(1, 0), ('*', 1))
        self.assertEqual(JK(1, 1), ('*', 0))
        self.assertEqual(JK('*', '0'), ('*', '*'))
        self.assertEqual(JK('0', '*'), ('*', '*'))
        self.assertEqual(JK('*', '1'), ('*', '*'))
        self.assertEqual(JK('1', '*'), ('*', '*'))

    def test_JK_for_string(self):
        self.assertEqual(JK('0', '0'), (0, '*'))
        self.assertEqual(JK('0', '1'), (1, '*'))
        self.assertEqual(JK('1', '0'), ('*', 1))
        self.assertEqual(JK('1', '1'), ('*', 0))
        self.assertEqual(JK('*', 0), ('*', '*'))
        self.assertEqual(JK(0, '*'), ('*', '*'))
        self.assertEqual(JK('*', 1), ('*', '*'))
        self.assertEqual(JK(1, '*'), ('*', '*'))

    def test_D_for_int(self):
        self.assertEqual(D(0), 0)
        self.assertEqual(D(1), 1)
        self.assertEqual(D(0, 0), 0)
        self.assertEqual(D(0, 1), 1)
        self.assertEqual(D(1, 0), 0)
        self.assertEqual(D(1, 1), 1)
        self.assertEqual(D('*', 0), '*')
        self.assertEqual(D(0, '*'), '*')
        self.assertEqual(D('*', 1), '*')
        self.assertEqual(D(1, '*'), '*')

    def test_D_for_string(self):
        self.assertEqual(D('0'), 0)
        self.assertEqual(D('1'), 1)
        self.assertEqual(D('*'), '*')
        self.assertEqual(D('0', '0'), 0)
        self.assertEqual(D('0', '1'), 1)
        self.assertEqual(D('1', '0'), 0)
        self.assertEqual(D('1', '1'), 1)
        self.assertEqual(D('*', '0'), '*')
        self.assertEqual(D('0', '*'), '*')
        self.assertEqual(D('*', '1'), '*')
        self.assertEqual(D('1', '*'), '*')

    def test_D_for_name(self):
        self.assertEqual(D.name, 'D')

    def test_T_for_int(self):
        self.assertEqual(T(0, 0), 0)
        self.assertEqual(T(0, 1), 1)
        self.assertEqual(T(1, 0), 1)
        self.assertEqual(T(1, 1), 0)
        self.assertEqual(T('*', 0), '*')
        self.assertEqual(T(0, '*'), '*')
        self.assertEqual(T('*', 1), '*')
        self.assertEqual(T(1, '*'), '*')

    def test_T_for_string(self):
        self.assertEqual(T('0', '0'), 0)
        self.assertEqual(T('0', '1'), 1)
        self.assertEqual(T('1', '0'), 1)
        self.assertEqual(T('1', '1'), 0)
        self.assertEqual(T('*', '0'), '*')
        self.assertEqual(T('0', '*'), '*')
        self.assertEqual(T('*', '1'), '*')
        self.assertEqual(T('1', '*'), '*')

    def test_T_for_name(self):
        self.assertEqual(T.name, 'T')


if __name__ == '__main__':
    unittest.main()

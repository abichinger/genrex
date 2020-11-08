
import unittest
import genrex
import sys

class TestGenrex(unittest.TestCase):

    def test_literal(self):
        p = genrex.parse('abc')
        self.assertEqual(len(p), 1)
        self.assertEqual(p[0], 'abc')
        self.assertEqual(p.random(), 'abc')

    def test_literal_escaped(self):
        p = genrex.parse(r'\.\?')
        self.assertEqual(p[0], '.?')

    def test_dot(self):
        p = genrex.parse('.')
        self.assertEqual(len(p), sys.maxunicode-1)

    def test_set_simple(self):
        p = genrex.parse('[abc]')
        self.assertEqual(len(p), 3)
        self.assertTrue(p.random() in ['a', 'b', 'c'])

    def test_set_range(self):
        digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
        p = genrex.parse('[0-9a-f][0-9a-f]')
        self.assertEqual(len(p), 256)
        r = p.random()
        self.assertTrue(r[0] in digits and r[1] in digits)

    def test_set_inverted(self):
        p = genrex.parse('[^a]')
        self.assertTrue(len(p) > 1)

    def test_branch(self):
        p = genrex.parse('a|b|c')
        self.assertEqual(len(p), 3)
        self.assertTrue(p.random() in ['a', 'b', 'c'])

        p = genrex.parse('1:[a-c]|2:[x-z]|3:[1-3]')
        self.assertEqual(len(p), 9)
        self.assertTrue('3:1' in p and '3:a' not in p)

    def test_group(self):
        p = genrex.parse('(x|y)(1|2)')
        self.assertEqual(len(p), 4)
        self.assertTrue(p.random() in ['x1', 'y1', 'x2', 'y2'])

    def test_repetition(self):
        res = ['a'*i for i in range(6)]
        p = genrex.parse('a{0,5}')
        self.assertEqual(len(p), 6)
        for s in p:
            self.assertTrue(s in res)

        p = genrex.parse('a{5}')
        self.assertEqual(len(p), 1)
        self.assertEqual(p[0], 'aaaaa')

        p = genrex.parse('a{0,5}?')
        self.assertEqual(len(p), 6)
        for s in p:
            self.assertTrue(s in res)
 
    def test_star(self):
        p = genrex.parse('a*', max_depth=5)
        self.assertEqual(len(p), 6)

    def test_plus(self):
        p = genrex.parse('a+', max_depth=5)
        self.assertEqual(len(p), 5)

    def test_question_mark(self):
        p = genrex.parse('a?')
        self.assertEqual(len(p), 2)
        for s in p:
            self.assertTrue(s in ['', 'a'])

    def test_digit(self):
        p = genrex.parse('\d')
        self.assertTrue(len(p) > 10)

    def test_advanced_patterns(self):
        raise Exception('not implemented')
import unittest
import remove2ndInstance


class TestRemove2ndInstancev5(unittest.TestCase):
    def test_case_1(self):
        print('test for list within which no item repeates:')
        inp = [3, 2, 6, 7, 9, 89, 45, 0, 1]
        result = remove2ndInstance.remove2ndInstancev5(inp)
        expected = inp
        self.assertEqual(result, expected)

    def test_case_2(self):
        print('Test for list, one of whose item repeates:')
        inp = [0, 12, 12, 0, 12, 12, 34, 56, 23]
        result = remove2ndInstance.remove2ndInstancev5(inp)
        expected = [0, 12, 12, 12, 12, 34, 56, 23]
        self.assertEqual(result, expected)


class TestRemove2ndInstancev6(unittest.TestCase):
    def test_case_1(self):
        print('test for list whin which no item repeates')
        inp = [3, 2, 6, 7, 9, 89, 45, 0, 1]
        result = remove2ndInstance.remove2ndInstanceV6(inp)
        expected = inp
        self.assertEqual(result, expected)

    def test_case_2(self):
        print('Test for list, one of whose item repeates:')
        inp = [0, 12, 12, 0, 12, 12, 34, 56, 23]
        result = remove2ndInstance.remove2ndInstanceV6(inp)
        expected = [0, 12, 0, 12, 12, 34, 56, 23]
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()

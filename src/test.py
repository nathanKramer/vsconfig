import unittest
import cli

class TestCli(unittest.TestCase):

    def test_parse_flags(self):
        cases = [
            (['--file', 'work'], { 'file': 'work' }),
            (['--flag', 'value', '--something', 'else', '--fruit', 'banana'],
                { 'flag': 'value', 'something': 'else', 'fruit': 'banana' }
            )
        ]
        for case in cases:
            self.assertEqual(cli.parse_flags(case[0]), case[1]) 

if __name__ == '__main__':
    unittest.main()
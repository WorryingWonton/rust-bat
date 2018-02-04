import unittest
from printbat_builder import *
print(build_string(build_input('p145416')))

class Test_emptyvechandler(unittest.TestCase):
    def test_i32(self):
        self.assertEqual(['Vec::<i32>::new()'], inv_vec_handler(['int[]'], '(\'Vec::<>::new()\')'))

if __name__ == '__main__':
    unittest.main()
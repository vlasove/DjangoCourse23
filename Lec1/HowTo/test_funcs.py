import funcs as f 

import unittest 

class TestFuncs(unittest.TestCase):
    def test_add(self):
        self.assertEqual(f.add(2,3), 5) 
        self.assertEqual(f.add(0, 5), 5)
        self.assertEqual(f.add(-1, -2), -3)


    def test_sub(self):
        self.assertEqual(f.sub(5, 1), 4)

    def test_mult(self):
        self.assertEqual(f.mult(2,2), 4) 
        self.assertEqual(f.mult(1, 10), 10)
    def test_div(self):
        self.assertEqual(f.div(4,3), 1) 
        self.assertEqual(f.div(-4,3), -2)

if __name__ == "__main__":
    unittest.main()
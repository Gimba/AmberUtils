import unittest
import Occupancy as occ

class OccupancyTests(unittest.TestCase):
    def test_number_of_inputs(self):
        result = len(occ.argv)
        self.assertEqual(7, result)

if __name__ == '__main__':
    unittest.main()

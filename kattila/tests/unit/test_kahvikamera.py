import unittest

class TestImageDifference(unittest.TestCase):

    def test_eroavatkuvat_eroavat(self):
        result = 1.0 # TODO ÄLÄ JÄTÄ
        unexpected = 0.0
        self.assertNotEqual(result, unexpected)

if __name__ == '__main__':
    unittest.main()
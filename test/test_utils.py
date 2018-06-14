import unittest
from pythonping import utils


class UtilsTestCase(unittest.TestCase):
    """Tests for Utils class"""

    def test_random_text_generation(self):
        """Verifies that random_text generates text of correct size"""
        sizes = [0, 4, 1500, 1, 33, 44, 11]
        for size in sizes:
            self.assertEqual(
                len(utils.random_text(size)), size,
                'Unable to generate a random string of {0} characters'.format(size))

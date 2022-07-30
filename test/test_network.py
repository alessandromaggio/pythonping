import unittest
from pythonping.network import Socket


class UtilsTestCase(unittest.TestCase):
    """Tests for Socket class"""

    def test_raise_explicative_error_on_name_resolution_failure(self):
        """Test a runtime error is generated if the name cannot be resolved"""
        with self.assertRaises(RuntimeError):
            Socket('invalid', 'raw')

import unittest
from pythonping import executor


class ExecutorUtilsTestCase(unittest.TestCase):
    """Tests for standalone functions in pythonping.executor"""

    def test_represent_seconds_in_ms(self):
        """Verifies conversion from seconds to milliseconds works correctly"""
        self.assertEqual(executor.represent_seconds_in_ms(4), 4000, 'Failed to convert seconds to milliseconds')
        self.assertEqual(executor.represent_seconds_in_ms(0), 0, 'Failed to convert seconds to milliseconds')
        self.assertEqual(executor.represent_seconds_in_ms(0.001), 1, 'Failed to convert seconds to milliseconds')
        self.assertEqual(executor.represent_seconds_in_ms(0.0001), 0.1, 'Failed to convert seconds to milliseconds')
        self.assertEqual(executor.represent_seconds_in_ms(0.00001), 0.01, 'Failed to convert seconds to milliseconds')


class ResponseTestCase(unittest.TestCase):
    """Tests to verify that a Response object renders information correctly"""

    def test_success(self):
        """Verifies the if the Response can indicate a success to a request correctly"""
        pass

    def test_error_message(self):
        """Verifies error messages are presented correctly"""
        pass

    def time_elapsed(self):
        """Verifies the time elapsed is presented correctly"""
        pass


class ResponseListTestCase(unittest.TestCase):
    """Tests for ResponseList"""

    def test_rtt_min_ms(self):
        """Verifies the minimum RTT is found correctly"""
        pass

    def test_rtt_max_ms(self):
        """Verifies the maximum RTT is found correctly"""
        pass

    def test_rtt_avg_ms(self):
        """Verifies the average RTT is found correctly"""
        pass

    def test_len(self):
        """Verifies the length is returned correctly"""
        pass


class CommunicatorTestCase(unittest.TestCase):
    """Tests for Communicator"""

    def test_increase_seq(self):
        """Verifies Communicator can increase sequence number correctly"""
        self.assertEqual(executor.Communicator.increase_seq(1), 2, 'Increasing sequence number 1 did not return 2')
        self.assertEqual(executor.Communicator.increase_seq(100), 101, 'Increasing sequence number 1 did not return 2')
        self.assertEqual(executor.Communicator.increase_seq(0xFFFF), 1,
                         'Not returned to 1 when exceeding sequence number maximum length')
        self.assertEqual(executor.Communicator.increase_seq(0xFFFE), 0xFFFF,
                         'Increasing sequence number 0xFFFE did not return 0xFFFF')

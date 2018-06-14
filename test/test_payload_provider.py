import unittest
from pythonping import payload_provider


class PayloadProviderTestCase(unittest.TestCase):
    """Tests for PayloadProvider class"""

    def test_list(self):
        """Verifies that a list provider generates the correct payloads"""
        payloads = [
            b'payload A',
            b'second payload'
            b'payload 3+'
        ]
        res = []
        provider = payload_provider.List(payloads)
        for payload in provider:
            res.append(payload)
        for num, payload in enumerate(payloads):
            self.assertEqual(res[num], payload, 'Payload not expected in position {0}'.format(num))

    def test_repeat(self):
        """Verifies that a repeat provider generates the correct payloads"""
        pattern = b'this is a pattern'
        count = 5
        provider = payload_provider.Repeat(pattern, count)
        for payload in provider:
            self.assertEqual(payload, pattern, 'Payload does not reflect the pattern')
            count -= 1
        self.assertEqual(count, 0, 'Generated a wrong number of payloads')

    def sweep_tester(self, pattern, start, end):
        """Runs the creation of a sweep provider and performs some basics tests on it"""
        provider = payload_provider.Sweep(pattern, start, end)
        payloads_generated = 0
        for payload in provider:
            self.assertEqual(len(payload), start, 'Generated a payload with a wrong size')
            start += 1
            payloads_generated += 1
        self.assertEqual(start, end+1, 'Generated a wrong number of payloads')
        return payloads_generated

    def test_sweep_normal(self):
        """Verifies that a sweep provider generates the correct payloads"""
        self.sweep_tester(b'abc', 10, 20)

    def test_sweep_one(self):
        """Verifies that a sweep provider generates one correct payload if start and end sizes are equal"""
        self.assertEqual(
            self.sweep_tester(b'frog', 40, 40),
            1,
            'Unable to generate exactly 1 payload during a sweep')

    def test_sweep_reversed(self):
        """Verifies that it is not possible to generate a payload with start size greater than end size"""
        with self.assertRaises(ValueError):
            payload_provider.Sweep(b'123', 100, 45)

    def test_sweep_no_pattern(self):
        """Verifies that it is not possible to generate a payload with an empty pattern"""
        with self.assertRaises(ValueError):
            payload_provider.Sweep(b'', 1, 10)

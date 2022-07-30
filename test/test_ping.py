import unittest
import os
from pythonping import ping


class PingCase(unittest.TestCase):
    """Tests for actual ping against localhost"""

    def test_ping_execution(self):
        """Verifies that random_text generates text of correct size"""
        # NOTE, this may be considered an e2e test
        self.assertEqual(len(ping('10.127.0.1', count=4, size=10)), 4,
                         'Sent 4 pings to localhost, but not received 4 responses')

        # Github Actions does not support ICMP
        if os.getenv("GITHUB_ACTIONS") is None:
            self.assertEqual(ping('8.8.8.8', count=4, size=992).success(), True,
                             'Sent 4 large pings to google DNS A with payload match off, received all replies')

            self.assertEqual(ping('8.8.8.8', count=4, size=992, match=True).success(), False,
                             'Sent 4 large pings to google DNS A with payload match on,'
                             + 'expected all to fail since they truncate large payloads')

"""Tests for miscelleanous functions."""

import datetime
import unittest

import care_calendar


class TestCurrentYear(unittest.TestCase):
    """Tests for care_calendar.current_year."""

    def test_returns_int(self):
        self.assertIsInstance(care_calendar.current_year(), int)

    def test_actually_returns_the_current_year(self):
        self.assertEqual(care_calendar.current_year(), datetime.datetime.now().year)

"""Tests for miscelleanous functions."""

import datetime
import random
import unittest

import care_calendar


class TestCurrentYear(unittest.TestCase):
    """Tests for care_calendar.current_year."""

    def test_returns_int(self):
        self.assertIsInstance(care_calendar.current_year(), int)

    def test_actually_returns_the_current_year(self):
        self.assertEqual(care_calendar.current_year(), datetime.datetime.now().year)


class TestWeekId(unittest.TestCase):
    """Tests for care_calendar.week_id."""

    def test_within_1_53(self):
        year = 2021
        for month in range(1, 13):
            for day in (1, 28, 29, 30, 31):
                try:
                    date = datetime.date(year, month, day)
                except ValueError:
                    pass
                else:
                    self.assertGreaterEqual(care_calendar.week_id(date), 1)
                    self.assertLessEqual(care_calendar.week_id(date), 53)

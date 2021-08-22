#!/usr/bin/env python

"""Tests for `care_calendar` package."""

import unittest

from care_calendar import Calendar, current_year

class TestCalendar(unittest.TestCase):
    """Tests for care_calendar.Calendar"""

    def test_initialize_with_current_year_by_default(self):
        cal = Calendar()
        self.assertEqual(cal.year, current_year())

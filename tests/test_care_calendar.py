#!/usr/bin/env python

"""Tests for `care_calendar` package."""

import unittest

from care_calendar import Calendar, current_year

class TestCalendar(unittest.TestCase):
    """Tests for care_calendar.Calendar"""

    def setUp(self):
        self.calendar = Calendar()

    def test_initialize_with_current_year_by_default(self):
        self.assertEqual(self.calendar.year, current_year())

    def test_format_month_returns_an_html_table(self):
        html = self.calendar.format_month(1)
        self.assertIsInstance(html, str)
        self.assertTrue(html.startswith("<table>"))
        self.assertTrue(html.endswith("</table>"))

    def test_format_month_name_is_a_table_row_header(self):
        html = self.calendar.format_month_name(1)
        self.assertTrue(html.startswith("<tr><th"))
        self.assertTrue(html.endswith("</th></tr>"))

    def test_format_month_name_has_adequate_value(self):
        for month in range(1, 13):
            html = self.calendar.format_month_name(month)
            self.assertIn(self.calendar.month_name[month], html)

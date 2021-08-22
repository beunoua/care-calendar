#!/usr/bin/env python

"""Tests for `care_calendar` package."""

from calendar import month_name
import datetime
import unittest

from care_calendar import Calendar, current_year

class TestCalendar(unittest.TestCase):
    """Tests for care_calendar.Calendar"""

    def setUp(self):
        self.year = 2021
        self.calendar = Calendar(self.year)

    def test_initialize_with_current_year_by_default(self):
        self.assertEqual(self.calendar.year, current_year())

    def test_format_month_returns_an_html_table(self):
        html = self.calendar.format_month(1)
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

    def test_format_day_is_a_table_row(self):
        day = datetime.datetime.now()
        html = self.calendar.format_day(day)
        self.assertTrue(html.startswith("<tr"))
        self.assertTrue(html.endswith("</tr>"))

    def test_format_day_contains_the_date_data(self):
        day = datetime.datetime.now()
        html = self.calendar.format_day(day)
        self.assertIn(str(day.day), html)
        self.assertIn(self.calendar.day_abbr[day.weekday()], html)

    def test_iter_month_dates(self):
        month = 1
        for date in self.calendar.iter_month_dates(month):
            self.assertEqual(date.month, month)
            self.assertEqual(date.year, self.year)


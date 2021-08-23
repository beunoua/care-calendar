"""Tests for `care_calendar.status` module."""


import unittest

from care_calendar.status import str_to_date


class TestStrToDate(unittest.TestCase):

    def test_date_from_day_and_month(self):
        date_str = "12/01"
        date = str_to_date(date_str, 2021)
        self.assertEqual(date.day, 12)
        self.assertEqual(date.month, 1)
        self.assertEqual(date.year, 2021)

    def test_date_from_day_month_and_year(self):
        date_str = "12/01/2000"
        date = str_to_date(date_str)
        self.assertEqual(date.day, 12)
        self.assertEqual(date.month, 1)
        self.assertEqual(date.year, 2000)

    def test_date_from_day_month_and_year_2_digits(self):
        date_str = "12/01/22"
        date = str_to_date(date_str)
        self.assertEqual(date.day, 12)
        self.assertEqual(date.month, 1)
        self.assertEqual(date.year, 2022)

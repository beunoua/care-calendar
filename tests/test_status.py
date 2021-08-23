"""Tests for `care_calendar.status` module."""


import datetime
import os
import unittest

from care_calendar.status import str_to_date, date_range_to_list, read_status_yaml


class TestStrToDate(unittest.TestCase):
    """Tests for care_calendar.status.str_to_date."""

    def test_returns_a_date(self):
        date_str = "12/01"
        date = str_to_date(date_str, 2021)
        self.assertIsInstance(date, datetime.date)

    def test_date_from_day_and_month(self):
        date_str = "12/01"
        date = str_to_date(date_str, 2021)
        self.assertEqual(date.day, 12)
        self.assertEqual(date.month, 1)
        self.assertEqual(date.year, 2021)

    def test_date_from_day_and_month_year_as_argument(self):
        date_str = "12/01"
        date = str_to_date(date_str, 1912)
        self.assertEqual(date.day, 12)
        self.assertEqual(date.month, 1)
        self.assertEqual(date.year, 1912)

    def test_date_from_day_month_no_year(self):
        date_str = "12/01"
        date = str_to_date(date_str)
        self.assertEqual(date.day, 12)
        self.assertEqual(date.month, 1)
        self.assertEqual(date.year, 2021)

    def test_date_from_day_month_and_year(self):
        date_str = "12/01/2000"
        date = str_to_date(date_str)
        self.assertEqual(date.day, 12)
        self.assertEqual(date.month, 1)
        self.assertEqual(date.year, 2000)

    def test_date_from_an_other_century(self):
        date_str = "12/01/1912"
        date = str_to_date(date_str)
        self.assertEqual(date.day, 12)
        self.assertEqual(date.month, 1)
        self.assertEqual(date.year, 1912)

    def test_date_from_day_month_and_year_2_digits(self):
        date_str = "12/01/22"
        date = str_to_date(date_str)
        self.assertEqual(date.day, 12)
        self.assertEqual(date.month, 1)
        self.assertEqual(date.year, 2022)

    def test_too_many_tokens(self):
        date_str = "12/01/22/43"
        with self.assertRaises(ValueError):
            str_to_date(date_str)

    def test_invalid_date(self):
        date_str = "12/14/22"  # invalid month "14"
        with self.assertRaises(ValueError):
            str_to_date(date_str)

    def test_passed_but_also_in_str(self):
        date_str = "12/01/22"
        with self.assertRaises(ValueError):
            str_to_date(date_str, 2021)


class TestDateRangeToList(unittest.TestCase):
    """Tests for care_calendar.status.date_range_to_list."""

    def test_returns_a_list_of_dates(self):
        dates = date_range_to_list("13/02 - 15/02", 1912)
        self.assertIsInstance(dates, list)
        for date in dates:
            self.assertIsInstance(date, datetime.date)

    def test_returns_correct_dates(self):
        dates = date_range_to_list("13/02 - 15/02", 1912)
        self.assertEqual(len(dates), 3)
        for i, day in enumerate(range(13, 16)):
            self.assertEqual(dates[i].day, day)
            self.assertEqual(dates[i].month, 2)
            self.assertEqual(dates[i].year, 1912)

    def test_returns_correct_dates_no_year(self):
        dates = date_range_to_list("13/02 - 15/02", 1912)
        self.assertEqual(len(dates), 3)
        for i, day in enumerate(range(13, 16)):
            self.assertEqual(dates[i].day, day)
            self.assertEqual(dates[i].month, 2)
            self.assertEqual(dates[i].year, 1912)

    def test_accross_years(self):
        dates = date_range_to_list("28/12/20 - 06/01/21")
        self.assertEqual(len(dates), 10)
        for i, day in enumerate(range(28, 32)):
            self.assertEqual(dates[i].day, day)
            self.assertEqual(dates[i].month, 12)
            self.assertEqual(dates[i].year, 2020)
        for i, day in enumerate(range(1, 7)):
            self.assertEqual(dates[i + 4].day, day)
            self.assertEqual(dates[i + 4].month, 1)
            self.assertEqual(dates[i + 4].year, 2021)


class TestReadStatusYaml(unittest.TestCase):
    """Tests for care_calendar.status.read_status_yaml."""

    def test_read_yaml(self):
        path = os.path.join(os.path.dirname(__file__), "data", "test_status.yaml")
        data = read_status_yaml(path)
        self.assertEqual(len(data), 2)
        self.assertIn("vacances scolaires", data)
        self.assertIn("férié", data)
        self.assertEqual(len(data["vacances scolaires"]), 13)
        self.assertEqual(len(data["férié"]), 4)

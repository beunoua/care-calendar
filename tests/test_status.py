"""Tests for `care_calendar.status` module."""


import datetime
import os
import unittest

from care_calendar.status import (
    str_to_date,
    date_range_from_str,
    read_status_yaml,
    Status,
)


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


class TestDateRangeFromStr(unittest.TestCase):
    """Tests for care_calendar.status.date_range_from_str."""

    def test_returns_a_list_of_dates(self):
        dates = date_range_from_str("13/02 - 15/02", 1912)
        self.assertIsInstance(dates, list)
        for date in dates:
            self.assertIsInstance(date, datetime.date)

    def test_returns_correct_dates(self):
        dates = date_range_from_str("13/02 - 15/02", 1912)
        self.assertEqual(len(dates), 3)
        for i, day in enumerate(range(13, 16)):
            self.assertEqual(dates[i].day, day)
            self.assertEqual(dates[i].month, 2)
            self.assertEqual(dates[i].year, 1912)

    def test_returns_correct_dates_no_year(self):
        dates = date_range_from_str("13/02 - 15/02", 1912)
        self.assertEqual(len(dates), 3)
        for i, day in enumerate(range(13, 16)):
            self.assertEqual(dates[i].day, day)
            self.assertEqual(dates[i].month, 2)
            self.assertEqual(dates[i].year, 1912)

    def test_accross_years(self):
        dates = date_range_from_str("28/12/20 - 06/01/21")
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

    def setUp(self):
        self.yaml_path = os.path.join(
            os.path.dirname(__file__), "data", "test_status.yaml"
        )
        self.data = read_status_yaml(self.yaml_path)

    def test_read_yaml_returns_a_list_of_status_instances(self):
        self.assertIsInstance(self.data, list)
        for element in self.data:
            self.assertIsInstance(element, Status)

    def test_read_yaml(self):
        self.assertEqual(len(self.data), 2)
        status_vacances = self.data[0]
        self.assertEqual(status_vacances.name, "vacances scolaires")
        self.assertEqual(len(status_vacances.date_list), 13)

        status_ferie = self.data[1]
        self.assertEqual(status_ferie.name, "férié")
        self.assertEqual(len(status_ferie.date_list), 4)


class TestStatus(unittest.TestCase):
    """Tests for care_calendar.status.Status class."""

    def setUp(self):
        self.dates = [datetime.date(1921, 12, 1), datetime.date(1922, 11, 2)]
        self.status = Status("the name", self.dates)

    def test_name_stays_untouched(self):
        self.assertEqual(self.status.name, "the name")

    def test_constructor_copies_input_list(self):
        self.assertNotEqual(id(self.dates), id(self.status.date_list))

    def test_css_class_name_initialization(self):
        self.assertEqual(self.status.css_name, "thename")

    def test_len(self):
        self.assertEqual(len(self.status), 2)

    def test_contains(self):
        self.assertIn(self.dates[0], self.status)
        self.assertIn(self.dates[1], self.status)

    def test_iter(self):
        for i, date in enumerate(self.status):
            self.assertIn(date, self.dates)

#!/usr/bin/env python

"""Tests for `care_calendar` package."""

from calendar import month_name
from care_calendar import status
from care_calendar.utils import week_id
import datetime
import unittest
from unittest.case import TestCase

from bs4 import BeautifulSoup

from care_calendar import Calendar, current_year
from care_calendar.status import Status


class TestCalendar(unittest.TestCase):
    """Tests for care_calendar.Calendar"""

    def setUp(self):
        self.year = 2021
        self.calendar = Calendar(self.year)

    def test_iter_month_dates(self):
        month = 1
        for date in self.calendar.iter_month_dates(month):
            self.assertEqual(date.month, month)
            self.assertEqual(date.year, self.year)

    def test_initialize_with_current_year_by_default(self):
        self.assertEqual(self.calendar.year, current_year())


class TestCalendarFormatMonth(unittest.TestCase):
    def setUp(self):
        self.calendar = Calendar(2021)
        self.html = self.calendar.format_month(1)
        self.soup = BeautifulSoup(self.html, "html.parser")

    def test_format_month_returns_an_html_table(self):
        self.assertEqual(self.soup.find().name, "table")

    def test_format_month_name_is_a_table_row_header(self):
        html = self.calendar.format_month_name(1)
        soup = BeautifulSoup(html, "html.parser")
        first_tag = soup.find()
        self.assertEqual(first_tag.name, "tr")
        second_tag = first_tag.find()
        self.assertEqual(second_tag.name, "th")

    def test_format_month_name_value(self):
        for month in range(1, 13):
            html = self.calendar.format_month_name(month)
            soup = BeautifulSoup(html, "html.parser")
            second_tag = soup.find().find()
            self.assertEqual(second_tag.text, self.calendar.month_name[month])

    def test_month_name_has_adequate_css_class(self):
        html = self.calendar.format_month_name(1)
        soup = BeautifulSoup(html, "html.parser")
        first_tag = soup.find()
        self.assertEqual(first_tag.name, "tr")
        self.assertIn(self.calendar.css_class_month_name, first_tag.attrs["class"])


class TestCalendarFormatDay(unittest.TestCase):
    def setUp(self):
        self.calendar = Calendar(1021)
        self.day = datetime.date(1963, 7, 12)
        self.html = self.calendar.format_day(self.day)
        self.soup = BeautifulSoup(self.html, "html.parser")

    def test_format_day_is_a_table_row(self):
        self.assertTrue(self.html.startswith("<tr"))
        self.assertTrue(self.html.endswith("</tr>"))

    def test_a_day_has_4_cells(self):
        self.assertEqual(len(self.soup.find_all("td")), 4)

    def test_format_day_contains_the_date_data(self):
        html = self.calendar.format_day(self.day)
        self.assertIn(str(self.day.day), html)
        self.assertIn(self.calendar.day_abbr[self.day.weekday()], html)

    def test_weekend_rows_have_adequate_css_class(self):
        day = datetime.date(2021, 1, 2)  # Saturday
        html = self.calendar.format_day(day)
        soup = BeautifulSoup(html, "html.parser")
        tr_tag = soup.find()
        self.assertEqual(tr_tag.name, "tr")
        self.assertIn(self.calendar.css_class_weekend, tr_tag.attrs["class"])

    def test_week_rows_have_adequate_css_class(self):
        day = datetime.date(2021, 1, 1)  # Friday
        html = self.calendar.format_day(day)
        soup = BeautifulSoup(html, "html.parser")
        tr_tag = soup.find()
        self.assertEqual(tr_tag.name, "tr")
        self.assertIn(self.calendar.css_class_weekday, tr_tag.attrs["class"])


class TestCalendarFormatDayNumber(unittest.TestCase):
    def setUp(self):
        self.calendar = Calendar(1021)
        self.day = datetime.date(1963, 7, 12)
        self.html = self.calendar.format_day_number(self.day)
        self.soup = BeautifulSoup(self.html, "html.parser")

    def test_day_number_has_adequate_class(self):
        first_tag = self.soup.find()
        self.assertEqual(first_tag.name, "td")
        self.assertIn("class", first_tag.attrs)
        self.assertIn(self.calendar.css_class_day_number, first_tag.attrs["class"])


class TestCalendarFormatDayName(unittest.TestCase):
    def setUp(self):
        self.calendar = Calendar(1021)
        self.day = datetime.date(1963, 7, 12)
        self.html = self.calendar.format_day_name(self.day)
        self.soup = BeautifulSoup(self.html, "html.parser")

    def test_day_name_has_adequate_class(self):
        first_tag = self.soup.find()
        self.assertEqual(first_tag.name, "td")
        self.assertIn("class", first_tag.attrs)
        self.assertIn(self.calendar.css_class_day_name, first_tag.attrs["class"])


class TestCalendarFormatDayStatus(unittest.TestCase):
    def setUp(self):
        self.calendar = Calendar(1021)
        self.day = datetime.date(1963, 7, 12)
        self.html = self.calendar.format_day_status(self.day)
        self.soup = BeautifulSoup(self.html, "html.parser")

    def test_day_status_has_adequate_class(self):
        first_tag = self.soup.find()
        self.assertEqual(first_tag.name, "td")
        self.assertIn("class", first_tag.attrs)
        self.assertIn(
            self.calendar.css_class_day_status, first_tag.attrs["class"]
        )

    def test_day_status_is_empty(self):
        first_tag = self.soup.find()
        self.assertEqual(first_tag.name, "td")
        self.assertEqual(first_tag.encode_contents(formatter="html"), b"&nbsp;")


class TestCalendarFormatDayCare(unittest.TestCase):
    def setUp(self):
        self.calendar = Calendar(1021)
        self.day = datetime.date(1963, 7, 12)
        html = self.calendar.format_day_custody(self.day)
        self.soup = BeautifulSoup(html, "html.parser")

    def test_day_care_has_adequate_class(self):
        first_tag = self.soup.find()
        self.assertEqual(first_tag.name, "td")
        self.assertIn("class", first_tag.attrs)
        self.assertIn(self.calendar.css_class_day_custody, first_tag.attrs["class"])


class TestCalendarFormatWeekNumber(unittest.TestCase):
    def setUp(self):
        self.calendar = Calendar(2021)
        self.rowspan = 2
        self.day = datetime.date(2021, 1, 1)
        self.weekid = week_id(self.day)
        html = self.calendar.format_week_number(self.day, self.rowspan)
        self.soup = BeautifulSoup(html, "html.parser")

    def test_weekid_is_first_column(self):
        first_tag = self.soup.find()
        self.assertEqual(first_tag.name, "tr")

    def test_weekid_value(self):
        td_tag = self.soup.find().find()
        self.assertEqual(td_tag.name, "td")
        self.assertEqual(td_tag.text, str(self.weekid))

    def test_rowspan_value(self):
        td_tag = self.soup.find().find()
        self.assertEqual(td_tag.name, "td")
        self.assertIn("rowspan", td_tag.attrs)
        self.assertEqual(str(self.rowspan), td_tag.attrs["rowspan"])

    def test_week_cell_has_adequate_class(self):
        td_tag = self.soup.find().find()
        self.assertEqual(td_tag.name, "td")
        self.assertIn(self.calendar.css_class_week_number, td_tag.attrs["class"])


class TestCalendarWithStatus(unittest.TestCase):
    """Tests that providing statuses actually changes day css classes."""
    def setUp(self):
        self.calendar = Calendar(2021)
        self.day = datetime.date(2021, 1, 1)  # a Friday
        self.status = Status("my status", [self.day])

    def test_status_changed_css(self):
        """Tests css changed in the "status" cell."""
        html = self.calendar.format_day(self.day)
        tr_tag = BeautifulSoup(html, "html.parser").find("tr")
        status_cell = tr_tag.find_all("td")[2]
        self.assertEqual(status_cell.attrs["class"], [self.calendar.css_class_day_status])

        self.calendar.status_list = [self.status]
        html = self.calendar.format_day(self.day)
        tr_tag = BeautifulSoup(html, "html.parser").find("tr")
        status_cell = tr_tag.find_all("td")[2]
        self.assertEqual(
            status_cell.attrs["class"],
            [self.calendar.css_class_day_status, self.status.css_name],
        )

    def test_still_working_when_formatting_month(self):
        self.calendar.status_list = [self.status]
        html = self.calendar.format_month(1)
        tr_tag = BeautifulSoup(html, "html.parser").find("tr").find_next_sibling("tr")
        status_cell = tr_tag.find_all("td")[3]
        self.assertEqual(
            status_cell.attrs["class"],
            [self.calendar.css_class_day_status, self.status.css_name],
        )

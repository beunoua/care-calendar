#!/usr/bin/env python

"""Tests for `care_calendar` package."""

from calendar import month_name
import datetime
import unittest

from bs4 import BeautifulSoup

from care_calendar import Calendar, current_year


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
            self.calendar.css_class_day_status_blank, first_tag.attrs["class"]
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


class TestCalendarFormatWeekId(unittest.TestCase):
    def setUp(self):
        self.calendar = Calendar(2021)
        self.rowspan = 2
        self.weekid = 12
        html = self.calendar.format_week_number(self.weekid, self.rowspan, weekday=1)
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

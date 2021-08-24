"""Console script for care_calendar."""

import sys

import jinja2

import care_calendar

HTML_TEMPLATE = """\
<html>
<head>
<link rel="stylesheet" href="{{css_file}}">
</head>
<body>
{{calendar_html}}
</body>
</html>
"""


import datetime
from care_calendar.status import read_status_yaml

def main():
    """Console script for care_calendar."""

    css_file = "calendar.css"
    template = jinja2.Template(HTML_TEMPLATE)

    cal = care_calendar.Calendar(2021)
    day = datetime.date(2021, 1, 1)  # a Friday
    cal.status_list = read_status_yaml("holidays-2021.yaml")

    html = template.render(css_file=css_file, calendar_html=cal.format_year())
    with open("foo.html", "wt") as f:
        print(html, file=f)

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover

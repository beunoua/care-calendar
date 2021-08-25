"""Console script for care_calendar."""

import sys

import jinja2

import care_calendar

HTML_TEMPLATE = """\
<html>
<head>
<title>Calendrier de Garde {{this_year}}</title>
<link rel="stylesheet" href="{{css_file}}">
</head>
<body>

<h1>Calendrier de Garde {{this_year}}</h1>

<div id="legend">
{{legend_html}}
</div>
<div id="calendar">
{{calendar_html}}
</div>
<div class="comments">
This is a comment
</div>
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

    html = template.render(
        css_file=css_file,
        legend_html=cal.format_legend(),
        calendar_html=cal.format_year(),
        this_year = care_calendar.current_year(),
    )

    with open("foo.html", "wt") as f:
        print(html, file=f)

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover

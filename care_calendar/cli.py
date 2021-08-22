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


def main():
    """Console script for care_calendar."""

    css_file = "calendar.css"
    template = jinja2.Template(HTML_TEMPLATE)

    cal = care_calendar.Calendar()
    html = template.render(
        css_file=css_file,
        calendar_html=cal.format_month(1)
    )

    with open("foo.html", "wt") as f:
        print(html, file=f)

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover

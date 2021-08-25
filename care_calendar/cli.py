"""Console script for care_calendar."""

import datetime
import sys

import jinja2
import markdown

import care_calendar
from care_calendar.status import read_status_yaml


HTML_TEMPLATE = """\
<html>
<head>
<title>Calendrier de Garde {{this_year}}</title>
<link rel="stylesheet" href="{{css_file}}">
</head>
<body>

<h1>Calendrier de Garde {{this_year}}</h1>

<div id="legend">
{{html_legend}}
</div>
<div id="calendar">
{{html_calendar}}
</div>
<div class="comments">
{{html_comments}}
</div>
</body>
</html>
"""




def read_comments_markdown(path: str) -> str:
    """Read the markdown comment file.
    
    Returns the comments formatted in HTML.
    """
    with open(path, "rt") as f:
        text = f.read()
    return markdown.markdown(text)


def main():
    """Console script for care_calendar."""

    html_comments = read_comments_markdown("comments.md")

    css_file = "calendar.css"
    template = jinja2.Template(HTML_TEMPLATE)

    cal = care_calendar.Calendar(2021)
    day = datetime.date(2021, 1, 1)  # a Friday
    cal.status_list = read_status_yaml("holidays-2021.yaml")

    html = template.render(
        css_file=css_file,
        html_legend=cal.format_legend(),
        html_calendar=cal.format_year(),
        html_comments=html_comments,
        this_year=care_calendar.current_year(),
    )

    with open("foo.html", "wt") as f:
        print(html, file=f)

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover

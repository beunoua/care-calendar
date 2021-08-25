"""Console script for care_calendar."""

import datetime
import sys

import jinja2
import markdown

import care_calendar
from care_calendar.status import read_status_yaml



def read_comments_markdown(path: str) -> str:
    """Read the markdown comment file.
    
    Returns the comments formatted in HTML.
    """
    with open(path, "rt") as f:
        text = f.read()
    return markdown.markdown(text)


def read_template_jinja(path: str) -> jinja2.Template:
    """Reads the jinja template for the calendar HTML rendering."""
    with open(path, "rt") as f:
        text = f.read()
    return jinja2.Template(text)


def main():
    """Console script for care_calendar."""

    html_template = read_template_jinja("template.j2")
    html_comments = read_comments_markdown("comments.md")

    css_file = "calendar.css"
    

    cal = care_calendar.Calendar(2021)
    day = datetime.date(2021, 1, 1)  # a Friday
    cal.status_list = read_status_yaml("holidays-2021.yaml")

    html = html_template.render(
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

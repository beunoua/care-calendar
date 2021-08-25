"""Creates a calendar for children custody."""

import argparse
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


def parse_command_line() -> argparse.Namespace:
    """Command-line parsing."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "holidays",
        help="holidays YAML file",
    )
    parser.add_argument(
        "comments",
        help="comments Markdown file",
    )
    parser.add_argument(
        "--template",
        help="jinja2 template for HTML rendering",
        default="calendar.j2"
    )
    parser.add_argument(
        "--css",
        help="css styling file",
        default="calendar.css"
    )
    return parser.parse_args()


def main():
    """Console script for care_calendar."""

    args = parse_command_line()

    css_file = args.css
    html_template = read_template_jinja(args.template)
    html_comments = read_comments_markdown(args.comments)
    status_list = read_status_yaml(args.holidays)

    cal = care_calendar.Calendar(2021)
    cal.status_list = status_list

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

"""Creates a calendar for children custody."""

import argparse
import os
import sys

import jinja2
from jinja2.loaders import FileSystemLoader
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
    return jinja2.Environment(loader=FileSystemLoader(searchpath=".")).from_string(text)


def parse_command_line() -> argparse.Namespace:
    """Command-line parsing."""

    def valid_month(month: int) -> int:
        month = int(month)
        if month < 1 or month > 12:
            raise argparse.ArgumentTypeError("must be an integer in the range [1 - 12]")
        return month

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("holidays", help="holidays YAML file")
    parser.add_argument("comments", help="comments Markdown file")
    parser.add_argument(
        "-y", "--year", help="calendar year", default=care_calendar.current_year()
    )
    parser.add_argument(
        "--template", help="jinja2 template for HTML rendering", default="calendar.j2"
    )
    parser.add_argument(
        "-o", "--output", help="HTML output file name", default="index.html"
    )
    parser.add_argument(
        "--first-month",
        help="starts year at month id (between 1 and 12)",
        type=valid_month,
        default=1,
    )
    return parser.parse_args()


def write_output_html(path: str, html: str):
    """Write html to file."""
    with open(path, "wt") as f:
        print(html, file=f)
    print(f"Wrote html to {path}")


def write_output_pdf(path: str, html: str, zoom: float = 1.0):
    """Writes html to pdf using pdfkit."""
    import pdfkit
    import re

    # Remove footer that contains the download to pdf link.
    regex = re.compile("(<footer>.*</footer>)", re.S|re.M)
    match = regex.search(html)
    if match:
        html = html.replace(match.group(1), "")

    # Generate PDF.
    options = {
        "page-size": "A4",
        "encoding": "UTF8",
        "orientation": "Landscape",
        "dpi": 300,
        "background": "",
        # "zoom": zoom,
        "quiet": "",
    }

    pdfkit.from_string(html, path, options=options)
    print(f"Wrote output pdf to {path}", file=sys.stderr)



def main():
    """Console script for care_calendar."""

    args = parse_command_line()

    output_html = args.output
    output_pdf = os.path.join(
        os.path.dirname(output_html), f"calendar-{args.year}.pdf"
    )

    html_template = read_template_jinja(args.template)
    html_comments = read_comments_markdown(args.comments)
    status_list = read_status_yaml(args.holidays)

    cal = care_calendar.Calendar(args.year, first_month=args.first_month)
    cal.status_list = status_list

    html = html_template.render(
        html_legend=cal.format_legend(),
        html_calendar=cal.format_year(),
        html_comments=html_comments,
        this_year=cal.year,
        pdf_name=output_pdf,
    )

    write_output_html(output_html, html)
    write_output_pdf(output_pdf, html)


    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover


from pip import main


import kaloot

import sys

import jinja2
from jinja2.loaders import FileSystemLoader

def read_template_jinja(path: str) -> jinja2.Template:
    """Reads the jinja template for the calendar HTML rendering."""
    with open(path, "rt") as f:
        text = f.read()
    return jinja2.Environment(loader=FileSystemLoader(searchpath=".")).from_string(text)


def main():
    """Main function"""

    cal = kaloot.calendar.MasterCalendar()
    # cal.render()

    html_template_path = "calendar.j2"
    html_template = read_template_jinja(html_template_path)

    html = html_template.render(
    #     html_legend=cal.format_legend(),
        html_calendar=cal.render(),
    #     html_comments=html_comments,
    #     this_year=cal.year,
    #     pdf_name=output_pdf,
    )

    print(html)





    # sundays = kaloot.calendar.Calendar().month_sundays(1)
    # print(cal.format_week(sundays))



    # import timeit
    # N = 100000
    # setup = "import kaloot; master = kaloot.calendar.Calendar()"
    # print(timeit.timeit("for _ in master.iter_month_dates(1): pass", setup=setup, number=N))
    # print(timeit.timeit("for _ in master.iter_month_dates2(1): pass", setup=setup, number=N))



if __name__ == "__main__":
    sys.exit(main())

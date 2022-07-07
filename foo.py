
from pip import main


import kaloot

import sys

import jinja2


def main():
    """Main function"""

    env = jinja2.Environment(
        loader=jinja2.loaders.FileSystemLoader(searchpath="templates"),
    )

    cal = kaloot.calendar.MasterCalendar(env)

    template = env.get_template("master.j2")
    html = template.render(
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

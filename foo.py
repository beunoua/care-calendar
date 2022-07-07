
import kaloot

import sys

import jinja2


def main():
    """Main function"""

    import datetime
    start = kaloot.date.date(2022, 7, 8)
    end = start + datetime.timedelta(days=7)

    env = jinja2.Environment(
        loader=jinja2.loaders.FileSystemLoader(searchpath="templates"),
    )

    holidays = kaloot.event.read_event_yaml("holidays-2022.yaml")

    cal = kaloot.calendar.MasterCalendar(env)
    cal.features.append(kaloot.feature.EventCollectionFeatureMerge(holidays))

    template = env.get_template("master.j2")
    html = template.render(
    #     html_legend=cal.format_legend(),
        html_calendar=cal.render(),
    #     html_comments=html_comments,
    #     this_year=cal.year,
    #     pdf_name=output_pdf,
    )

    # print(html)


if __name__ == "__main__":
    sys.exit(main())

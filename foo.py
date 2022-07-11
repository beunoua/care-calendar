

from datetime import timedelta
from turtle import pu
import kaloot

import sys

import jinja2



def read_holidays(path: str) -> kaloot.event.Event:
    event_list = kaloot.event.read_event_yaml(path)
    assert len(event_list) == 1
    return event_list[0]

def main():
    """Main function"""
    env = jinja2.Environment(
        loader=jinja2.loaders.FileSystemLoader(searchpath="templates"),
    )

    holidays = read_holidays("holidays-2022.yaml")
    public_holidays = kaloot.event.public_holidays("férié", "férié")
    all_holidays = kaloot.feature.merge([holidays, public_holidays])


    cal = kaloot.MasterCalendar(env)
    cal.features.append(all_holidays)

    template = env.get_template("index.html")
    html = template.render(
    #     html_legend=cal.format_legend(),
        html_calendar=cal.render(),
    #     html_comments=html_comments,
    #     this_year=cal.year,
    #     pdf_name=output_pdf,
    )

    print(html)


if __name__ == "__main__":
    sys.exit(main())

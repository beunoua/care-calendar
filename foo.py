
import kaloot

import sys

import jinja2


def main():
    """Main function"""
    env = jinja2.Environment(
        loader=jinja2.loaders.FileSystemLoader(searchpath="templates"),
        trim_blocks = True,lstrip_blocks = True
    )

    user_events = kaloot.event.read_event_yaml("holidays-2022.yaml")

    public_holidays = kaloot.event.public_holidays()
    school_holidays = user_events["Vacances scolaires"]

    features = [
        kaloot.feature.merge([school_holidays, public_holidays]),
        kaloot.feature.CustodyFeature(school_holidays),
        kaloot.feature.EventCollectionFeature(user_events["Courses"]),
    ]

    cal = kaloot.MasterCalendar(env, features=features)


    template = env.get_template("index.html.j2")
    html = template.render(
        # html_legend=cal.format_legend(),
        html_calendar=cal.render(),
        # html_comments=html_comments,
        this_year=cal.year,
        # pdf_name=output_pdf,
    )

    print(html)


if __name__ == "__main__":
    sys.exit(main())


import argparse
import pathlib
import sys

import kaloot


def parse_args() -> argparse.Namespace:
    """Parse command line arguments"""
    def valid_file(path: str):
        path_ = pathlib.Path(path)
        if not path_.exists():
            raise argparse.ArgumentTypeError(f"File '{path_}' does not exist")
        if not path_.is_file():
            raise argparse.ArgumentTypeError(f"'{path_}' is not a valid file")
        return path_

    def valid_directory(path: str):
        path_ = pathlib.Path(path)
        if not path_.exists():
            raise argparse.ArgumentTypeError(f"Directory '{path_}' does not exist")
        if not path_.is_dir():
            raise argparse.ArgumentTypeError(f"'{path_}' is not a valid directory")
        return path_

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--year",
        type=int,
        default=kaloot.date.current_year(),
        help="The year to generate the calendar for")
    parser.add_argument(
        "holidays",
        help="The YAML file containing the school holidays",
        type=valid_file,
    )
    parser.add_argument(
        "--comments",
        help="The Markdown file containing the comments",
        type=valid_file,
        default="comments.md",
    )
    parser.add_argument(
        "--template-search-path",
        help="The path to the Jinja2 templates",
        type=valid_directory,
        default="templates",
    )
    parser.add_argument(
        "-o", "--output",
        help="The output HTML calendar file",
        type=pathlib.Path,
    )

    args = parser.parse_args()
    if args.output is None:
        args.output = pathlib.Path(f"calendar-{args.year}.html")

    return args



def main():
    """Main function"""
    args = parse_args()

    user_events = kaloot.io.read_user_events(args.holidays)
    html_comments = kaloot.io.read_comments_markdown(args.comments)

    public_holidays = kaloot.event.get_public_holidays(args.year)
    school_holidays = user_events["Vacances scolaires"]

    html = kaloot.html.render(
        template_search_path=args.template_search_path,
        public_holidays=public_holidays,
        school_holidays=school_holidays,
        comments=html_comments)

    kaloot.io.write_html(args.output, html)
    print("Wrote calendar to", args.output)


if __name__ == "__main__":
    sys.exit(main())

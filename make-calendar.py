import argparse
import pathlib
import sys

import kaloot


def parse_args() -> argparse.Namespace:
    """Parse command line arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="The configuration file", type=pathlib.Path)
    parser.add_argument(
        "-o",
        "--output",
        help="The output HTML calendar file",
        type=pathlib.Path,
    )
    args = parser.parse_args()
    kaloot.io.check_file_exists(args.config)
    return args


def main():
    """Main function"""
    args = parse_args()
    config = kaloot.io.read_configuration_file(args.config)

    cal = kaloot.html.create_calendar(config)
    html = cal.render()

    output_path = args.output or pathlib.Path(f"calendar-{config.year}.html")
    kaloot.io.write_html(output_path, html)
    print("Wrote calendar to", output_path)


if __name__ == "__main__":
    sys.exit(main())

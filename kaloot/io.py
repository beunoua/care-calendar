"""kaloot.io - Defines kaloot's input/output functions."""

import os
import pathlib
from typing import Optional

import markdown
import yaml

from .event import Event
from .config import UserConfiguration

def read_user_events(path: os.PathLike) -> dict[str, Event]:
    """Reads user events from a YAML file"""
    user_events = read_event_yaml(path)
    if len(user_events) == 0:
        raise ValueError("No user events found")
    if len(user_events) > 1:
        raise ValueError("Only one event is supported")
    if "Vacances scolaires" not in user_events:
        raise KeyError("Missing 'Vacances scolaires' in holiday file")
    return user_events


def read_comments_markdown(path: Optional[os.PathLike]) -> str:
    """Reads the markdown comment file.

    Returns the comments formatted in HTML.
    """
    if path is None:
        return ""
    check_file_exists(path)
    with open(path, "rt", encoding="utf-8") as input_file:
        text = input_file.read()
    return markdown.markdown(text)


def read_event_yaml(path: os.PathLike) -> dict[str, Event]:
    """Reads a yaml file containing events and dates (or date ranges) for each event."""

    with open(path, "rt", encoding="utf-8") as input_file:
        data = yaml.load(input_file, Loader=yaml.Loader)

    events = {}
    for data in data.items():
        event = Event.from_yaml(data)
        events[event.name] = event
    return events


def read_configuration_file(path: os.PathLike) -> UserConfiguration:
    """Reads the YAML configuration file"""
    with open(path, "rt", encoding="utf-8") as input_file:
        config = yaml.load(input_file, Loader=yaml.Loader)

    if "year" not in config:
        raise KeyError("Missing 'year' in configuration file")

    if "Vacances scolaires" not in config:
        raise KeyError("Missing 'Vacances scolaires' in configuration file")

    # If the template search path is not specified, use the default.
    if "template_dir" not in config:
        config["template_dir"] = "templates"
    check_directory_exists(config["template_dir"])

    config["comments_html"] = read_comments_markdown(config.get("comments"))

    # Store school holidays into config["school_holidays"].
    config["school_holidays"] = Event.from_yaml(
        name="Vacances scolaires",
        year=config["year"],
        event_data=config["Vacances scolaires"],
    )

    return UserConfiguration(
        year=config["year"],
        template_search_path=config["template_dir"],
        comments_html=config["comments_html"],
        school_holidays=config["school_holidays"],
)


def write_html(path: os.PathLike, html: str):
    """Writes the HTML calendar to a file."""
    with open(path, "wt", encoding="utf-8") as output_file:
        output_file.write(html)


def check_file_exists(path: os.PathLike):
    """Checks if a file exists and is a file."""
    path_ = pathlib.Path(path)
    if not path_.exists():
        raise FileNotFoundError(f"File '{path_}' does not exist")
    if not path_.is_file():
        raise FileNotFoundError(f"'{path_}' is not a valid file")


def check_directory_exists(path: os.PathLike):
    path_ = pathlib.Path(path)
    if not path_.exists():
        raise FileNotFoundError(f"Directory '{path_}' does not exist")
    if not path_.is_dir():
        raise NotADirectoryError(f"'{path_}' is not a valid directory")
    return path_
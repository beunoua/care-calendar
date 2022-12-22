"""kaloot.io - Defines kaloot's input/output functions."""

import os

import markdown
import yaml

from .event import Event


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


def read_comments_markdown(path: os.PathLike) -> str:
    """Reads the markdown comment file.

    Returns the comments formatted in HTML.
    """
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


def write_html(path: os.PathLike, html: str):
    """Writes the HTML calendar to a file."""
    with open(path, "wt", encoding="utf-8") as output_file:
        output_file.write(html)

"""Defines kaloot's input/output functions."""

import os
from typing import Optional

import markdown
import yaml

from .event import Event


def read_user_events(path: os.PathLike) -> dict[str, Event]:
    """Read user events from a YAML file"""
    user_events = read_event_yaml(path)
    if len(user_events) == 0:
        raise ValueError("No user events found")
    if len(user_events) > 1:
        raise ValueError("Only one event is supported")
    if "Vacances scolaires" not in user_events:
        raise KeyError("Missing 'Vacances scolaires' in holiday file")
    return user_events


def read_comments_markdown(path: os.PathLike) -> str:
    """Read the markdown comment file.

    Returns the comments formatted in HTML.
    """
    with open(path, "rt") as f:
        text = f.read()
    return markdown.markdown(text)


def read_event_yaml(path: os.PathLike, year: Optional[int] = None) -> dict[str, Event]:
    """Reads a yaml file containing events and dates (or date ranges) for each event."""

    with open(path, "rt") as f:
        data = yaml.load(f, Loader=yaml.Loader)

    events = {}
    for data in data.items():
        e = Event.from_yaml(data)
        events[e.name] = e
    return events


def write_html(path: os.PathLike, html: str):
    """Writes the HTML calendar to a file."""
    with open(path, "wt") as f:
        f.write(html)
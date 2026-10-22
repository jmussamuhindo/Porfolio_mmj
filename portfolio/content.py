"""Loads site content from the JSON files in /data.

Keeping content in JSON means you can update your bio, projects and skills
without touching any Python or HTML.
"""
import json
from functools import lru_cache
from pathlib import Path

from flask import current_app


def _read(name: str):
    path: Path = current_app.config["DATA_DIR"] / f"{name}.json"
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def get_profile() -> dict:
    return _read("profile")


def get_projects() -> list[dict]:
    projects = _read("projects")
    # Featured projects first, then keep the file's order.
    return sorted(projects, key=lambda p: not p.get("featured", False))


def get_project(slug: str) -> dict | None:
    return next((p for p in _read("projects") if p["slug"] == slug), None)


def get_skills() -> list[dict]:
    return _read("skills")


def get_experience() -> list[dict]:
    return _read("experience")


# Order in which article statuses are listed (and their display colour key).
ARTICLE_STATUS_ORDER = ["published", "accepted", "presented", "under review", "submitted", "in progress"]


def get_articles() -> list[dict]:
    articles = _read("articles")
    def key(a):
        status = a.get("status", "in progress").lower()
        rank = ARTICLE_STATUS_ORDER.index(status) if status in ARTICLE_STATUS_ORDER else 99
        return (-a.get("year", 0), rank)
    return sorted(articles, key=key)

"""Private admin panel — local only.

Runs when you start the app on your own machine (python app.py) and is never
part of the published static site. It edits the JSON files in /data directly;
after saving, commit and push to publish.
"""
import json
import re
from pathlib import Path

from flask import Blueprint, abort, current_app, flash, redirect, render_template, request, url_for

from . import content

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

ARTICLE_STATUSES = ["in progress", "submitted", "under review", "accepted", "presented", "published"]
ARTICLE_TYPES = ["Journal article", "Conference talk", "Conference paper", "Data paper", "Preprint", "Poster", "Book chapter", "Thesis"]


@admin_bp.before_request
def local_only():
    """Refuse anything that is not coming from this machine."""
    if request.remote_addr not in ("127.0.0.1", "::1"):
        abort(403)


# ---------- helpers ----------

def _path(name: str) -> Path:
    return current_app.config["DATA_DIR"] / f"{name}.json"


def _load(name: str) -> list:
    return json.loads(_path(name).read_text(encoding="utf-8"))


def _save(name: str, data: list) -> None:
    _path(name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _slugify(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s or "project"


def _lines(text: str) -> list[str]:
    return [ln.strip() for ln in text.splitlines() if ln.strip()]


def _csv(text: str) -> list[str]:
    return [t.strip() for t in text.split(",") if t.strip()]


def _blank(v: str):
    return v.strip() or None


# ---------- dashboard ----------

@admin_bp.route("/")
def index():
    return render_template(
        "admin/index.html",
        profile=content.get_profile(),
        articles=_load("articles"),
        projects=_load("projects"),
    )


# ---------- articles ----------

def _article_from_form(f) -> dict:
    return {
        "title": f.get("title", "").strip(),
        "authors": f.get("authors", "").strip(),
        "venue": f.get("venue", "").strip(),
        "year": int(f.get("year") or 0),
        "type": f.get("type", "").strip(),
        "status": f.get("status", "in progress").strip().lower(),
        "abstract": f.get("abstract", "").strip(),
        "link": _blank(f.get("link", "")),
    }


@admin_bp.route("/articles/new", methods=["GET", "POST"])
def article_new():
    if request.method == "POST":
        a = _article_from_form(request.form)
        if not a["title"]:
            flash("Title is required.", "error")
        else:
            data = _load("articles")
            data.insert(0, a)
            _save("articles", data)
            flash("Article added. Commit and push to publish.", "success")
            return redirect(url_for("admin.index"))
    return render_template("admin/article_form.html", profile=content.get_profile(),
                           article={}, idx=None, statuses=ARTICLE_STATUSES, types=ARTICLE_TYPES)


@admin_bp.route("/articles/<int:idx>/edit", methods=["GET", "POST"])
def article_edit(idx):
    data = _load("articles")
    if idx < 0 or idx >= len(data):
        abort(404)
    if request.method == "POST":
        a = _article_from_form(request.form)
        if not a["title"]:
            flash("Title is required.", "error")
        else:
            data[idx] = a
            _save("articles", data)
            flash("Article saved. Commit and push to publish.", "success")
            return redirect(url_for("admin.index"))
    return render_template("admin/article_form.html", profile=content.get_profile(),
                           article=data[idx], idx=idx, statuses=ARTICLE_STATUSES, types=ARTICLE_TYPES)


@admin_bp.route("/articles/<int:idx>/delete", methods=["POST"])
def article_delete(idx):
    data = _load("articles")
    if 0 <= idx < len(data):
        removed = data.pop(idx)
        _save("articles", data)
        flash(f"Deleted “{removed['title']}”.", "success")
    return redirect(url_for("admin.index"))


# ---------- projects ----------

def _project_from_form(f, existing: dict | None = None) -> dict:
    title = f.get("title", "").strip()
    slug = f.get("slug", "").strip() or (existing or {}).get("slug") or _slugify(title)
    return {
        "slug": _slugify(slug),
        "title": title,
        "summary": f.get("summary", "").strip(),
        "description": f.get("description", "").strip(),
        "highlights": _lines(f.get("highlights", "")),
        "tags": _csv(f.get("tags", "")),
        "year": int(f.get("year") or 0),
        "featured": f.get("featured") == "on",
        "repo": _blank(f.get("repo", "")),
        "demo": _blank(f.get("demo", "")),
        "accent": f.get("accent", "").strip() or "#6d4aff",
    }


@admin_bp.route("/projects/new", methods=["GET", "POST"])
def project_new():
    if request.method == "POST":
        p = _project_from_form(request.form)
        data = _load("projects")
        if not p["title"]:
            flash("Title is required.", "error")
        elif any(x["slug"] == p["slug"] for x in data):
            flash(f"A project with slug “{p['slug']}” already exists.", "error")
        else:
            data.insert(0, p)
            _save("projects", data)
            flash("Project added. Commit and push to publish.", "success")
            return redirect(url_for("admin.index"))
    return render_template("admin/project_form.html", profile=content.get_profile(), project={}, idx=None)


@admin_bp.route("/projects/<int:idx>/edit", methods=["GET", "POST"])
def project_edit(idx):
    data = _load("projects")
    if idx < 0 or idx >= len(data):
        abort(404)
    if request.method == "POST":
        p = _project_from_form(request.form, data[idx])
        if not p["title"]:
            flash("Title is required.", "error")
        elif any(i != idx and x["slug"] == p["slug"] for i, x in enumerate(data)):
            flash(f"A project with slug “{p['slug']}” already exists.", "error")
        else:
            data[idx] = p
            _save("projects", data)
            flash("Project saved. Commit and push to publish.", "success")
            return redirect(url_for("admin.index"))
    return render_template("admin/project_form.html", profile=content.get_profile(), project=data[idx], idx=idx)


@admin_bp.route("/projects/<int:idx>/delete", methods=["POST"])
def project_delete(idx):
    data = _load("projects")
    if 0 <= idx < len(data):
        removed = data.pop(idx)
        _save("projects", data)
        flash(f"Deleted “{removed['title']}”.", "success")
    return redirect(url_for("admin.index"))

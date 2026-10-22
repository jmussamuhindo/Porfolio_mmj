"""URL routes for the site."""
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

from . import content

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    return render_template(
        "index.html",
        profile=content.get_profile(),
        projects=content.get_projects()[:3],
        skills=content.get_skills(),
        experience=content.get_experience(),
        articles=content.get_articles()[:3],
    )


@main_bp.route("/publications")
def publications():
    return render_template(
        "publications.html",
        profile=content.get_profile(),
        articles=content.get_articles(),
    )


@main_bp.route("/projects")
def projects():
    return render_template(
        "projects.html",
        profile=content.get_profile(),
        projects=content.get_projects(),
    )


@main_bp.route("/projects/<slug>")
def project_detail(slug):
    project = content.get_project(slug)
    if project is None:
        abort(404)
    return render_template("project.html", profile=content.get_profile(), project=project)


@main_bp.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()
        if not (name and email and message):
            flash("Please fill in every field.", "error")
        else:
            # Hook up an email service or database here. For now we just log it.
            print(f"[contact] {name} <{email}>: {message}")
            flash("Thanks! Your message has been sent.", "success")
            return redirect(url_for("main.contact"))
    return render_template("contact.html", profile=content.get_profile())


@main_bp.app_errorhandler(404)
def not_found(_):
    return render_template("404.html", profile=content.get_profile()), 404

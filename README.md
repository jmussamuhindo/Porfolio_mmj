# Portfolio

A personal portfolio website built with Flask. Content lives in JSON files, so you can update it without touching code.

## Run it

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000.

## Project structure

```
portfolio/
├── app.py                 # Entry point
├── requirements.txt
├── data/                  # ← Edit these to change your content
│   ├── profile.json       # Name, bio, links, stats
│   ├── projects.json      # Your projects
│   ├── articles.json      # Publications & papers in progress (with status)
│   ├── skills.json        # Skill groups
│   └── experience.json    # Timeline (jobs, education)
├── portfolio/             # Flask package
│   ├── __init__.py        # create_app() factory
│   ├── config.py          # Settings
│   ├── content.py         # Loads the JSON data
│   ├── routes.py          # URL routes
│   ├── templates/         # Jinja2 HTML templates
│   │   ├── base.html      # Shared layout (nav, footer)
│   │   ├── index.html     # Home: hero, about, projects, experience
│   │   ├── projects.html  # All projects, with tag filter
│   │   ├── publications.html  # Articles, filterable by status
│   │   ├── project.html   # Single project page
│   │   ├── contact.html   # Contact form
│   │   ├── 404.html
│   │   ├── _project_card.html  # Reusable card partial
│   │   └── _article.html  # Reusable publication row
│   └── static/
│       ├── css/style.css  # All styles; colours/fonts at the top in :root
│       ├── js/main.js     # Mobile nav, scroll reveal, project filter
│       └── img/           # Put images here
└── tests/test_routes.py   # Run with: pytest
```

## Customising

- **Your info** – edit `data/profile.json`.
- **Add a project** – add an object to `data/projects.json`. `slug` becomes the URL (`/projects/<slug>`); `accent` is the card's colour; `featured: true` shows it on the home page.
- **Add an article** – add an object to `data/articles.json`. `status` can be `in progress`, `submitted`, `under review`, `accepted`, `presented` or `published` (it controls the colour of the tag). Set `link` to a DOI or PDF URL once it's public.
- **Colours & fonts** – change the variables at the top of `static/css/style.css`.
- **Contact form** – `routes.py` currently just prints submissions. Hook in Flask-Mail, a database, or a service like Formspree there.

## Deploying for free on Render

1. Push this folder to a GitHub repository.
2. Go to https://render.com, sign in with GitHub, click **New → Blueprint** and pick the repo. Render reads `render.yaml` and sets everything up (gunicorn, `FLASK_DEBUG=0`, a generated `SECRET_KEY`).
3. Click **Apply**. The first build takes a couple of minutes; after that every `git push` redeploys automatically.

Your site will be live at `https://portfolio-xxxx.onrender.com`. You can add a custom domain for free under the service's Settings → Custom Domains.

Note: free Render services spin down after 15 minutes of no traffic and take ~1 minute to wake on the next visit.

**Alternatives:** `Procfile` is included for Railway or any Heroku-style host. For PythonAnywhere (always-on free tier), upload the folder, create a Flask web app pointing at `app.py`, and set the WSGI file's `application = app`.

Local development still runs with `FLASK_DEBUG=1 python app.py` (debug is off by default now).

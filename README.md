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
│   ├── experience.json    # Work timeline
│   └── education.json     # Degrees
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

## Editing content — the hidden admin page

Open **https://mmj.ink/admin** (there is no link to it anywhere on the site). Sign in with a GitHub token and you can add, edit and delete publications (with links) and projects through forms. Clicking **Publish to site** commits the changes to this repository; GitHub rebuilds the site about a minute later.

**Create the token once:** github.com → Settings → Developer settings → Personal access tokens → Fine-grained tokens → Generate new token. Repository access: *Only select repositories* → this repo. Permissions: *Contents → Read and write*. Copy the token (it is shown only once) and keep it like a password. Tick "Stay signed in" on the admin page if you don't want to paste it every time.

The same page also works locally at http://127.0.0.1:8000/admin when running `python app.py`.

## Customising

- **Your info** – edit `data/profile.json`.
- **Add a project** – add an object to `data/projects.json`. `slug` becomes the URL (`/projects/<slug>`); `accent` is the card's colour; `featured: true` shows it on the home page.
- **Add an article** – add an object to `data/articles.json`. `status` can be `in progress`, `submitted`, `under review`, `accepted`, `presented` or `published` (it controls the colour of the tag). Set `link` to a DOI or PDF URL once it's public.
- **Colours & fonts** – change the variables at the top of `static/css/style.css`.
- **Contact form** – `routes.py` currently just prints submissions. Hook in Flask-Mail, a database, or a service like Formspree there.

## Hosting for free

### Option A — GitHub Pages (recommended: free, no card, never sleeps)

The site has no database, so it can be published as plain HTML.

1. Create a GitHub repository named **`<your-username>.github.io`** (that exact name makes it serve at the root URL). Push this folder to it.
2. In the repo, open **Settings → Pages** and set *Source* to **GitHub Actions**.
3. That's it. The workflow in `.github/workflows/pages.yml` builds the site (`python build_static.py`) and publishes it on every push. Your site is at `https://<your-username>.github.io`.

**Custom domain (e.g. `yourname.com`):**
1. Buy the domain (Cloudflare Registrar or Porkbun are cheapest, ~$11/year for .com, renewal at the same price).
2. Write the domain into the `CNAME` file in this folder (one line, no `https://`, no `www`) and push.
3. At your registrar add these DNS records:
   - `A` records for `@` pointing to `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - `CNAME` record for `www` pointing to `<your-username>.github.io`
4. In GitHub **Settings → Pages** enter the domain under *Custom domain*, wait for the DNS check, then tick **Enforce HTTPS**.
DNS can take from minutes to a few hours to propagate.

Contact form on a static site: sign up at https://formspree.io (free), create a form, and paste its endpoint into `"form_endpoint"` in `data/profile.json`. Leave it empty when running the Flask server locally.

To preview the static build locally: `python build_static.py && python -m http.server -d dist 8000`.

### Option B — PythonAnywhere (free, runs the Flask app)

One free web app at `<username>.pythonanywhere.com`; you have to click "Run until" roughly monthly to keep it alive. Upload the folder, create a Flask web app, and point the WSGI file at `app.py` (`from app import app as application`).

### Option C — Render / Railway (Flask app, Procfile and render.yaml included)

`gunicorn app:app` is the start command. Render's free services sleep after 15 minutes idle.

Local development runs with `FLASK_DEBUG=1 python app.py` (debug is off by default).

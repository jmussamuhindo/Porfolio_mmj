"""Render the whole site to static HTML in ./dist (for GitHub Pages, Netlify, etc.).

Usage:  python build_static.py
"""
import shutil
from pathlib import Path

from portfolio import create_app
from portfolio import content

OUT = Path(__file__).parent / "dist"


def main() -> None:
    app = create_app()
    app.config["STATIC_BUILD"] = True

    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()

    with app.app_context():
        pages = {
            "index.html": "/",
            "projects/index.html": "/projects",
            "publications/index.html": "/publications",
            "contact/index.html": "/contact",
            "404.html": "/this-page-does-not-exist",
            "admin/index.html": "/admin",
        }
        for p in content.get_projects():
            pages[f"projects/{p['slug']}/index.html"] = f"/projects/{p['slug']}"

    client = app.test_client()
    for out_name, url in pages.items():
        resp = client.get(url)
        if resp.status_code not in (200, 404):
            raise SystemExit(f"{url} returned {resp.status_code}")
        target = OUT / out_name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(resp.data)
        print(f"  {url:40s} -> {out_name}")

    shutil.copytree(Path(app.static_folder), OUT / "static")
    (OUT / ".nojekyll").touch()  # tell GitHub Pages not to run Jekyll

    # Custom domain: put your domain (e.g. "mussamuhindo.com") in a file named
    # CNAME next to this script and GitHub Pages will serve the site on it.
    cname = Path(__file__).parent / "CNAME"
    if cname.exists():
        shutil.copy(cname, OUT / "CNAME")
        print(f"  custom domain: {cname.read_text().strip()}")
    print(f"\nBuilt {len(pages)} pages into {OUT}")


if __name__ == "__main__":
    main()

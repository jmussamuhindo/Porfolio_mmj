import pytest
from portfolio import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


def test_index(client):
    r = client.get("/")
    assert r.status_code == 200
    assert b"Featured projects" in r.data


def test_projects_list(client):
    r = client.get("/projects")
    assert r.status_code == 200
    assert b"Neural CDEs" in r.data


def test_project_detail(client):
    assert client.get("/projects/malaria-neural-cde").status_code == 200
    assert client.get("/projects/does-not-exist").status_code == 404


def test_contact_form(client):
    r = client.post("/contact", data={"name": "A", "email": "a@b.c", "message": "hi"}, follow_redirects=True)
    assert b"Thanks" in r.data
    r = client.post("/contact", data={"name": "", "email": "", "message": ""})
    assert b"fill in every field" in r.data


def test_publications(client):
    r = client.get("/publications")
    assert r.status_code == 200
    assert b"in progress" in r.data

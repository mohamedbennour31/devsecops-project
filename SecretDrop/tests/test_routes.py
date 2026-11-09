import pytest
from run import create_app


@pytest.fixture
def client(tmp_path):
    app = create_app({
        "TESTING": True,
        "WTF_CSRF_ENABLED": True,
        "UPLOAD_FOLDER": str(tmp_path),
        "SECRET_KEY": "test-secret",
    })

    with app.test_client() as client:
        yield client


def test_homepage_returns_200(client):
    response = client.get("/")
    assert response.status_code == 200


def test_invalid_share_returns_404(client):
    response = client.get("/share/invalid")
    assert response.status_code == 404


def test_invalid_download_returns_404(client):
    response = client.get("/download/invalid")
    assert response.status_code == 404


def test_upload_rejects_missing_csrf_token(client):
    response = client.post("/upload", data={})
    assert response.status_code == 400


def test_download_from_link_rejects_missing_csrf_token(client):
    response = client.post(
        "/download-from-link",
        data={"share_url": "http://127.0.0.1:5000/share/test"}
    )
    assert response.status_code == 400

import os
import secrets
from pathlib import Path

from flask import Flask
from flask_wtf.csrf import CSRFProtect


def create_app(test_config=None):
    app = Flask(__name__, template_folder="app/templates", static_folder="app/static")

    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY") or secrets.token_hex(32),
        PUBLIC_BASE_URL=os.environ.get(
            "PUBLIC_BASE_URL",
            "http://127.0.0.1:5000"
        ),
        MAX_CONTENT_LENGTH=10 * 1024 * 1024,
        UPLOAD_FOLDER=str(Path(app.root_path) / "uploads"),
    )

    if test_config:
        app.config.update(test_config)

    CSRFProtect(app)

    Path(app.config["UPLOAD_FOLDER"]).mkdir(
        parents=True,
        exist_ok=True,
    )

    from app.routes import main
    app.register_blueprint(main)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


import os
import secrets
from pathlib import Path

from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY") or secrets.token_hex(32),
        MAX_CONTENT_LENGTH=10 * 1024 * 1024,
        UPLOAD_FOLDER=str(Path(app.root_path) / "uploads"),
    )

    if test_config:
        app.config.update(test_config)

    Path(app.config["UPLOAD_FOLDER"]).mkdir(
        parents=True,
        exist_ok=True,
    )

    from app.routes import main
    app.register_blueprint(main)

    return app

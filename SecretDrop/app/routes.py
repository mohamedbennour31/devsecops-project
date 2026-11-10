import re
import time
import secrets
from pathlib import Path
from urllib.parse import urlparse

from flask import (
    Blueprint,
    abort,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.utils import secure_filename

main = Blueprint("main", __name__)


@main.route("/health", methods=["GET"])
def health():
    return {"status": "healthy"}, 200


ALLOWED_EXTENSIONS = {
    "pdf",
    "doc",
    "docx",
    "txt",
    "csv",
    "xls",
    "xlsx",
    "ppt",
    "pptx",
    "png",
    "jpg",
    "jpeg",
    "gif",
    "webp",
}

FILE_ID_PATTERN = re.compile(r"[A-Za-z0-9_-]{20,30}\Z")


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def cleanup_expired_files():
    upload_dir = Path(current_app.config["UPLOAD_FOLDER"])

    # Production: expire files after 24 hours
    expiration_seconds = 24 * 60 * 60
    now = time.time()

    for path in upload_dir.iterdir():
        if not path.is_file():
            continue

        try:
            if now - path.stat().st_mtime >= expiration_seconds:
                path.unlink()
                current_app.logger.info("Deleted expired file: %s", path.name)
        except OSError:
            current_app.logger.exception("Could not remove expired file: %s", path.name)


def find_uploaded_file(file_id):
    cleanup_expired_files()

    if not FILE_ID_PATTERN.fullmatch(file_id):
        return None

    upload_dir = Path(current_app.config["UPLOAD_FOLDER"])

    matches = [
        path
        for path in upload_dir.iterdir()
        if path.is_file()
        and path.stem == file_id
        and path.suffix.lower().lstrip(".") in ALLOWED_EXTENSIONS
    ]

    return matches[0] if len(matches) == 1 else None


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        flash("Please choose a file to upload.", "error")
        return redirect(url_for("main.index"))

    file = request.files["file"]

    if not file.filename or not file.filename.strip():
        flash("Please choose a file to upload.", "error")
        return redirect(url_for("main.index"))

    if not allowed_file(file.filename):
        flash("File type not allowed. Upload a document or image.", "error")
        return redirect(url_for("main.index"))

    safe_name = secure_filename(file.filename)
    extension = Path(safe_name).suffix.lower()

    if not safe_name or not extension:
        flash("Invalid filename.", "error")
        return redirect(url_for("main.index"))

    upload_dir = Path(current_app.config["UPLOAD_FOLDER"])
    upload_dir.mkdir(parents=True, exist_ok=True)

    while True:
        file_id = secrets.token_urlsafe(16)
        destination = upload_dir / f"{file_id}{extension}"

        try:
            with destination.open("xb") as output:
                file.save(output)
            break
        except FileExistsError:
            continue
        except OSError:
            current_app.logger.exception("Could not save uploaded file")
            flash("The file could not be saved. Please try again.", "error")
            return redirect(url_for("main.index"))

    return redirect(url_for("main.share_file", file_id=file_id))


@main.app_errorhandler(RequestEntityTooLarge)
def handle_file_too_large(error):
    flash("File is too large. Maximum allowed size is 10 MB.", "error")
    return redirect(url_for("main.index"))


@main.route("/share/<file_id>")
def share_file(file_id):
    stored_file = find_uploaded_file(file_id)

    if stored_file is None:
        abort(404)

    share_url = (
        f"{current_app.config['PUBLIC_BASE_URL'].rstrip('/')}"
        f"{url_for('main.share_file', file_id=file_id)}"
    )

    return render_template(
        "index.html",
        share_url=share_url,
        file_id=file_id,
    )


@main.route("/download/<file_id>")
def download_file(file_id):
    stored_file = find_uploaded_file(file_id)

    if stored_file is None:
        abort(404)

    return send_from_directory(
        str(stored_file.parent),
        stored_file.name,
        as_attachment=True,
    )


@main.route("/download-from-link", methods=["POST"])
def download_from_link():
    share_url = request.form.get("share_url", "").strip()

    if not share_url:
        flash("Please enter a share link.", "error")
        return redirect(url_for("main.index"))

    parsed = urlparse(share_url)

    # Accept only local links for this running application.
    expected_host = request.host.lower()

    if (
        parsed.scheme not in ("http", "https")
        or not parsed.netloc
        or parsed.netloc.lower() != expected_host
        or parsed.username is not None
        or parsed.password is not None
        or parsed.query
        or parsed.fragment
    ):
        flash("Please enter a valid SecretDrop share link.", "error")
        return redirect(url_for("main.index"))

    match = re.fullmatch(r"/share/([A-Za-z0-9_-]{20,30})", parsed.path)

    if not match:
        flash("Invalid SecretDrop share link.", "error")
        return redirect(url_for("main.index"))

    file_id = match.group(1)

    if find_uploaded_file(file_id) is None:
        flash("The shared file does not exist.", "error")
        return redirect(url_for("main.index"))

    return redirect(url_for("main.download_file", file_id=file_id))

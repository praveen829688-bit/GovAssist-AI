import re
import time
from pathlib import Path

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".png",
    ".jpg",
    ".jpeg",
    ".txt",
    ".docx"
}

MAX_UPLOAD_SIZE = 10 * 1024 * 1024

_suspicious_patterns = [
    r"<script",
    r"javascript:",
    r"onerror\s*=",
    r"onload\s*=",
    r"drop\s+table",
    r"union\s+select",
    r"select\s+.*from",
    r"insert\s+into",
    r"delete\s+from",
    r"update\s+.*set",
]

def sanitize_text(value, max_length=2000):
    if value is None:
        return ""

    value = str(value)

    value = value.replace("\x00", "")

    value = re.sub(r"<script.*?>.*?</script>", "", value,
                   flags=re.IGNORECASE | re.DOTALL)

    value = value.strip()

    return value[:max_length]


def contains_suspicious_input(value):
    if not value:
        return False

    text = str(value).lower()

    for pattern in _suspicious_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True

    return False


def validate_upload(file_name, file_size):
    if not file_name:
        return False, "Missing file name."

    suffix = Path(file_name).suffix.lower()

    if suffix not in ALLOWED_EXTENSIONS:
        return False, "File type is not allowed."

    try:
        size = int(file_size)
    except (TypeError, ValueError):
        return False, "Invalid file size."

    if size <= 0:
        return False, "File is empty."

    if size > MAX_UPLOAD_SIZE:
        return False, "File exceeds the 10 MB upload limit."

    return True, "File is valid."


class RateLimiter:
    """
    Simple in-memory rate limiter.
    Suitable for local/demo use.
    Production deployments should use a shared
    datastore such as Redis.
    """

    def __init__(self, max_requests=20, window_seconds=60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = {}

    def allow(self, key):
        now = time.time()

        history = self.requests.get(key, [])

        history = [
            timestamp
            for timestamp in history
            if now - timestamp < self.window_seconds
        ]

        if len(history) >= self.max_requests:
            self.requests[key] = history
            return False

        history.append(now)
        self.requests[key] = history

        return True


def safe_filename(filename):
    if not filename:
        return "upload"

    name = Path(filename).name

    name = re.sub(
        r"[^A-Za-z0-9._-]",
        "_",
        name
    )

    return name[:150]

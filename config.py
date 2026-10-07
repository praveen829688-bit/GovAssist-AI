import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = "GovAssist AI"

APP_VERSION = "3.0.0"

ENVIRONMENT = os.getenv(
    "ENVIRONMENT",
    "development"
)

OPENAI_MODEL = os.getenv(
    "OPENAI_MODEL",
    "gpt-6-luna"
)

OPENAI_API_KEY = os.getenv(
    "OPENAI_API_KEY",
    ""
).strip()

SUPPORTED_LANGUAGES = [
    "English",
    "Kannada",
    "Hindi",
    "Tamil",
    "Telugu"
]

MAX_UPLOAD_MB = 10

ALLOWED_DOCUMENT_TYPES = [
    "pdf",
    "png",
    "jpg",
    "jpeg",
    "webp",
    "txt"
]

OFFICIAL_PORTALS = [
    "https://www.india.gov.in/",
    "https://www.myscheme.gov.in/",
    "https://www.passportindia.gov.in/",
    "https://www.incometax.gov.in/",
    "https://parivahan.gov.in/",
    "https://scholarships.gov.in/",
    "https://pmkisan.gov.in/",
    "https://pmjay.gov.in/",
    "https://sevasindhu.karnataka.gov.in/"
]


def validate_configuration():

    warnings = []

    if not OPENAI_API_KEY:

        warnings.append(
            "OPENAI_API_KEY is not configured. "
            "GovAssist will use fallback AI mode."
        )

    if not OPENAI_MODEL:

        warnings.append(
            "OPENAI_MODEL is not configured."
        )

    return warnings

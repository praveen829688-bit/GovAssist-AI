import re
from pathlib import Path

try:
    import pytesseract
    from PIL import Image
except ImportError:
    pytesseract = None
    Image = None

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None


DOCUMENT_TYPES = {
    "aadhaar": [
        "aadhaar",
        "uidai",
        "unique identification",
        "government of india"
    ],
    "pan": [
        "income tax department",
        "permanent account number",
        "pan card",
        "pan"
    ],
    "passport": [
        "passport",
        "republic of india",
        "passport number"
    ],
    "income_certificate": [
        "income certificate",
        "annual income",
        "income"
    ],
    "birth_certificate": [
        "birth certificate",
        "date of birth",
        "place of birth"
    ],
    "caste_certificate": [
        "caste certificate",
        "community certificate",
        "caste"
    ],
    "driving_licence": [
        "driving licence",
        "driving license",
        "licence number",
        "license number"
    ],
    "ration_card": [
        "ration card",
        "food and civil supplies",
        "family members"
    ],
    "marks_card": [
        "marks card",
        "marksheet",
        "marks sheet",
        "semester",
        "university"
    ]
}


def extract_text_from_image(file_path):
    if Image is None or pytesseract is None:
        return "", "OCR packages are not installed."

    try:
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image)

        return text.strip(), None

    except Exception as error:
        return "", str(error)


def extract_text_from_pdf(file_path):
    if PdfReader is None:
        return "", "PDF package is not installed."

    try:
        reader = PdfReader(file_path)

        pages = []

        for page in reader.pages:
            text = page.extract_text() or ""
            pages.append(text)

        return "\n".join(pages).strip(), None

    except Exception as error:
        return "", str(error)


def extract_document_text(file_path):
    path = Path(file_path)

    extension = path.suffix.lower()

    if extension in [".png", ".jpg", ".jpeg", ".webp", ".bmp"]:
        return extract_text_from_image(file_path)

    if extension == ".pdf":
        return extract_text_from_pdf(file_path)

    if extension in [".txt", ".md"]:
        try:
            return path.read_text(encoding="utf-8"), None
        except Exception as error:
            return "", str(error)

    return "", f"Unsupported file type: {extension}"


def detect_document_type(text):
    text_lower = text.lower()

    scores = {}

    for document_type, keywords in DOCUMENT_TYPES.items():
        score = 0

        for keyword in keywords:
            if keyword in text_lower:
                score += 1

        scores[document_type] = score

    best_type = max(scores, key=scores.get)

    if scores[best_type] == 0:
        return "unknown", 0

    return best_type, scores[best_type]


def detect_sensitive_information(text):
    findings = []

    patterns = {
        "Aadhaar-like number": r"\b\d{4}\s?\d{4}\s?\d{4}\b",
        "PAN-like number": r"\b[A-Z]{5}[0-9]{4}[A-Z]\b",
        "Phone number": r"\b[6-9]\d{9}\b",
        "Email address": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    }

    for label, pattern in patterns.items():
        matches = re.findall(pattern, text)

        if matches:
            findings.append({
                "type": label,
                "count": len(matches)
            })

    return findings


def mask_sensitive_information(text):
    masked = text

    masked = re.sub(
        r"\b\d{4}\s?\d{4}\s?\d{4}\b",
        "[AADHAAR REDACTED]",
        masked
    )

    masked = re.sub(
        r"\b[A-Z]{5}[0-9]{4}[A-Z]\b",
        "[PAN REDACTED]",
        masked
    )

    masked = re.sub(
        r"\b[6-9]\d{9}\b",
        "[PHONE REDACTED]",
        masked
    )

    return masked


def get_checklist(document_type):
    checklists = {
        "aadhaar": [
            "Check that the name is readable.",
            "Check that date of birth details are readable.",
            "Verify that the document is not expired or damaged where applicable.",
            "Do not share Aadhaar number publicly."
        ],

        "pan": [
            "Check that the PAN is readable.",
            "Check name and date of birth.",
            "Avoid publicly sharing the PAN number."
        ],

        "passport": [
            "Check name and date of birth.",
            "Check passport number.",
            "Check validity date.",
            "Ensure the document is readable."
        ],

        "income_certificate": [
            "Check applicant name.",
            "Check annual income information.",
            "Check issuing authority.",
            "Check certificate date and validity where applicable."
        ],

        "birth_certificate": [
            "Check name.",
            "Check date of birth.",
            "Check place of birth.",
            "Check registration details."
        ],

        "caste_certificate": [
            "Check applicant name.",
            "Check community/caste details.",
            "Check issuing authority.",
            "Check certificate details and date."
        ],

        "driving_licence": [
            "Check licence holder name.",
            "Check licence number.",
            "Check vehicle class.",
            "Check validity dates."
        ],

        "ration_card": [
            "Check household details.",
            "Check family member information.",
            "Check card number.",
            "Check issuing authority."
        ],

        "marks_card": [
            "Check student name.",
            "Check USN/registration number.",
            "Check semester and subjects.",
            "Check marks and university information."
        ],

        "unknown": [
            "Document type could not be confidently identified.",
            "Make sure the document image is clear.",
            "Try uploading a better-quality image or PDF.",
            "Do not upload passwords, OTPs or other secrets."
        ]
    }

    return checklists.get(document_type, checklists["unknown"])


def analyze_document(file_path):
    text, error = extract_document_text(file_path)

    if error:
        return {
            "success": False,
            "error": error,
            "text": "",
            "document_type": "unknown",
            "confidence": 0,
            "sensitive": [],
            "checklist": get_checklist("unknown")
        }

    document_type, score = detect_document_type(text)

    sensitive = detect_sensitive_information(text)

    confidence = min(score / 3, 1.0)

    return {
        "success": True,
        "error": None,
        "text": text,
        "document_type": document_type,
        "confidence": confidence,
        "sensitive": sensitive,
        "checklist": get_checklist(document_type)
    }


if __name__ == "__main__":
    print("GovAssist Document Intelligence")
    print("--------------------------------")
    print("Supported document types:")

    for item in DOCUMENT_TYPES:
        print("-", item)

    print("")
    print("OCR engine:", "READY" if pytesseract else "NOT AVAILABLE")
    print("PDF engine:", "READY" if PdfReader else "NOT AVAILABLE")

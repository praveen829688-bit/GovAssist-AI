from urllib.parse import urlparse
import re


# ============================================================
# VERIFIED INDIAN GOVERNMENT DOMAINS
# ============================================================

OFFICIAL_DOMAINS = {
    "india.gov.in",
    "services.india.gov.in",
    "mygov.in",
    "myscheme.gov.in",
    "digilocker.gov.in",
    "uidai.gov.in",
    "incometax.gov.in",
    "parivahan.gov.in",
    "passportindia.gov.in",
    "pmkisan.gov.in",
    "scholarships.gov.in",
    "education.gov.in",
    "mohfw.gov.in",
    "pmjay.gov.in",
    "nsp.gov.in",
    "epfindia.gov.in",
    "esic.gov.in",
    "rbi.org.in",
    "sebi.gov.in",
    "cybercrime.gov.in",
    "consumerhelpline.gov.in",
    "eci.gov.in",
    "courts.gov.in",
    "legislative.gov.in",
}


# Domains that are government-like but should still be checked.
GOVERNMENT_SUFFIXES = (
    ".gov.in",
    ".nic.in",
    ".ac.in",
)


SUSPICIOUS_KEYWORDS = {
    "freegift",
    "reward",
    "lottery",
    "claimnow",
    "urgent",
    "verifyaccount",
    "kycupdate",
    "prize",
    "cashback",
    "winner",
    "otp",
    "password",
    "accountblocked",
}


def normalize_url(url):
    url = str(url).strip()

    if not url:
        return ""

    if not re.match(r"^https?://", url, re.IGNORECASE):
        url = "https://" + url

    return url


def extract_domain(url):
    try:
        normalized = normalize_url(url)
        parsed = urlparse(normalized)

        domain = parsed.netloc.lower()

        if "@" in domain:
            domain = domain.split("@")[-1]

        if ":" in domain:
            domain = domain.split(":")[0]

        return domain

    except Exception:
        return ""


def is_official_domain(domain):
    domain = str(domain).lower().strip().rstrip(".")

    if domain in OFFICIAL_DOMAINS:
        return True

    # Only trust an actual government suffix.
    if domain.endswith(".gov.in"):
        return True

    return False


def verify_government_source(url):
    normalized = normalize_url(url)
    domain = extract_domain(normalized)

    if not domain:
        return {
            "status": "Invalid",
            "risk": "High",
            "domain": "",
            "official": False,
            "message": "The supplied URL is not valid."
        }

    official = is_official_domain(domain)

    if official:
        return {
            "status": "Likely Official",
            "risk": "Low",
            "domain": domain,
            "official": True,
            "message": (
                "This domain matches a recognized Indian government "
                "domain pattern. Still verify the exact page before "
                "entering personal information."
            )
        }

    # Suspicious wording in domain
    suspicious_matches = [
        keyword
        for keyword in SUSPICIOUS_KEYWORDS
        if keyword in domain.replace("-", "").replace(".", "")
    ]

    if suspicious_matches:
        return {
            "status": "High Risk",
            "risk": "High",
            "domain": domain,
            "official": False,
            "message": (
                "This domain contains suspicious keywords and is not "
                "recognized as an official government domain."
            )
        }

    # HTTPS alone does NOT mean government official.
    if normalized.lower().startswith("https://"):
        return {
            "status": "Needs Verification",
            "risk": "Medium",
            "domain": domain,
            "official": False,
            "message": (
                "The website uses HTTPS, but HTTPS alone does not "
                "prove that a website belongs to the government."
            )
        }

    return {
        "status": "High Risk",
        "risk": "High",
        "domain": domain,
        "official": False,
        "message": (
            "The website is not recognized as an official government "
            "domain and does not use HTTPS."
        )
    }


def explain_source_safety(url):
    result = verify_government_source(url)

    return (
        f"Status: {result['status']}\n"
        f"Risk: {result['risk']}\n"
        f"Domain: {result['domain']}\n\n"
        f"{result['message']}"
    )

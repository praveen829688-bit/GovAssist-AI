from urllib.parse import urlparse


OFFICIAL_DOMAINS = [
    ".gov.in",
    ".nic.in",
    "passportindia.gov.in",
    "incometax.gov.in",
    "parivahan.gov.in",
    "pmkisan.gov.in",
    "pmjay.gov.in",
    "scholarships.gov.in",
    "myscheme.gov.in",
    "sevasindhu.karnataka.gov.in",
    "ahara.kar.nic.in"
]


SUSPICIOUS_WORDS = [
    "free-money",
    "instant-loan",
    "reward",
    "lottery",
    "claim-prize",
    "urgent-payment",
    "verify-account",
    "otp"
]


def analyze_url(url):

    original = url.strip()

    if not original:
        return {
            "status": "Invalid",
            "score": 0,
            "reasons": ["No URL was provided."]
        }

    if not original.startswith(
        ("http://", "https://")
    ):
        original = "https://" + original

    try:
        parsed = urlparse(original)
        domain = parsed.netloc.lower()

    except Exception:
        return {
            "status": "Invalid",
            "score": 0,
            "reasons": ["The URL could not be parsed."]
        }

    score = 0
    reasons = []

    if parsed.scheme == "https":
        score += 20
        reasons.append(
            "HTTPS connection detected."
        )

    else:
        score -= 30
        reasons.append(
            "The website does not use HTTPS."
        )

    official = False

    for official_domain in OFFICIAL_DOMAINS:

        if (
            domain == official_domain
            or domain.endswith(official_domain)
        ):
            official = True
            score += 70

            reasons.append(
                "The domain matches a known government domain."
            )

            break

    if not official:

        reasons.append(
            "The domain was not recognized as an official government domain."
        )

    for word in SUSPICIOUS_WORDS:

        if word in original.lower():

            score -= 20

            reasons.append(
                f"Suspicious keyword detected: {word}"
            )

    score = max(
        0,
        min(100, score)
    )

    if official and score >= 70:
        status = "Likely Official"

    elif score >= 40:
        status = "Needs Verification"

    else:
        status = "High Risk"

    return {
        "status": status,
        "score": score,
        "domain": domain,
        "reasons": reasons
    }

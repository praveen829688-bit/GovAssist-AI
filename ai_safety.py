import re
from urllib.parse import urlparse

try:
    from official_source_verifier import verify_url
except Exception:
    verify_url = None


def extract_urls(text):
    if not text:
        return []

    pattern = r"https?://[^\s<>\"]+"

    return re.findall(pattern, str(text))


def check_url(url):
    if not url:
        return {
            "safe": False,
            "status": "Needs Verification",
            "reason": "No URL supplied."
        }

    try:
        parsed = urlparse(url)

        if parsed.scheme not in ("http", "https"):
            return {
                "safe": False,
                "status": "High Risk",
                "reason": "Unsupported URL scheme."
            }

        if not parsed.netloc:
            return {
                "safe": False,
                "status": "High Risk",
                "reason": "Invalid URL."
            }

        if verify_url:
            try:
                result = verify_url(url)

                if isinstance(result, dict):
                    return result
            except Exception:
                pass

        hostname = parsed.hostname or ""

        if hostname.endswith(".gov.in"):
            return {
                "safe": parsed.scheme == "https",
                "status": "Likely Official",
                "domain": hostname,
                "reason": "The domain uses the official .gov.in namespace."
            }

        if parsed.scheme != "https":
            return {
                "safe": False,
                "status": "High Risk",
                "domain": hostname,
                "reason": "The website does not use HTTPS."
            }

        return {
            "safe": False,
            "status": "Needs Verification",
            "domain": hostname,
            "reason": "The website is not recognized as an official government domain."
        }

    except Exception as exc:
        return {
            "safe": False,
            "status": "High Risk",
            "reason": f"URL validation failed: {exc}"
        }


def analyze_text(text):
    urls = extract_urls(text)

    results = []

    for url in urls:
        results.append({
            "url": url,
            "analysis": check_url(url)
        })

    return results


def confidence_score(text):
    """
    Heuristic confidence indicator.
    This is NOT a true hallucination detector.
    """

    if not text:
        return 0.0

    score = 0.5

    urls = extract_urls(text)

    if urls:
        score += 0.2

        for url in urls:
            result = check_url(url)

            if result.get("status") == "Likely Official":
                score += 0.2

    if "official source" in text.lower():
        score += 0.05

    return min(round(score, 2), 0.95)


def safety_warning(text):
    results = analyze_text(text)

    warnings = []

    for item in results:

        analysis = item["analysis"]

        if analysis.get("status") != "Likely Official":
            warnings.append(
                f"Verify this source before using it: {item['url']}"
            )

    return warnings


def protect_answer(text):
    """
    Adds safety guidance to AI-generated government answers.
    """

    if not text:
        return ""

    warnings = safety_warning(text)

    if not warnings:
        return text

    extra = "\n\nIMPORTANT: Verify government information using the official portal before submitting documents or making payments."

    return text + extra

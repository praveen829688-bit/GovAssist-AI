from official_source_verifier import (
    verify_government_source,
    extract_domain,
)


def analyze_url(url):
    result = verify_government_source(url)

    return {
        "url": url,
        "domain": result["domain"],
        "status": result["status"],
        "risk": result["risk"],
        "official": result["official"],
        "message": result["message"],
    }


def check_website(url):
    return analyze_url(url)


def detect_scam(url):
    return analyze_url(url)


def get_safety_advice(result):
    if result["risk"] == "Low":
        return [
            "Check that the domain is exactly correct.",
            "Do not share OTPs, passwords, PINs or CVV numbers.",
            "Verify important information on the official portal."
        ]

    if result["risk"] == "Medium":
        return [
            "HTTPS does not prove that the website is official.",
            "Do not enter Aadhaar, bank or login information yet.",
            "Find the service through India.gov.in or the relevant official portal.",
            "Check the spelling of the domain carefully."
        ]

    return [
        "Do not enter personal or financial information.",
        "Do not share OTPs, passwords, PINs or CVV numbers.",
        "Do not download unknown files or applications.",
        "Close the website and find the service through an official government portal.",
        "If you suspect fraud, consider reporting it through the appropriate official cybercrime channel."
    ]

import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
SCHEMES_FILE = BASE_DIR / "knowledge" / "schemes.json"


def load_schemes():
    if not SCHEMES_FILE.exists():
        return []

    with open(SCHEMES_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def normalize(value):
    return str(value).strip().lower()


def safe_number(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def calculate_scheme_score(profile, scheme):
    score = 0
    reasons = []
    checks = []

    age = safe_number(profile.get("age"))
    income = safe_number(profile.get("income"))

    student = profile.get("student", False)
    farmer = profile.get("farmer", False)

    category = normalize(profile.get("category", ""))
    state = normalize(profile.get("state", ""))

    scheme_name = normalize(scheme.get("name", ""))
    scheme_category = normalize(scheme.get("category", ""))
    target = normalize(scheme.get("target", ""))
    keywords = [
        normalize(x)
        for x in scheme.get("keywords", [])
    ]

    searchable = " ".join([
        scheme_name,
        scheme_category,
        target,
        " ".join(keywords)
    ])

    # --------------------------------------------------------
    # Student matching
    # --------------------------------------------------------

    if student:

        if (
            "student" in searchable
            or "education" in searchable
            or "scholarship" in searchable
        ):
            score += 35

            reasons.append(
                "The scheme appears relevant to students."
            )

            checks.append(
                "Student status matches the scheme's target group."
            )

    # --------------------------------------------------------
    # Farmer matching
    # --------------------------------------------------------

    if farmer:

        if (
            "farmer" in searchable
            or "agriculture" in searchable
        ):
            score += 35

            reasons.append(
                "The scheme appears relevant to farmers."
            )

            checks.append(
                "Farmer status matches the scheme's target group."
            )

    # --------------------------------------------------------
    # Age relevance
    # --------------------------------------------------------

    if age > 0:

        if student and 15 <= age <= 35:
            score += 10

            reasons.append(
                "Age is within a common student-age range."
            )

        elif farmer and age >= 18:
            score += 5

            reasons.append(
                "Age is compatible with an adult beneficiary profile."
            )

    # --------------------------------------------------------
    # Income relevance
    # --------------------------------------------------------

    if income > 0:

        if (
            "scholarship" in searchable
            or "education" in searchable
        ):
            score += 15

            reasons.append(
                "Income information can be relevant to education benefits."
            )

            checks.append(
                "Verify the exact income threshold for the selected scholarship."
            )

        elif (
            "housing" in searchable
            or "health" in searchable
            or "welfare" in searchable
        ):
            score += 5

            reasons.append(
                "Income may be relevant to welfare eligibility."
            )

            checks.append(
                "Verify the official income and beneficiary criteria."
            )

    # --------------------------------------------------------
    # Category relevance
    # --------------------------------------------------------

    if category:

        category_map = {
            "obc": ["scholarship", "education"],
            "sc": ["scholarship", "education"],
            "st": ["scholarship", "education"],
            "general": ["education"],
            "ews": ["education", "housing"],
            "minority": ["scholarship", "education"]
        }

        relevant_categories = category_map.get(
            category,
            []
        )

        for keyword in relevant_categories:

            if keyword in searchable:
                score += 10

                reasons.append(
                    f"Your category may be relevant to {keyword}-related benefits."
                )

                break

    # --------------------------------------------------------
    # State relevance
    # --------------------------------------------------------

    if state:

        scheme_state = normalize(
            scheme.get("state", "")
        )

        if scheme_state and (
            state in scheme_state
            or scheme_state in state
            or scheme_state == "india"
        ):
            score += 10

            reasons.append(
                "The scheme is applicable nationally or appears relevant to your state."
            )

    score = min(score, 100)

    if score >= 70:
        status = "Highly Relevant"

    elif score >= 45:
        status = "Potentially Relevant"

    elif score >= 20:
        status = "Needs Verification"

    else:
        status = "Low Match"

    return {
        "scheme": scheme,
        "score": score,
        "status": status,
        "reasons": reasons,
        "checks": checks
    }


def recommend_schemes(profile, limit=5):
    results = []

    for scheme in load_schemes():

        result = calculate_scheme_score(
            profile,
            scheme
        )

        if result["score"] > 0:
            results.append(result)

    results.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return results[:limit]


def eligibility_summary(profile, results):
    if not results:
        return (
            "No potentially relevant scheme was identified "
            "from the current knowledge base."
        )

    top = results[0]

    return (
        f"Based on the information provided, "
        f"{top['scheme']['name']} has the highest "
        f"preliminary relevance score of {top['score']}%."
    )


if __name__ == "__main__":

    demo_profile = {
        "age": 21,
        "state": "Karnataka",
        "income": 250000,
        "category": "OBC",
        "student": True,
        "farmer": False
    }

    print("")
    print("======================================")
    print(" GOVASSIST ELIGIBILITY ENGINE")
    print("======================================")

    results = recommend_schemes(
        demo_profile
    )

    for result in results:

        print("")
        print(result["scheme"]["name"])
        print("Score :", result["score"])
        print("Status:", result["status"])

        for reason in result["reasons"]:
            print("-", reason)

    print("")
    print(
        eligibility_summary(
            demo_profile,
            results
        )
    )

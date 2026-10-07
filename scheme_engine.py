from pathlib import Path
import json
import re


BASE_DIR = Path(__file__).resolve().parent
SCHEME_FILE = BASE_DIR / "knowledge" / "schemes.json"


def load_schemes():

    if not SCHEME_FILE.exists():
        return []

    try:

        with open(
            SCHEME_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

        if isinstance(data, list):
            return data

        if isinstance(data, dict):

            for key in [
                "schemes",
                "items",
                "data"
            ]:

                if isinstance(
                    data.get(key),
                    list
                ):
                    return data[key]

    except Exception as e:

        print(
            "Scheme loading error:",
            e
        )

    return []


def text_of_scheme(scheme):

    values = []

    for value in scheme.values():

        if isinstance(
            value,
            (str, int, float, bool)
        ):

            values.append(
                str(value)
            )

    return " ".join(values).lower()


def keyword_score(profile, scheme):

    text = text_of_scheme(
        scheme
    )

    score = 0
    reasons = []

    # --------------------------------------------------------
    # STUDENT
    # --------------------------------------------------------

    if profile.get("student"):

        if any(
            word in text
            for word in [
                "student",
                "scholarship",
                "education",
                "school",
                "college"
            ]
        ):

            score += 30

            reasons.append(
                "The scheme appears relevant to students."
            )

    # --------------------------------------------------------
    # FARMER
    # --------------------------------------------------------

    if profile.get("farmer"):

        if any(
            word in text
            for word in [
                "farmer",
                "agriculture",
                "agricultural",
                "cultivation",
                "kisan"
            ]
        ):

            score += 30

            reasons.append(
                "The scheme appears relevant to farmers."
            )

    # --------------------------------------------------------
    # CATEGORY
    # --------------------------------------------------------

    category = str(
        profile.get(
            "category",
            ""
        )
    ).lower()

    if category:

        category_words = {

            "sc": [
                "scheduled caste",
                "sc",
                "sc category"
            ],

            "st": [
                "scheduled tribe",
                "st",
                "st category"
            ],

            "obc": [
                "obc",
                "backward class",
                "other backward"
            ],

            "ews": [
                "ews",
                "economically weaker"
            ],

            "general": [
                "general",
                "all citizens",
                "all eligible"
            ]
        }

        for word in category_words.get(
            category,
            []
        ):

            if word in text:

                score += 20

                reasons.append(
                    f"The scheme contains information "
                    f"relevant to the {category.upper()} category."
                )

                break

    # --------------------------------------------------------
    # INCOME
    # --------------------------------------------------------

    income = profile.get(
        "income"
    )

    if income is not None:

        income_text = str(
            income
        )

        # If scheme contains income-related eligibility,
        # give a modest relevance score.
        if any(
            word in text
            for word in [
                "income",
                "annual income",
                "family income"
            ]
        ):

            score += 10

            reasons.append(
                "Income may be an eligibility factor."
            )

    # --------------------------------------------------------
    # NEED
    # --------------------------------------------------------

    need = str(
        profile.get(
            "need",
            ""
        )
    ).lower()

    if need:

        need_tokens = set(
            re.findall(
                r"[a-zA-Z]+",
                need
            )
        )

        scheme_tokens = set(
            re.findall(
                r"[a-zA-Z]+",
                text
            )
        )

        overlap = (
            need_tokens &
            scheme_tokens
        )

        if overlap:

            score += min(
                len(overlap) * 5,
                25
            )

            reasons.append(
                "The scheme description "
                "matches part of your stated need."
            )

    return score, reasons


def find_matching_schemes(
    profile,
    limit=10
):

    schemes = load_schemes()

    results = []

    for scheme in schemes:

        score, reasons = keyword_score(
            profile,
            scheme
        )

        name = (
            scheme.get("name")
            or scheme.get("title")
            or scheme.get("scheme")
            or "Government Scheme"
        )

        results.append(
            {
                "name": name,
                "score": score,
                "reasons": reasons,
                "data": scheme
            }
        )

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results[:limit]


def eligibility_message(result):

    score = result["score"]

    if score >= 50:

        return "Strong preliminary match"

    if score >= 25:

        return "Potential match"

    return "Low preliminary match"

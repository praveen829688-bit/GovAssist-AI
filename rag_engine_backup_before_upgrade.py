from pathlib import Path
import json
import re

BASE_DIR = Path(__file__).resolve().parent
KNOWLEDGE_DIR = BASE_DIR / "knowledge"


def load_json(filename):

    path = KNOWLEDGE_DIR / filename

    if not path.exists():
        return []

    try:

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except Exception:

        return []


def tokens(text):

    return set(
        re.findall(
            r"[a-zA-Z0-9]+",
            str(text).lower()
        )
    )


def item_text(item):

    return " ".join([
        item.get("name", ""),
        item.get("description", ""),
        item.get("category", ""),
        item.get("target", ""),
        item.get("eligibility", ""),
        " ".join(
            item.get("keywords", [])
        )
    ])


def relevance(query, item):

    query_tokens = tokens(query)

    item_tokens = tokens(
        item_text(item)
    )

    if not query_tokens:
        return 0

    score = len(
        query_tokens.intersection(
            item_tokens
        )
    )

    name_tokens = tokens(
        item.get("name", "")
    )

    score += 3 * len(
        query_tokens.intersection(
            name_tokens
        )
    )

    return score


def retrieve(query, limit=8):

    services = load_json(
        "services.json"
    )

    schemes = load_json(
        "schemes.json"
    )

    results = []

    for item in services:

        score = relevance(
            query,
            item
        )

        if score > 0:

            results.append(
                (
                    score,
                    "service",
                    item
                )
            )

    for item in schemes:

        score = relevance(
            query,
            item
        )

        if score > 0:

            results.append(
                (
                    score,
                    "scheme",
                    item
                )
            )

    results.sort(
        key=lambda x: x[0],
        reverse=True
    )

    return results[:limit]


def build_rag_context(query):

    results = retrieve(
        query,
        limit=8
    )

    if not results:

        return (
            "No matching records were found "
            "in the GovAssist knowledge base."
        )

    lines = []

    for score, item_type, item in results:

        lines.append(
            f"""
TYPE: {item_type}
NAME: {item.get('name', '')}
CATEGORY: {item.get('category', '')}
DESCRIPTION: {item.get('description', '')}
ELIGIBILITY: {item.get('eligibility', 'Not specified')}
DOCUMENTS: {', '.join(item.get('documents', []))}
OFFICIAL SOURCE: {item.get('source', '')}
RELEVANCE SCORE: {score}
"""
        )

    return "\n".join(lines)


if __name__ == "__main__":

    print(
        build_rag_context(
            "student scholarship"
        )
    )

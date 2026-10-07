import json
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
KNOWLEDGE_DIR = BASE_DIR / "knowledge"


def load_json(filename):
    path = KNOWLEDGE_DIR / filename

    if not path.exists():
        return []

    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception:
        return []


def load_services():
    return load_json("services.json")


def load_schemes():
    return load_json("schemes.json")


def tokenize(text):
    return set(
        re.findall(
            r"[a-zA-Z0-9]+",
            str(text).lower()
        )
    )


def score_item(query, item):
    query_words = tokenize(query)

    searchable = " ".join([
        item.get("name", ""),
        item.get("category", ""),
        item.get("description", ""),
        item.get("target", ""),
        item.get("eligibility", ""),
        " ".join(item.get("keywords", []))
    ])

    item_words = tokenize(searchable)

    if not query_words:
        return 0

    score = len(query_words.intersection(item_words))

    name_words = tokenize(item.get("name", ""))
    score += len(query_words.intersection(name_words)) * 3

    return score


def search_items(query, items, limit=5):
    results = []

    for item in items:
        score = score_item(query, item)

        if score > 0:
            results.append((score, item))

    results.sort(key=lambda x: x[0], reverse=True)

    return [item for score, item in results[:limit]]


def search_services(query, limit=5):
    return search_items(query, load_services(), limit)


def search_schemes(query, limit=5):
    return search_items(query, load_schemes(), limit)


def get_knowledge_context(query):
    services = search_services(query, 5)
    schemes = search_schemes(query, 5)

    lines = []

    if services:
        lines.append("MATCHING GOVERNMENT SERVICES:")

        for item in services:
            lines.append(
                f"- {item['name']}: {item.get('description', '')}"
            )

    if schemes:
        lines.append("")
        lines.append("MATCHING GOVERNMENT SCHEMES:")

        for item in schemes:
            lines.append(
                f"- {item['name']}: {item.get('description', '')}"
            )

    if not lines:
        return "No matching government information was found."

    return "\n".join(lines)


if __name__ == "__main__":
    print("GovAssist Knowledge Engine")
    print("--------------------------")

    print("Services:", len(load_services()))
    print("Schemes:", len(load_schemes()))

    query = "student scholarship"

    print("")
    print("Search:", query)
    print("")

    for item in search_schemes(query):
        print("-", item["name"])

    print("")
    print(get_knowledge_context(query))

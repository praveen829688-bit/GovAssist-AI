from pathlib import Path
import json
import re


BASE_DIR = Path(__file__).resolve().parent
KNOWLEDGE_DIR = BASE_DIR / "knowledge"


def _load_json(filename):
    path = KNOWLEDGE_DIR / filename

    if not path.exists():
        return []

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if isinstance(data, list):
            return data

        if isinstance(data, dict):
            for key in ["services", "schemes", "items", "data"]:
                if isinstance(data.get(key), list):
                    return data[key]

    except Exception as e:
        print("Knowledge loading error:", e)

    return []


def load_services():
    return _load_json("services.json")


def load_schemes():
    return _load_json("schemes.json")


def _tokens(text):
    return set(
        re.findall(
            r"[a-zA-Z0-9]+",
            str(text).lower()
        )
    )


def _search_items(query, items, limit=5):
    query_tokens = _tokens(query)

    if not query_tokens:
        return []

    scored = []

    for item in items:
        searchable = " ".join(
            str(value)
            for value in item.values()
            if isinstance(value, (str, int, float, bool))
        ).lower()

        item_tokens = _tokens(searchable)

        score = len(query_tokens.intersection(item_tokens))

        # Extra weight for title/name matches
        title = str(
            item.get("name")
            or item.get("title")
            or item.get("service")
            or item.get("scheme")
            or ""
        ).lower()

        for token in query_tokens:
            if token in title:
                score += 3

        if score > 0:
            scored.append((score, item))

    scored.sort(key=lambda x: x[0], reverse=True)

    return [item for _, item in scored[:limit]]


def search_knowledge(query, limit=5):
    services = _search_items(
        query,
        load_services(),
        limit
    )

    schemes = _search_items(
        query,
        load_schemes(),
        limit
    )

    return {
        "services": services,
        "schemes": schemes
    }


def build_rag_context(query, limit=5):
    results = search_knowledge(query, limit)

    sections = []

    if results["services"]:
        sections.append("GOVERNMENT SERVICES:")

        for item in results["services"]:
            name = (
                item.get("name")
                or item.get("title")
                or item.get("service")
                or "Government Service"
            )

            sections.append(f"\nService: {name}")

            for key, value in item.items():
                if key.lower() not in [
                    "name",
                    "title",
                    "service"
                ]:
                    sections.append(
                        f"{key}: {value}"
                    )

    if results["schemes"]:
        sections.append("\nGOVERNMENT SCHEMES:")

        for item in results["schemes"]:
            name = (
                item.get("name")
                or item.get("title")
                or item.get("scheme")
                or "Government Scheme"
            )

            sections.append(f"\nScheme: {name}")

            for key, value in item.items():
                if key.lower() not in [
                    "name",
                    "title",
                    "scheme"
                ]:
                    sections.append(
                        f"{key}: {value}"
                    )

    if not sections:
        return "No matching government knowledge-base records were found."

    return "\n".join(sections)


def get_relevant_sources(query):
    results = search_knowledge(query)

    sources = []

    for item in results["services"]:
        name = (
            item.get("name")
            or item.get("title")
            or item.get("service")
        )

        if name:
            sources.append({
                "type": "Government Service",
                "name": name
            })

    for item in results["schemes"]:
        name = (
            item.get("name")
            or item.get("title")
            or item.get("scheme")
        )

        if name:
            sources.append({
                "type": "Government Scheme",
                "name": name
            })

    return sources

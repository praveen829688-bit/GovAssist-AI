from pathlib import Path
import json

def get_knowledge_counts():
    """Return live counts from the GovAssist knowledge base."""

    services_file = Path("knowledge/services.json")
    schemes_file = Path("knowledge/schemes.json")

    services_count = 0
    schemes_count = 0

    try:
        if services_file.exists():
            with open(services_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            if isinstance(data, list):
                services_count = len(data)
            elif isinstance(data, dict):
                services_count = len(
                    data.get("services", data.get("items", []))
                )

    except Exception:
        services_count = 0

    try:
        if schemes_file.exists():
            with open(schemes_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            if isinstance(data, list):
                schemes_count = len(data)
            elif isinstance(data, dict):
                schemes_count = len(
                    data.get("schemes", data.get("items", []))
                )

    except Exception:
        schemes_count = 0

    return services_count, schemes_count

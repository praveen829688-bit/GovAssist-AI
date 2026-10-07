import os
from pathlib import Path


def check_health():

    root = Path(__file__).resolve().parent

    checks = {}

    checks["Application"] = True

    checks["Knowledge Base"] = (
        (root / "knowledge").exists()
    )

    checks["Database"] = (
        (root / "data" / "govassist.db").exists()
    )

    checks["AI Configuration"] = bool(
        os.getenv(
            "OPENAI_API_KEY",
            ""
        ).strip()
    )

    checks["Document Engine"] = (
        (root / "document_ai.py").exists()
    )

    checks["RAG Engine"] = (
        (root / "rag_engine.py").exists()
    )

    return checks


def health_score():

    checks = check_health()

    passed = sum(
        1
        for value in checks.values()
        if value
    )

    return int(
        passed /
        len(checks) *
        100
    )

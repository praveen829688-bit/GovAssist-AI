import os

from dotenv import load_dotenv

from rag_engine import build_rag_context

load_dotenv()

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


MODEL = os.getenv(
    "OPENAI_MODEL",
    "gpt-6-luna"
)

API_KEY = os.getenv(
    "OPENAI_API_KEY",
    ""
).strip()


def fallback_answer(question):

    q = question.lower()

    if "scholarship" in q:

        return (
            "I found scholarship-related information in the "
            "GovAssist knowledge base. Check the Scheme Finder "
            "and Eligibility Checker for potentially relevant "
            "programmes, then verify the final eligibility on "
            "the official government portal."
        )

    if "passport" in q:

        return (
            "GovAssist can guide you regarding passport services. "
            "Please verify current documents, fees and appointment "
            "requirements through the official Passport Seva portal."
        )

    if "certificate" in q:

        return (
            "GovAssist can help you locate government certificate "
            "services such as Income, Birth, Caste and Residence "
            "certificates."
        )

    return (
        "I am GovAssist AI. I can help you find government "
        "services, schemes, eligibility information, documents "
        "and application guidance."
    )


def ask_govassist(
    question,
    services=None,
    schemes=None
):

    question = question.strip()

    if not question:

        return "Please enter your question."

    context = build_rag_context(
        question
    )

    if not API_KEY or OpenAI is None:

        return fallback_answer(
            question
        )

    try:

        client = OpenAI(
            api_key=API_KEY
        )

        instructions = f"""
You are GovAssist AI.

You are an intelligent assistant for discovering
Indian government services and schemes.

IMPORTANT RULES:

1. Use the supplied knowledge context as your primary source.
2. Never invent government rules.
3. Never invent eligibility requirements.
4. Never invent fees or deadlines.
5. If information is missing, say so.
6. Encourage verification using the official source.
7. Never request OTPs, passwords, PINs or authentication secrets.
8. Do not claim to be a government employee.
9. Give practical step-by-step guidance.
10. Clearly distinguish between "potentially eligible"
    and "officially eligible".
11. Answer in the language requested by the user.
12. Keep answers concise and structured.

KNOWLEDGE CONTEXT:

{context}
"""

        response = client.responses.create(
            model=MODEL,
            instructions=instructions,
            input=question
        )

        answer = response.output_text.strip()

        if answer:

            return answer

        return fallback_answer(
            question
        )

    except Exception:

        return fallback_answer(
            question
        )

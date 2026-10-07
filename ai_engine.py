import os
from dotenv import load_dotenv

load_dotenv()

from rag_engine import build_rag_context, get_relevant_sources


MODEL = os.getenv(
    "OPENAI_MODEL",
    "gpt-6-luna"
)

API_KEY = os.getenv(
    "OPENAI_API_KEY",
    ""
)


SYSTEM_PROMPT = """
You are GovAssist AI, a government-service information assistant.

Your job is to help citizens understand government services,
schemes, documents, application processes and eligibility.

IMPORTANT RULES:

1. Prefer the provided GovAssist knowledge base.
2. Never invent government schemes, URLs, fees, deadlines or eligibility rules.
3. If information is missing, clearly say that it needs verification.
4. Government eligibility provided by this system is preliminary guidance,
   not an official eligibility decision.
5. Encourage users to verify important information on the relevant
   official government portal.
6. Never ask users for OTPs, passwords, PINs, CVV numbers or other
   authentication secrets.
7. Do not request unnecessary Aadhaar or other sensitive information.
8. Give clear step-by-step answers.
9. When relevant, mention required documents.
10. Keep answers understandable for ordinary citizens.
"""


def _local_fallback(question, context):
    question_lower = question.lower()

    if context and "No matching" not in context:
        return (
            "Based on the GovAssist knowledge base, I found relevant "
            "government information.\n\n"
            + context
            + "\n\n"
            "Please verify the latest requirements and application "
            "details on the official government portal before applying."
        )

    if "document" in question_lower:
        return (
            "I can help identify the documents usually needed for "
            "government services. Please tell me the exact service "
            "you want to apply for."
        )

    if "scheme" in question_lower:
        return (
            "I can help you find government schemes. Tell me your "
            "state, approximate income, student/farmer status and "
            "the type of assistance you need. Do not share OTPs, "
            "passwords or other sensitive credentials."
        )

    return (
        "I couldn't find a strong match in the current GovAssist "
        "knowledge base. Please provide the government service, "
        "scheme or document you are asking about."
    )


def ask_govassist(question):
    question = str(question).strip()

    if not question:
        return {
            "answer": "Please enter a government-service question.",
            "sources": []
        }

    context = build_rag_context(question)
    sources = get_relevant_sources(question)

    # --------------------------------------------------------
    # OPENAI RESPONSES API
    # --------------------------------------------------------
    if API_KEY:

        try:
            from openai import OpenAI

            client = OpenAI(
                api_key=API_KEY
            )

            prompt = f"""
USER QUESTION:
{question}

RETRIEVED GOVASSIST KNOWLEDGE:
{context}

Answer the user's question using the retrieved knowledge.

If the retrieved knowledge does not contain enough information,
say that the information requires verification instead of inventing
an answer.

End with a short reminder to verify important details on the
official government portal when appropriate.
"""

            response = client.responses.create(
                model=MODEL,
                instructions=SYSTEM_PROMPT,
                input=prompt
            )

            answer = response.output_text.strip()

            if not answer:
                answer = _local_fallback(
                    question,
                    context
                )

            return {
                "answer": answer,
                "sources": sources
            }

        except Exception as e:

            print(
                "OpenAI request failed:",
                type(e).__name__,
                str(e)
            )

    # --------------------------------------------------------
    # SAFE LOCAL FALLBACK
    # --------------------------------------------------------
    return {
        "answer": _local_fallback(
            question,
            context
        ),
        "sources": sources
    }


def ask_ai(question):
    """
    Backward-compatible function for the existing app.
    """
    result = ask_govassist(question)
    return result["answer"]

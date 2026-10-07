import streamlit as st
import os
import sqlite3
from datetime import datetime


def get_project_health():

    checks = {}

    checks["Application"] = os.path.exists("app.py")
    checks["Authentication"] = os.path.exists("auth.py")
    checks["Database"] = os.path.exists("data/govassist.db")
    checks["Knowledge Base"] = os.path.exists("knowledge")
    checks["RAG Engine"] = os.path.exists("rag_engine.py")
    checks["Document AI"] = os.path.exists("document_ai.py")
    checks["Scam Detector"] = os.path.exists("scam_detector.py")
    checks["AI Safety"] = os.path.exists("ai_safety.py")
    checks["Security"] = os.path.exists("security_utils.py")

    return checks


def get_platform_counts():

    result = {
        "users": 0,
        "applications": 0,
        "notifications": 0
    }

    db = "data/govassist.db"

    if not os.path.exists(db):
        return result

    try:

        conn = sqlite3.connect(db)
        cur = conn.cursor()

        for table, key in [
            ("users", "users"),
            ("applications", "applications"),
            ("notifications", "notifications")
        ]:

            try:
                cur.execute(
                    f"SELECT COUNT(*) FROM {table}"
                )
                result[key] = cur.fetchone()[0]
            except Exception:
                pass

        conn.close()

    except Exception:
        pass

    return result


def render_final_overview():

    st.title("GovAssist AI")

    st.caption(
        "AI-Powered Government Service Intelligence Platform"
    )

    st.success(
        "AI System Online"
    )

    st.markdown("""
    GovAssist AI helps citizens discover government services,
    schemes, documents and application information through an
    intelligent and secure digital assistant.
    """)

    st.divider()

    counts = get_platform_counts()

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Registered Citizens",
            counts["users"]
        )

    with c2:
        st.metric(
            "Applications",
            counts["applications"]
        )

    with c3:
        st.metric(
            "Notifications",
            counts["notifications"]
        )

    with c4:
        st.metric(
            "AI Modules",
            "10+"
        )

    st.divider()

    st.subheader("Platform Capabilities")

    features = [
        ("AI Assistant", "Government questions with AI assistance"),
        ("Service Finder", "Discover relevant government services"),
        ("Scheme Finder", "Find potentially relevant schemes"),
        ("Document Intelligence", "OCR and document analysis"),
        ("Scam Detector", "Check suspicious government URLs"),
        ("Application Tracker", "Track personal applications"),
        ("Notifications", "Personal reminders and alerts"),
        ("Multilingual", "English, Kannada, Hindi, Tamil and Telugu"),
        ("Voice", "Browser-based voice input"),
        ("Security", "Authentication and user data isolation")
    ]

    cols = st.columns(2)

    for index, item in enumerate(features):

        with cols[index % 2]:

            st.markdown(
                f"""
                <div style="
                    padding:16px;
                    margin-bottom:12px;
                    border-radius:12px;
                    background:#0d1b2a;
                    border:1px solid #26384d;
                ">
                    <strong style="color:#60a5fa;">
                        {item[0]}
                    </strong>
                    <br>
                    <span style="color:#cbd5e1;">
                        {item[1]}
                    </span>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.divider()

    st.subheader("System Health")

    health = get_project_health()

    for component, status in health.items():

        if status:
            st.success(
                f"{component}: Operational"
            )
        else:
            st.warning(
                f"{component}: Needs attention"
            )

    st.divider()

    st.info(
        "Important: GovAssist AI provides informational assistance. "
        "Citizens should verify important eligibility, deadlines and "
        "requirements through the relevant official government portal."
    )

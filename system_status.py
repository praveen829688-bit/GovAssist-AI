import streamlit as st
import os


def render_system_status():

    st.title("System Status")

    st.caption(
        "GovAssist AI component health and readiness"
    )

    components = {
        "Authentication": "auth.py",
        "Citizen Dashboard": "citizen_dashboard.py",
        "Application Tracker": "tracker_page.py",
        "Notifications": "notifications_page.py",
        "AI Engine": "ai_engine.py",
        "RAG Engine": "rag_engine.py",
        "AI Safety": "ai_safety.py",
        "Document Intelligence": "document_ai.py",
        "Scam Detection": "scam_detector.py",
        "Official Source Verification": "official_source_verifier.py",
        "Multilingual": "multilingual_voice.py",
        "Security": "security_utils.py",
        "Admin Dashboard": "admin_dashboard.py"
    }

    for name, file_name in components.items():

        exists = os.path.exists(file_name)

        if exists:
            st.success(
                f"{name} — Ready"
            )
        else:
            st.warning(
                f"{name} — File not found"
            )

    st.divider()

    st.subheader("Deployment Checklist")

    checklist = [
        "Environment variables configured",
        "Production database configured",
        "Trusted origins configured",
        "HTTPS enabled",
        "Production secrets configured",
        "Rate limiting enabled",
        "Database backups configured",
        "Monitoring configured",
        "Official government sources verified"
    ]

    for item in checklist:
        st.checkbox(
            item,
            key="check_" + item
        )

    st.caption(
        "The checklist is informational and does not automatically "
        "verify external infrastructure."
    )

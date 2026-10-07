import streamlit as st
from datetime import datetime, date
from database import init_db, get_applications, add_notification, get_notifications

def render_notifications_page():
    init_db()

    st.title("Notification Center")
    st.caption("Application updates, deadlines and citizen reminders")

    tab1, tab2 = st.tabs(["Notifications", "Create Reminder"])

    with tab1:
        notifications = get_notifications()

        if not notifications:
            st.info("No notifications yet.")
        else:
            for item in notifications:
                if isinstance(item, dict):
                    title = item.get("title", "Notification")
                    message = item.get("message", "")
                    created = item.get("created_at", "")
                    st.markdown(
                        f"""
                        <div style="
                            padding:16px;
                            margin-bottom:12px;
                            border-radius:12px;
                            background:#0d1b2a;
                            border:1px solid #26384d;
                        ">
                            <h4 style="margin:0;color:#60a5fa;">{title}</h4>
                            <p style="color:#f8fafc;">{message}</p>
                            <small style="color:#94a3b8;">{created}</small>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

    with tab2:
        st.subheader("Create Citizen Reminder")

        title = st.text_input(
            "Reminder title",
            placeholder="Example: Submit income certificate"
        )

        message = st.text_area(
            "Reminder message",
            placeholder="Enter the important information..."
        )

        reminder_date = st.date_input(
            "Reminder date",
            value=date.today()
        )

        if st.button("Create Reminder", use_container_width=True):
            if not title.strip() or not message.strip():
                st.warning("Please enter both title and message.")
            else:
                try:
                    add_notification(
                        title.strip(),
                        message.strip(),
                        reminder_date.isoformat()
                    )
                    st.success("Reminder created successfully.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Unable to create reminder: {e}")

    st.divider()

    st.subheader("Application Alerts")

    try:
        applications = get_applications()

        if not applications:
            st.info("No applications available for alerts.")
        else:
            for app in applications:
                if isinstance(app, dict):
                    name = app.get("service_name", "Application")
                    status = app.get("status", "Unknown")
                    ref = app.get("reference_number", "")

                    if status in ["Documents Required", "Rejected"]:
                        st.warning(
                            f"**{name}** — {status}"
                            + (f" | Reference: {ref}" if ref else "")
                        )
                    elif status == "Approved":
                        st.success(
                            f"**{name}** — Application approved"
                            + (f" | Reference: {ref}" if ref else "")
                        )
                    elif status in ["Submitted", "Under Review"]:
                        st.info(
                            f"**{name}** — {status}"
                            + (f" | Reference: {ref}" if ref else "")
                        )
    except Exception as e:
        st.error(f"Unable to load application alerts: {e}")

    st.divider()

    st.caption(
        "Privacy note: reminders are stored locally in the GovAssist database. "
        "Do not store passwords, OTPs or unnecessary sensitive information."
    )

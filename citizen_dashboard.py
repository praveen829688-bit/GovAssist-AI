import streamlit as st

from user_data import (
    get_user_applications,
    get_user_notifications,
    get_user_statistics,
    create_user_notification
)


def render_citizen_dashboard():

    user_id = st.session_state.get("user_id")

    if not user_id:
        st.error("Authentication required.")
        return

    user_name = st.session_state.get(
        "user_name",
        "Citizen"
    )

    user_email = st.session_state.get(
        "user_email",
        ""
    )

    st.title("Citizen Dashboard")

    st.markdown(
        f"### Welcome, {user_name}"
    )

    st.caption(
        f"Secure citizen account: {user_email}"
    )

    # ========================================================
    # STATISTICS
    # ========================================================

    stats = get_user_statistics(user_id)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "My Applications",
            stats["total"]
        )

    with col2:
        st.metric(
            "Active",
            stats["active"]
        )

    with col3:
        st.metric(
            "Approved",
            stats["approved"]
        )

    with col4:
        st.metric(
            "Notifications",
            stats["notifications"]
        )

    st.divider()

    # ========================================================
    # APPLICATIONS
    # ========================================================

    st.subheader("My Applications")

    applications = get_user_applications(user_id)

    if not applications:
        st.info(
            "You have not submitted any applications yet."
        )
    else:

        for app in applications:

            service = app.get(
                "service_name",
                "Government Service"
            )

            status = app.get(
                "status",
                "Submitted"
            )

            reference = app.get(
                "reference_number",
                ""
            )

            application_date = app.get(
                "application_date",
                ""
            )

            status_icons = {
                "Draft": "📝",
                "Submitted": "📤",
                "Under Review": "🔎",
                "Documents Required": "📄",
                "Approved": "✅",
                "Rejected": "❌",
                "Completed": "🎉"
            }

            icon = status_icons.get(
                status,
                "📌"
            )

            with st.expander(
                f"{icon} {service} — {status}"
            ):

                if reference:
                    st.write(
                        f"**Reference:** {reference}"
                    )

                if application_date:
                    st.write(
                        f"**Application Date:** "
                        f"{application_date}"
                    )

                notes = app.get(
                    "notes",
                    ""
                )

                if notes:
                    st.write(
                        f"**Notes:** {notes}"
                    )

                st.progress(
                    {
                        "Draft": 0.1,
                        "Submitted": 0.25,
                        "Under Review": 0.5,
                        "Documents Required": 0.5,
                        "Approved": 0.8,
                        "Rejected": 0.8,
                        "Completed": 1.0
                    }.get(status, 0.25)
                )


    # ========================================================
    # NOTIFICATIONS
    # ========================================================

    st.divider()

    st.subheader("My Notifications")

    notifications = get_user_notifications(user_id)

    if not notifications:

        st.info(
            "You currently have no notifications."
        )

    else:

        for notification in notifications:

            title = notification.get(
                "title",
                "Notification"
            )

            message = notification.get(
                "message",
                ""
            )

            reminder = notification.get(
                "reminder_date",
                ""
            )

            st.info(
                f"**{title}**\n\n"
                f"{message}"
                + (
                    f"\n\nReminder: {reminder}"
                    if reminder else ""
                )
            )


    # ========================================================
    # QUICK REMINDER
    # ========================================================

    st.divider()

    with st.expander(
        "Create a Personal Reminder"
    ):

        reminder_title = st.text_input(
            "Reminder title",
            key="citizen_reminder_title"
        )

        reminder_message = st.text_area(
            "Reminder message",
            key="citizen_reminder_message"
        )

        if st.button(
            "Save Reminder",
            use_container_width=True
        ):

            if not reminder_title.strip():
                st.warning(
                    "Enter a reminder title."
                )

            elif not reminder_message.strip():
                st.warning(
                    "Enter a reminder message."
                )

            else:

                create_user_notification(
                    user_id,
                    reminder_title.strip(),
                    reminder_message.strip()
                )

                st.success(
                    "Personal reminder saved."
                )

                st.rerun()


    st.divider()

    st.caption(
        "Privacy: Your dashboard only retrieves records "
        "associated with your authenticated user account."
    )

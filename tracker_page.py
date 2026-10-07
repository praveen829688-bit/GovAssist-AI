import streamlit as st
from datetime import date

from user_data import (
    create_user_application,
    get_user_applications,
    update_user_application_status
)


def render_tracker_page():

    user_id = st.session_state.get("user_id")

    if not user_id:
        st.error("Please login first.")
        return

    st.title("Application Tracker")
    st.caption(
        "Track your government applications securely."
    )

    st.subheader("Submit New Application")

    service_name = st.text_input(
        "Service / Scheme Name"
    )

    reference_number = st.text_input(
        "Reference Number"
    )

    application_date = st.date_input(
        "Application Date",
        value=date.today()
    )

    notes = st.text_area(
        "Notes"
    )

    if st.button(
        "Add Application",
        use_container_width=True,
        type="primary"
    ):

        if not service_name.strip():

            st.warning(
                "Please enter the service or scheme name."
            )

        else:

            create_user_application(
                user_id=user_id,
                service_name=service_name.strip(),
                reference_number=reference_number.strip(),
                notes=notes.strip(),
                application_date=application_date.isoformat()
            )

            st.success(
                "Application added to your account."
            )

            st.rerun()


    st.divider()

    st.subheader("My Applications")

    applications = get_user_applications(user_id)

    if not applications:

        st.info(
            "No applications found in your account."
        )

        return

    status_options = [
        "Draft",
        "Submitted",
        "Under Review",
        "Documents Required",
        "Approved",
        "Rejected",
        "Completed"
    ]

    for app in applications:

        application_id = app["id"]

        with st.expander(
            f'{app["service_name"]} — {app["status"]}'
        ):

            st.write(
                f'**Reference:** '
                f'{app.get("reference_number", "")}'
            )

            st.write(
                f'**Date:** '
                f'{app.get("application_date", "")}'
            )

            if app.get("notes"):
                st.write(
                    f'**Notes:** {app["notes"]}'
                )

            new_status = st.selectbox(
                "Update Status",
                status_options,
                index=(
                    status_options.index(app["status"])
                    if app["status"] in status_options
                    else 1
                ),
                key=f"status_{application_id}"
            )

            if st.button(
                "Update Status",
                key=f"update_{application_id}",
                use_container_width=True
            ):

                success = update_user_application_status(
                    user_id,
                    application_id,
                    new_status
                )

                if success:
                    st.success(
                        "Application status updated."
                    )
                    st.rerun()
                else:
                    st.error(
                        "Unable to update this application."
                    )


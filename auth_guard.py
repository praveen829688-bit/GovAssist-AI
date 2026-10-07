import streamlit as st

from auth_page import render_auth_page
from session_manager import initialize_auth, logout


def require_login():

    if not initialize_auth():

        render_auth_page()

        return False

    return True


def render_user_sidebar():

    st.sidebar.markdown("---")

    st.sidebar.markdown(
        "**Citizen Account**"
    )

    st.sidebar.write(
        f"👤 {st.session_state.get('user_name', 'Citizen')}"
    )

    st.sidebar.caption(
        st.session_state.get(
            "user_email",
            ""
        )
    )

    if st.sidebar.button(
        "Logout",
        use_container_width=True
    ):
        logout()

    st.sidebar.markdown("---")

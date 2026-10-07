import streamlit as st

from auth import (
    validate_session,
    logout_session
)


def initialize_auth():

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if "session_token" not in st.session_state:
        st.session_state.session_token = None

    if st.session_state.session_token:

        session = validate_session(
            st.session_state.session_token
        )

        if session:

            st.session_state.authenticated = True
            st.session_state.user_id = session["user_id"]
            st.session_state.user_name = session["name"]
            st.session_state.user_email = session["email"]
            st.session_state.user_role = session["role"]

            return True

        else:

            clear_auth()

    return False


def clear_auth():

    token = st.session_state.get(
        "session_token"
    )

    if token:
        logout_session(token)

    keys = [
        "authenticated",
        "session_token",
        "user_id",
        "user_name",
        "user_email",
        "user_role"
    ]

    for key in keys:
        st.session_state.pop(key, None)

    st.session_state.authenticated = False
    st.session_state.session_token = None


def logout():

    clear_auth()
    st.rerun()

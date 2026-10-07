import streamlit as st

from auth import (
    register_user,
    authenticate_user,
    create_session
)


def render_auth_page():

    st.markdown("""
    <style>

    /* =====================================================
       AUTHENTICATION PAGE
       ===================================================== */

    .auth-header {
        text-align: center;
        padding-top: 35px;
        padding-bottom: 20px;
    }

    .auth-logo {
        font-size: 42px;
        font-weight: 800;
        color: #2563eb !important;
        margin-bottom: 5px;
    }

    .auth-subtitle {
        font-size: 17px;
        color: #475569 !important;
    }

    /* Streamlit labels */
    label {
        color: #1e293b !important;
        font-weight: 600 !important;
    }

    /* Input fields */
    div[data-baseweb="input"] {
        background-color: #ffffff !important;
        border: 1px solid #94a3b8 !important;
        border-radius: 10px !important;
    }

    div[data-baseweb="input"] input {
        color: #0f172a !important;
        background-color: #ffffff !important;
        caret-color: #2563eb !important;
    }

    div[data-baseweb="input"] input::placeholder {
        color: #64748b !important;
        opacity: 1 !important;
    }

    /* Password eye button */
    div[data-baseweb="input"] button {
        color: #475569 !important;
        background: transparent !important;
    }

    /* Login / register buttons */
    .stButton > button {
        border-radius: 10px !important;
        min-height: 45px !important;
        font-weight: 700 !important;
        border: 1px solid #2563eb !important;
    }

    /* Tab text */
    button[data-baseweb="tab"] {
        color: #334155 !important;
        font-weight: 600 !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #2563eb !important;
    }

    /* Welcome heading */
    h1, h2, h3, h4 {
        color: #0f172a !important;
    }

    /* Normal text */
    p, span, div {
        color: inherit;
    }

    /* Security information */
    .security-note {
        margin-top: 25px;
        padding: 15px 18px;
        border-radius: 12px;
        background: #eff6ff;
        border: 1px solid #bfdbfe;
        color: #1e3a8a !important;
        font-size: 14px;
        line-height: 1.5;
    }

    .security-note strong {
        color: #1e40af !important;
    }

    /* Help text */
    .stCaption {
        color: #64748b !important;
    }

    /* Remove excessive top blank area */
    .block-container {
        padding-top: 2rem !important;
    }

    /* Main authentication width */
    [data-testid="stVerticalBlock"] {
        color: #0f172a;
    }

    </style>
    """, unsafe_allow_html=True)


    # =========================================================
    # HEADER
    # =========================================================

    st.markdown("""
    <div class="auth-header">
        <div class="auth-logo">GovAssist AI</div>
        <div class="auth-subtitle">
            Secure Government Service Assistant
        </div>
    </div>
    """, unsafe_allow_html=True)


    # =========================================================
    # AUTH TABS
    # =========================================================

    login_tab, register_tab = st.tabs([
        "Login",
        "Create Account"
    ])


    # =========================================================
    # LOGIN
    # =========================================================

    with login_tab:

        st.markdown("## Welcome Back")

        st.caption(
            "Login to access your personalized government services."
        )

        email = st.text_input(
            "Email",
            key="login_email",
            placeholder="citizen@example.com"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_password",
            placeholder="Enter your password"
        )

        if st.button(
            "Login Securely",
            use_container_width=True,
            type="primary"
        ):

            if not email.strip():
                st.warning("Please enter your email address.")

            elif not password:
                st.warning("Please enter your password.")

            else:

                user, message = authenticate_user(
                    email,
                    password
                )

                if user:

                    token = create_session(
                        user["id"]
                    )

                    st.session_state.authenticated = True
                    st.session_state.session_token = token
                    st.session_state.user_id = user["id"]
                    st.session_state.user_name = user["name"]
                    st.session_state.user_email = user["email"]
                    st.session_state.user_role = user["role"]

                    st.success("Login successful.")
                    st.rerun()

                else:
                    st.error(message)


    # =========================================================
    # REGISTER
    # =========================================================

    with register_tab:

        st.markdown("## Create Citizen Account")

        st.caption(
            "Create a secure account to manage your government services."
        )

        name = st.text_input(
            "Full Name",
            key="register_name",
            placeholder="Enter your full name"
        )

        email = st.text_input(
            "Email Address",
            key="register_email",
            placeholder="citizen@example.com"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="register_password",
            placeholder="Minimum 8 characters"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            key="register_confirm",
            placeholder="Re-enter your password"
        )

        st.caption(
            "Password must contain at least 8 characters."
        )

        if st.button(
            "Create Account",
            use_container_width=True,
            type="primary"
        ):

            if not name.strip():
                st.warning("Please enter your full name.")

            elif not email.strip():
                st.warning("Please enter your email address.")

            elif not password:
                st.warning("Please create a password.")

            elif password != confirm_password:
                st.error("Passwords do not match.")

            else:

                success, message = register_user(
                    name,
                    email,
                    password
                )

                if success:
                    st.success(
                        "Account created successfully. "
                        "Please switch to Login."
                    )

                else:
                    st.error(message)


    # =========================================================
    # SECURITY NOTICE
    # =========================================================

    st.markdown("""
    <div class="security-note">
        <strong>🔐 Security Protection</strong><br>
        Your password is protected using PBKDF2-HMAC-SHA256
        with a unique cryptographic salt. Login sessions
        automatically expire after 24 hours.
    </div>
    """, unsafe_allow_html=True)


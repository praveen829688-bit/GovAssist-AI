import streamlit as st

from scheme_engine import (
    find_matching_schemes,
    eligibility_message
)


def render_scheme_finder():

    st.markdown(
        """
        <div class="scheme-hero">
            <div class="scheme-icon">🎯</div>
            <h1>Smart Government Scheme Finder</h1>
            <p>
                Find government schemes that may be relevant to
                your profile and requirements.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.info(
        "This tool provides preliminary matching only. "
        "It does not determine official eligibility."
    )

    st.markdown(
        "### 👤 Tell GovAssist About Yourself"
    )

    col1, col2 = st.columns(2)

    with col1:

        state = st.selectbox(
            "State",
            [
                "Karnataka",
                "Tamil Nadu",
                "Andhra Pradesh",
                "Telangana",
                "Kerala",
                "Maharashtra",
                "Other"
            ]
        )

        age = st.number_input(
            "Age",
            min_value=1,
            max_value=120,
            value=21
        )

        income = st.number_input(
            "Approximate Annual Family Income (₹)",
            min_value=0,
            value=0,
            step=10000
        )

        category = st.selectbox(
            "Category",
            [
                "Not specified",
                "SC",
                "ST",
                "OBC",
                "EWS",
                "General"
            ]
        )

    with col2:

        student = st.checkbox(
            "🎓 I am a student"
        )

        farmer = st.checkbox(
            "🌾 I am a farmer"
        )

        need = st.text_area(
            "What kind of assistance do you need?",
            placeholder=(
                "Example: scholarship for college education, "
                "financial assistance, housing, farming support..."
            )
        )

    find_button = st.button(
        "🎯 Find Relevant Schemes",
        type="primary",
        use_container_width=True
    )

    if not find_button:
        return

    profile = {

        "state": state,

        "age": age,

        "income": income,

        "category": (
            ""
            if category == "Not specified"
            else category
        ),

        "student": student,

        "farmer": farmer,

        "need": need
    }

    with st.spinner(
        "Analyzing available schemes..."
    ):

        results = find_matching_schemes(
            profile
        )

    if not results:

        st.warning(
            "No schemes are currently available "
            "in the GovAssist knowledge base."
        )

        return

    st.markdown(
        "## 🔎 Preliminary Matches"
    )

    shown = False

    for result in results:

        if result["score"] <= 0:
            continue

        shown = True

        scheme = result["data"]

        st.markdown(
            f"""
            <div class="scheme-result">
                <h3>{result['name']}</h3>
                <p>
                    <strong>{eligibility_message(result)}</strong>
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        if result["reasons"]:

            st.markdown(
                "**Why it may be relevant:**"
            )

            for reason in result["reasons"]:

                st.markdown(
                    f"- {reason}"
                )

        # Show useful scheme information
        for key, value in scheme.items():

            if key.lower() in [
                "name",
                "title",
                "scheme"
            ]:
                continue

            if isinstance(
                value,
                (str, int, float)
            ):

                st.markdown(
                    f"**{key.replace('_', ' ').title()}:** {value}"
                )

        st.divider()

    if not shown:

        st.info(
            "No strong preliminary matches were found. "
            "Try describing your requirement more specifically."
        )

    st.warning(
        "⚠️ Important: Scheme matching is an AI-assisted "
        "preliminary recommendation. Always verify the latest "
        "eligibility criteria, documents, deadlines and application "
        "process on the official government portal."
    )

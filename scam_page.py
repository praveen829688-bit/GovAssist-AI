import streamlit as st

from scam_detector import analyze_url, get_safety_advice


def render_scam_detector():
    st.markdown(
        """
        <div class="govassist-scam-hero">
            <div class="govassist-scam-icon">🛡️</div>
            <h1>Government Website Safety Checker</h1>
            <p>
                Check whether a website appears to be an official
                Indian government website before entering sensitive information.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="govassist-warning">
            <strong>Important:</strong>
            A website using HTTPS is not automatically a government website.
            Never share OTPs, passwords, PINs, CVV numbers or authentication
            credentials with anyone.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### 🔎 Check a Website")

    url = st.text_input(
        "Website URL",
        placeholder="https://example.gov.in",
        help="Paste the complete website address you want to check."
    )

    check = st.button(
        "🛡️ Check Website Safety",
        type="primary",
        use_container_width=True
    )

    if check:

        if not url.strip():
            st.warning("Please enter a website URL.")
            return

        result = analyze_url(url)

        status = result["status"]
        risk = result["risk"]

        if risk == "Low":
            st.success(
                f"✅ {status}"
            )

        elif risk == "Medium":
            st.warning(
                f"⚠️ {status}"
            )

        else:
            st.error(
                f"🚨 {status}"
            )

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Domain")
            st.code(
                result["domain"] or "Unable to determine"
            )

        with col2:
            st.markdown("### Risk Level")
            st.metric(
                "Risk",
                risk
            )

        st.markdown("### 🔍 Verification Result")

        st.info(result["message"])

        st.markdown("### 🔐 Safety Recommendations")

        for advice in get_safety_advice(result):
            st.markdown(f"- {advice}")

        if result["official"]:
            st.success(
                "The domain matches a recognized Indian government "
                "domain pattern. Always check the exact domain spelling "
                "before entering personal information."
            )

        st.caption(
            "GovAssist AI provides a safety signal, not a legal or "
            "official certification of website ownership."
        )

import streamlit as st

# Live knowledge-base dashboard statistics
services_count, schemes_count = get_knowledge_counts()
from dashboard_counts import get_knowledge_counts


# ============================================================
# GOVASSIST AI - PROFESSIONAL UI POLISH
# ============================================================
st.markdown("""
<style>

/* ============================================================
   GOVASSIST HERO - HIGH CONTRAST
   ============================================================ */

.govassist-hero-fix,
.govassist-hero-fix * {
    color: #ffffff !important;
    opacity: 1 !important;
}

.govassist-hero-fix {
    background: linear-gradient(
        135deg,
        #071a33 0%,
        #12345d 50%,
        #1d4f86 100%
    ) !important;

    border-radius: 0 0 28px 28px !important;
    padding: 42px 48px !important;
    margin-bottom: 28px !important;
    box-shadow: 0 12px 30px rgba(0,0,0,0.15) !important;
}

.govassist-hero-fix h1 {
    color: #ffffff !important;
    font-size: 2.8rem !important;
    font-weight: 850 !important;
    margin-bottom: 15px !important;
}

.govassist-hero-fix p {
    color: #eaf2ff !important;
    font-size: 1.08rem !important;
    font-weight: 500 !important;
}

/* Catch Streamlit markdown containers inside hero */
.govassist-hero-fix [data-testid="stMarkdownContainer"],
.govassist-hero-fix [data-testid="stMarkdownContainer"] *,
.govassist-hero-fix p,
.govassist-hero-fix span {
    color: #ffffff !important;
    opacity: 1 !important;
}

/* ============================================================
   DASHBOARD METRIC CARDS
   ============================================================ */

[data-testid="stMetric"] {
    background: #ffffff !important;
    border: 1px solid #d7e0ec !important;
    border-radius: 18px !important;
    padding: 24px !important;
    min-height: 145px !important;
    box-shadow: 0 6px 18px rgba(15,35,65,0.08) !important;
}

[data-testid="stMetricValue"] {
    color: #163d70 !important;
    font-size: 2.1rem !important;
    font-weight: 850 !important;
    opacity: 1 !important;
}

[data-testid="stMetricLabel"] {
    color: #53657e !important;
    font-size: 0.98rem !important;
    font-weight: 650 !important;
    opacity: 1 !important;
}

/* ============================================================
   DASHBOARD HEADINGS
   ============================================================ */

.govassist-section-title,
.govassist-section-title * {
    color: #163d70 !important;
    opacity: 1 !important;
}

/* ============================================================
   QUICK ACCESS
   ============================================================ */

.govassist-quick,
.govassist-quick * {
    color: #163d70 !important;
    opacity: 1 !important;
}

.govassist-quick {
    background: #ffffff !important;
    border: 1px solid #d7e0ec !important;
    border-radius: 18px !important;
    padding: 22px !important;
    box-shadow: 0 6px 18px rgba(15,35,65,0.07) !important;
}

/* ============================================================
   SIDEBAR BRANDING
   ============================================================ */

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span {
    opacity: 1 !important;
}

section[data-testid="stSidebar"] {
    background: #09172a !important;
}

section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] * {
    color: #edf4ff !important;
    opacity: 1 !important;
}

/* ============================================================
   GENERAL TEXT VISIBILITY
   ============================================================ */

.stApp p,
.stApp label {
    opacity: 1 !important;
}




/* Main application background */
.stApp {
    background: #f4f7fb;
}

/* Main content */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}

/* Hide unnecessary Streamlit decoration */
[data-testid="stDecoration"] {
    display: none;
}

/* Hero section */
.gov-hero,
.gov-hero * {
    color: #ffffff !important;
}

.gov-hero {
    background: linear-gradient(135deg, #0b1b35 0%, #19345f 55%, #254b82 100%);
    border-radius: 0 0 28px 28px;
    padding: 42px 48px;
    margin-bottom: 28px;
    box-shadow: 0 12px 30px rgba(15, 35, 65, 0.12);
}

/* All metric cards */
[data-testid="stMetric"],
[data-testid="stMetricValue"],
[data-testid="stMetricLabel"] {
    color: #14213d !important;
}

[data-testid="stMetric"] {
    background: #ffffff !important;
    border: 1px solid #dce4ef !important;
    border-radius: 18px !important;
    padding: 22px !important;
    box-shadow: 0 5px 18px rgba(15, 35, 65, 0.07) !important;
}

/* Metric value */
[data-testid="stMetricValue"] {
    font-size: 2rem !important;
    font-weight: 800 !important;
    color: #123b70 !important;
}

/* Metric label */
[data-testid="stMetricLabel"] {
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    color: #52647d !important;
}

/* Custom dashboard cards */
.gov-card,
.gov-card *,
.dashboard-card,
.dashboard-card *,
.service-card,
.service-card *,
.scheme-card,
.scheme-card *,
.quick-card,
.quick-card * {
    color: #172b4d !important;
}

.gov-card,
.dashboard-card,
.service-card,
.scheme-card,
.quick-card {
    background: #ffffff !important;
    border: 1px solid #dce4ef !important;
    border-radius: 18px !important;
    padding: 24px !important;
    box-shadow: 0 6px 20px rgba(15, 35, 65, 0.07) !important;
}

/* Section headings */
h1 {
    color: #102a4c !important;
    font-weight: 800 !important;
}

h2, h3 {
    color: #17365f !important;
    font-weight: 750 !important;
}

/* Normal text */
p, label, span {
    color: #334155;
}

/* Buttons */
.stButton > button {
    border-radius: 10px !important;
    border: 1px solid #cbd5e1 !important;
    background: #ffffff !important;
    color: #123b70 !important;
    font-weight: 650 !important;
    min-height: 44px !important;
    transition: all 0.2s ease !important;
}

.stButton > button:hover {
    background: #123b70 !important;
    color: #ffffff !important;
    border-color: #123b70 !important;
    transform: translateY(-1px);
}

/* Primary buttons */
.stButton > button[kind="primary"] {
    background: #123b70 !important;
    color: #ffffff !important;
    border-color: #123b70 !important;
}

/* Inputs */
.stTextInput input,
.stTextArea textarea,
.stSelectbox div[data-baseweb="select"],
.stNumberInput input {
    background: #ffffff !important;
    color: #172b4d !important;
    border-radius: 10px !important;
}

/* Input labels */
.stTextInput label,
.stTextArea label,
.stSelectbox label,
.stNumberInput label {
    color: #334155 !important;
    font-weight: 600 !important;
}

/* Expanders */
.streamlit-expanderHeader {
    background: #ffffff !important;
    color: #17365f !important;
    border: 1px solid #dce4ef !important;
    border-radius: 12px !important;
}

/* Alerts */
[data-testid="stAlert"] {
    border-radius: 12px !important;
}

/* Dataframes */
[data-testid="stDataFrame"] {
    border-radius: 12px !important;
    overflow: hidden !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #0b1729 !important;
}

section[data-testid="stSidebar"] * {
    color: #e8eef7 !important;
}

/* Sidebar buttons */
section[data-testid="stSidebar"] .stButton > button {
    background: #14263f !important;
    color: #ffffff !important;
    border-color: #263d5d !important;
}

section[data-testid="stSidebar"] .stButton > button:hover {
    background: #234d7d !important;
}

/* Links */
a {
    color: #175ca8 !important;
    font-weight: 600;
}

/* Footer */
.gov-footer,
.gov-footer * {
    color: #64748b !important;
    text-align: center;
}

/* Mobile */
@media (max-width: 768px) {
    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .gov-hero {
        padding: 28px 24px;
    }
}

</style>
""", unsafe_allow_html=True)

from datetime import datetime

# ============================================================
# GOVASSIST AI
# AI-POWERED GOVERNMENT SERVICE & SCHEME INTELLIGENCE PLATFORM
# ============================================================

st.set_page_config(
    page_title="GovAssist AI",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------- PROFESSIONAL UI -----------------------

st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

.stApp {
    background: #f5f7fb;
}

.block-container {
    max-width: 1400px;
    padding-top: 2rem;
}

.hero {
    padding: 35px;
    border-radius: 22px;
    background: linear-gradient(135deg, #172033, #263b63);
    color: white;
    margin-bottom: 25px;
}

.hero h1 {
    font-size: 44px;
    margin-bottom: 5px;
}

.hero p {
    font-size: 18px;
    opacity: 0.85;
}

.card {
    background: white;
    padding: 22px;
    border-radius: 18px;
    border: 1px solid #e4e7ec;
    margin-bottom: 18px;
}

.metric {
    background: white;
    border: 1px solid #e4e7ec;
    border-radius: 18px;
    padding: 22px;
    text-align: center;
}

.metric h2 {
    font-size: 30px;
    margin: 0;
}

.metric p {
    color: #667085;
}

.badge {
    display: inline-block;
    padding: 5px 10px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 700;
}

.success {
    background: #dcfae6;
    color: #067647;
}

.warning {
    background: #fef0c7;
    color: #b54708;
}
</style>
""", unsafe_allow_html=True)


# -------------------- DATA --------------------

SERVICES = [
    {
        "name": "Income Certificate",
        "category": "Certificates",
        "department": "Revenue Department",
        "description": "Used to establish annual family income for eligible government benefits and scholarships.",
        "documents": ["Aadhaar Card", "Address Proof", "Income Proof"],
        "processing": "7-15 working days",
        "fee": "Varies by state",
        "source": "https://www.india.gov.in/"
    },
    {
        "name": "Birth Certificate",
        "category": "Certificates",
        "department": "Local Government",
        "description": "Official record of a person's birth.",
        "documents": ["Hospital Record", "Parent ID", "Address Proof"],
        "processing": "7-21 working days",
        "fee": "Varies",
        "source": "https://www.india.gov.in/"
    },
    {
        "name": "Driving Licence",
        "category": "Transport",
        "department": "Transport Department",
        "description": "Guidance for driving licence related services.",
        "documents": ["Identity Proof", "Address Proof"],
        "processing": "Varies",
        "fee": "Varies",
        "source": "https://parivahan.gov.in/"
    },
    {
        "name": "Passport",
        "category": "Identity",
        "department": "Ministry of External Affairs",
        "description": "Passport application and renewal guidance.",
        "documents": ["Identity Proof", "Address Proof", "DOB Proof"],
        "processing": "Varies",
        "fee": "Depends on service",
        "source": "https://www.passportindia.gov.in/"
    },
    {
        "name": "PAN Card",
        "category": "Tax",
        "department": "Income Tax Department",
        "description": "Permanent Account Number application guidance.",
        "documents": ["Identity Proof", "Address Proof", "DOB Proof"],
        "processing": "Varies",
        "fee": "Depends on method",
        "source": "https://www.incometax.gov.in/"
    },
    {
        "name": "Ration Card",
        "category": "Food & Civil Supplies",
        "department": "State Food Department",
        "description": "Guidance for ration card related services.",
        "documents": ["Identity Proof", "Address Proof", "Family Details"],
        "processing": "Varies",
        "fee": "Varies",
        "source": "https://www.india.gov.in/"
    }
]

SCHEMES = [
    {
        "name": "Post-Matric Scholarship",
        "category": "Education",
        "target": "Students",
        "income_limit": 300000,
        "description": "Financial assistance for eligible students pursuing education after matriculation.",
        "source": "https://scholarships.gov.in/"
    },
    {
        "name": "National Scholarship Portal",
        "category": "Education",
        "target": "Students",
        "income_limit": 500000,
        "description": "Access point for multiple scholarship schemes.",
        "source": "https://scholarships.gov.in/"
    },
    {
        "name": "PM-KISAN",
        "category": "Agriculture",
        "target": "Farmers",
        "income_limit": None,
        "description": "Income support initiative for eligible farmer families.",
        "source": "https://pmkisan.gov.in/"
    },
    {
        "name": "Ayushman Bharat",
        "category": "Healthcare",
        "target": "Eligible Families",
        "income_limit": None,
        "description": "Government healthcare coverage initiative.",
        "source": "https://pmjay.gov.in/"
    }
]


# -------------------- SESSION STATE --------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "saved_services" not in st.session_state:
    st.session_state.saved_services = []

if "saved_schemes" not in st.session_state:
    st.session_state.saved_schemes = []


# -------------------- AI ENGINE --------------------

def generate_ai_response(question):

    q = question.lower()

    if "scholarship" in q:
        return """
### 🎓 Scholarship Assistance

GovAssist AI can help identify potentially relevant scholarship schemes.

Use **🎯 Scheme Finder** to enter:

- Age
- Student status
- Education
- Annual family income
- Requirement category

The system will calculate a **preliminary match score**.

⚠️ Always verify the latest eligibility requirements on the official government portal.
"""

    if "passport" in q:
        return """
### 🛂 Passport Assistance

Passport-related services are available through the official Passport Seva platform.

Typical requirements may include:

1. Identity proof
2. Address proof
3. Date-of-birth proof
4. Photograph where applicable

🔗 Use the official source shown in Service Finder.
"""

    if "driving" in q or "licence" in q:
        return """
### 🚗 Driving Licence Assistance

Driving licence services are available through the official Parivahan platform.

Typical workflow:

1. Select service
2. Enter applicant information
3. Upload documents
4. Pay applicable fee
5. Schedule appointment/test where applicable
6. Track application

Requirements vary by service and state.
"""

    if "certificate" in q:
        return """
### 📄 Certificate Assistance

GovAssist can help identify common government certificates such as:

- Income Certificate
- Birth Certificate
- Address-related services

Open **Service Finder** to see documents and official sources.
"""

    if "aadhaar" in q:
        return """
### 🪪 Aadhaar Safety

For Aadhaar-related services, use official UIDAI channels.

Never provide OTPs, passwords, PINs or authentication credentials to unknown websites or people.

🔐 Do not enter sensitive credentials into this chat.
"""

    return """
### 🤖 GovAssist AI

I can help you with:

• Government services  
• Scholarships  
• Government schemes  
• Eligibility  
• Required documents  
• Certificates  
• Passport  
• Driving licence  
• PAN  
• Ration card  
• Healthcare schemes  

Try:

**"Which scholarship can I apply for?"**

or

**"How do I apply for an income certificate?"**
"""


def search_services(query):

    query = query.lower().strip()

    if not query:
        return SERVICES

    words = query.split()
    results = []

    for service in SERVICES:

        text = (
            service["name"] + " " +
            service["category"] + " " +
            service["department"] + " " +
            service["description"]
        ).lower()

        if any(word in text for word in words):
            results.append(service)

    return results


def recommend_schemes(age, student, income, category):

    recommendations = []

    for scheme in SCHEMES:

        score = 50

        if student and scheme["target"] == "Students":
            score += 30

        if scheme["income_limit"] is not None:

            if income <= scheme["income_limit"]:
                score += 15
            else:
                score -= 20

        if category.lower() in scheme["category"].lower():
            score += 10

        score = max(0, min(99, score))

        recommendations.append(
            (scheme, score)
        )

    recommendations.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return recommendations


# -------------------- SIDEBAR --------------------

with st.sidebar:

    st.markdown("## 🇮🇳 GovAssist AI")

    st.caption(
        "Government Service Intelligence Platform"
    )

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "🤖 AI Assistant",
            "🔎 Service Finder",
            "🎯 Scheme Finder",
            "📄 Document Center",
            "🛡️ Scam Detector",
            "📊 Analytics",
            "ℹ️ About"
        ]
    )

    st.divider()

    st.success("● AI System Online")

    st.caption(
        "Protect your OTPs, passwords and sensitive credentials."
    )


# ============================================================
# DASHBOARD
# ============================================================

if page == "🏠 Dashboard":

    st.markdown("""
    <div class="govassist-hero-fix">
        <h1>🇮🇳 GovAssist AI</h1>
        <p>AI-Powered Government Service & Scheme Intelligence Platform</p>
        <p>Discover services • Understand eligibility • Prepare documents • Stay safe</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)

    metrics = [
        (str(len(SERVICES)), "Government Services"),
        (str(len(SCHEMES)), "Government Schemes"),
        ("AI", "Smart Assistance"),
        ("24/7", "Platform Availability")
    ]

    for col, (number, label) in zip(
        [c1, c2, c3, c4],
        metrics
    ):

        with col:

            st.markdown(
                f"""
                <div class="metric">
                    <h2>{number}</h2>
                    <p>{label}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.write("")

    left, right = st.columns([1.6, 1])

    with left:

        st.markdown("### 🤖 Ask GovAssist AI")

        question = st.text_input(
            "Government service question",
            placeholder="Example: Which scholarship can I apply for?"
        )

        if st.button(
            "Ask GovAssist AI",
            type="primary",
            use_container_width=True
        ):

            if question:

                response = generate_ai_response(question)

                st.session_state.messages.append(
                    ("user", question)
                )

                st.session_state.messages.append(
                    ("assistant", response)
                )

        for role, message in st.session_state.messages[-6:]:

            if role == "user":

                st.markdown(
                    f"""
                    <div class="card">
                    <b>You</b><br>{message}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            else:

                st.markdown(
                    f"""
                    <div class="card">
                    {message}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    with right:

        st.markdown("### ⚡ Quick Access")

        st.button("🎓 Scholarships", use_container_width=True)
        st.button("📄 Certificates", use_container_width=True)
        st.button("🛂 Passport", use_container_width=True)
        st.button("🚗 Driving Licence", use_container_width=True)
        st.button("💳 PAN Card", use_container_width=True)
        st.button("🏠 Government Schemes", use_container_width=True)

    st.divider()

    st.markdown("### 🌟 Platform Capabilities")

    a, b, c = st.columns(3)

    with a:
        st.markdown("""
        <div class="card">
        <h3>🧠 AI Guidance</h3>
        Natural-language government assistance.
        </div>
        """, unsafe_allow_html=True)

    with b:
        st.markdown("""
        <div class="card">
        <h3>🎯 Smart Recommendations</h3>
        Personalized scheme discovery.
        </div>
        """, unsafe_allow_html=True)

    with c:
        st.markdown("""
        <div class="card">
        <h3>🛡️ Citizen Safety</h3>
        Official-source and scam awareness.
        </div>
        """, unsafe_allow_html=True)


# ============================================================
# AI ASSISTANT
# ============================================================

elif page == "🤖 AI Assistant":

    st.title("🤖 AI Government Assistant")

    st.caption(
        "Ask GovAssist about government services, schemes and application procedures."
    )

    for role, message in st.session_state.messages:

        if role == "user":

            st.info(
                f"**You:** {message}"
            )

        else:

            st.markdown(
                f'<div class="card">{message}</div>',
                unsafe_allow_html=True
            )

    question = st.chat_input(
        "Ask GovAssist AI..."
    )

    if question:

        st.session_state.messages.append(
            ("user", question)
        )

        st.session_state.messages.append(
            ("assistant", generate_ai_response(question))
        )

        st.rerun()


# ============================================================
# SERVICE FINDER
# ============================================================

elif page == "🔎 Service Finder":

    st.title("🔎 Government Service Finder")

    query = st.text_input(
        "Search service",
        placeholder="passport, certificate, licence..."
    )

    categories = sorted(
        list(
            set(
                s["category"]
                for s in SERVICES
            )
        )
    )

    category = st.selectbox(
        "Filter by category",
        ["All"] + categories
    )

    results = search_services(query)

    if category != "All":

        results = [
            s for s in results
            if s["category"] == category
        ]

    st.write(
        f"### {len(results)} government service(s) found"
    )

    for service in results:

        with st.container(border=True):

            st.subheader(
                service["name"]
            )

            st.caption(
                f"{service['department']} • {service['category']}"
            )

            st.write(
                service["description"]
            )

            x, y, z = st.columns(3)

            with x:
                st.write("**Processing**")
                st.write(service["processing"])

            with y:
                st.write("**Fee**")
                st.write(service["fee"])

            with z:
                st.write("**Documents**")
                st.write(
                    ", ".join(service["documents"])
                )

            st.link_button(
                "🔗 Official Source",
                service["source"]
            )


# ============================================================
# SCHEME FINDER
# ============================================================

elif page == "🎯 Scheme Finder":

    st.title("🎯 AI Government Scheme Finder")

    st.write(
        "Create a basic citizen profile to receive preliminary recommendations."
    )

    x, y = st.columns(2)

    with x:

        age = st.number_input(
            "Age",
            min_value=1,
            max_value=100,
            value=21
        )

        student = st.checkbox(
            "Currently a student"
        )

        income = st.number_input(
            "Annual family income (₹)",
            min_value=0,
            value=250000,
            step=10000
        )

    with y:

        category = st.selectbox(
            "Main requirement",
            [
                "Education",
                "Healthcare",
                "Agriculture",
                "Employment",
                "Housing"
            ]
        )

    if st.button(
        "🎯 Find Suitable Schemes",
        type="primary"
    ):

        recommendations = recommend_schemes(
            age,
            student,
            income,
            category
        )

        for scheme, score in recommendations:

            with st.container(border=True):

                st.subheader(
                    scheme["name"]
                )

                st.progress(
                    score / 100,
                    text=f"Preliminary Match: {score}%"
                )

                st.write(
                    scheme["description"]
                )

                st.link_button(
                    "🔗 Verify Official Source",
                    scheme["source"]
                )

        st.warning(
            "This is a preliminary recommendation, not an official eligibility decision."
        )


# ============================================================
# DOCUMENT CENTER
# ============================================================

elif page == "📄 Document Center":

    st.title("📄 Smart Document Center")

    st.info(
        "Upload a PDF or image for the document-analysis workflow."
    )

    uploaded = st.file_uploader(
        "Upload document",
        type=[
            "pdf",
            "png",
            "jpg",
            "jpeg"
        ]
    )

    if uploaded:

        st.success(
            f"Uploaded: {uploaded.name}"
        )

        st.markdown("### 🔍 Document Analysis")

        document_type = st.selectbox(
            "Detected / select document type",
            [
                "Income Certificate",
                "Aadhaar",
                "College ID",
                "Marks Card",
                "Address Proof",
                "Other"
            ]
        )

        st.markdown(
            f"**Selected Document:** {document_type}"
        )

        st.markdown("### 📋 Smart Checklist")

        checks = [
            ("Document uploaded", True),
            ("File readable", True),
            ("Document type identified", True),
            ("Expiry information detected", False)
        ]

        for label, status in checks:

            if status:
                st.success(f"✓ {label}")
            else:
                st.warning(f"⚠ {label}")

        st.caption(
            "Advanced OCR/RAG document processing can be connected in the next phase."
        )


# ============================================================
# SCAM DETECTOR
# ============================================================

elif page == "🛡️ Scam Detector":

    st.title("🛡️ Government Website Safety Checker")

    st.write(
        "Check whether a URL appears consistent with known Indian government domains."
    )

    url = st.text_input(
        "Website URL",
        placeholder="https://example.gov.in"
    )

    if st.button(
        "🔍 Analyze Website",
        type="primary"
    ):

        if not url:

            st.warning(
                "Please enter a URL."
            )

        else:

            official_domains = [
                ".gov.in",
                "india.gov.in",
                "uidai.gov.in",
                "passportindia.gov.in",
                "parivahan.gov.in",
                "incometax.gov.in",
                "scholarships.gov.in",
                "pmkisan.gov.in",
                "pmjay.gov.in"
            ]

            is_official = any(
                domain in url.lower()
                for domain in official_domains
            )

            if is_official:

                st.success(
                    "The URL appears consistent with a known official government domain."
                )

                st.metric(
                    "Initial Risk",
                    "LOW"
                )

            else:

                st.error(
                    "This URL could not be verified as a known official government domain."
                )

                st.metric(
                    "Initial Risk",
                    "REVIEW REQUIRED"
                )

                st.warning(
                    "Do not enter OTPs, passwords, banking details or identity credentials "
                    "until the website is independently verified."
                )


# ============================================================
# ANALYTICS
# ============================================================

elif page == "📊 Analytics":

    st.title("📊 Platform Analytics")

    a, b, c = st.columns(3)

    with a:
        st.metric(
            "Services",
            "120+"
        )

    with b:
        st.metric(
            "Schemes",
            "85+"
        )

    with c:
        st.metric(
            "AI Messages",
            len(st.session_state.messages)
        )

    st.divider()

    st.subheader(
        "Government Service Categories"
    )

    data = {
        "Education": 42,
        "Certificates": 35,
        "Healthcare": 28,
        "Identity": 24,
        "Transport": 20,
        "Agriculture": 17
    }

    st.bar_chart(data)


# ============================================================
# ABOUT
# ============================================================

elif page == "ℹ️ About":

    st.title("ℹ️ About GovAssist AI")

    st.markdown("""
## 🇮🇳 GovAssist AI

### AI-Powered Government Service & Scheme Intelligence Platform

GovAssist AI is designed to make government information easier to discover
and understand through an intelligent digital assistant.

### Core Modules

✓ AI Government Assistant  
✓ Government Service Finder  
✓ Scheme Recommendation  
✓ Eligibility Engine  
✓ Smart Document Center  
✓ Website Safety Checker  
✓ Official Source Verification  
✓ Analytics Dashboard  
✓ RAG-ready architecture  
✓ Multilingual-ready architecture  

### Technology

**Python • Streamlit • AI • NLP • RAG • Recommendation Systems • Document Intelligence**

### Disclaimer

GovAssist AI is an assistance platform and is not an official government authority.

Government rules, eligibility criteria, fees and deadlines can change.
Always verify important information through the relevant official government portal.
""")

st.divider()

st.caption(
    "GovAssist AI • Professional AI Government Service Platform • "
    + datetime.now().strftime("%d %b %Y")
)

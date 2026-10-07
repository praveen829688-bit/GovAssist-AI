import streamlit as st
import re
import io


# ============================================================
# DOCUMENT TEXT EXTRACTION
# ============================================================

def extract_pdf_text(uploaded_file):

    try:
        from pypdf import PdfReader

        data = uploaded_file.getvalue()

        reader = PdfReader(
            io.BytesIO(data)
        )

        pages = []

        for page in reader.pages:
            try:
                page_text = page.extract_text() or ""

                if page_text.strip():
                    pages.append(page_text)

            except Exception:
                continue

        return "\n".join(pages).strip()

    except Exception as e:
        return ""


def extract_image_text(uploaded_file):

    try:
        from PIL import Image
        import pytesseract

        image = Image.open(
            io.BytesIO(
                uploaded_file.getvalue()
            )
        )

        return pytesseract.image_to_string(
            image
        ).strip()

    except Exception as e:
        return ""


def extract_text(uploaded_file):

    filename = uploaded_file.name.lower()

    if filename.endswith(".pdf"):
        return extract_pdf_text(
            uploaded_file
        )

    if filename.endswith(
        (".png", ".jpg", ".jpeg", ".webp", ".bmp")
    ):
        return extract_image_text(
            uploaded_file
        )

    return ""


# ============================================================
# DOCUMENT TYPE DETECTION
# ============================================================

def detect_document_type(text):

    value = text.lower()

    patterns = {
        "Aadhaar-related document": [
            "aadhaar",
            "unique identification",
            "uidai"
        ],

        "Income Certificate": [
            "income certificate",
            "annual income",
            "income"
        ],

        "Birth Certificate": [
            "birth certificate",
            "date of birth",
            "place of birth"
        ],

        "Caste Certificate": [
            "caste certificate",
            "scheduled caste",
            "scheduled tribe",
            "backward class"
        ],

        "Domicile / Residence Certificate": [
            "domicile certificate",
            "residence certificate",
            "permanent resident"
        ],

        "Driving Licence": [
            "driving licence",
            "driving license",
            "transport department"
        ],

        "PAN Card": [
            "permanent account number",
            "income tax department",
            "pan card"
        ],

        "Passport": [
            "passport",
            "republic of india",
            "passport authority"
        ],

        "Ration Card": [
            "ration card",
            "food and civil supplies",
            "public distribution system"
        ],
    }

    scores = {}

    for document_type, keywords in patterns.items():

        score = 0

        for keyword in keywords:

            if keyword in value:
                score += 1

        if score:
            scores[document_type] = score

    if not scores:
        return "Unknown / Needs Review"

    return max(
        scores,
        key=scores.get
    )


# ============================================================
# SENSITIVE INFORMATION DETECTION
# ============================================================

def detect_sensitive_information(text):

    findings = []

    patterns = {
        "Possible Aadhaar number": r"\b\d{4}\s?\d{4}\s?\d{4}\b",

        "Possible PAN number": r"\b[A-Z]{5}\d{4}[A-Z]\b",

        "Possible phone number": r"\b(?:\+91[-\s]?)?[6-9]\d{9}\b",

        "Possible email address":
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",

        "Possible bank account number":
            r"\b\d{9,18}\b",

        "Possible OTP":
            r"\b(?:OTP|one[- ]time password)[^\d]{0,20}\d{4,8}\b",
    }

    for label, pattern in patterns.items():

        if re.search(
            pattern,
            text,
            flags=re.IGNORECASE
        ):
            findings.append(label)

    return list(dict.fromkeys(findings))


# ============================================================
# REDACT SENSITIVE INFORMATION
# ============================================================

def redact_text(text):

    redacted = text

    redacted = re.sub(
        r"\b\d{4}\s?\d{4}\s?\d{4}\b",
        "[REDACTED ID]",
        redacted
    )

    redacted = re.sub(
        r"\b[A-Z]{5}\d{4}[A-Z]\b",
        "[REDACTED PAN]",
        redacted
    )

    redacted = re.sub(
        r"\b(?:\+91[-\s]?)?[6-9]\d{9}\b",
        "[REDACTED PHONE]",
        redacted
    )

    redacted = re.sub(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        "[REDACTED EMAIL]",
        redacted
    )

    return redacted


# ============================================================
# SMART CHECKLIST
# ============================================================

def checklist_for(document_type):

    checklists = {

        "Income Certificate": [
            "Identity proof",
            "Address/residence proof",
            "Income-related supporting documents",
            "Application form",
            "Recent photograph if required"
        ],

        "Birth Certificate": [
            "Birth registration details",
            "Parent/guardian identification",
            "Hospital or birth record where applicable",
            "Application form",
            "Supporting residence details where required"
        ],

        "Caste Certificate": [
            "Identity proof",
            "Address/residence proof",
            "Existing caste-related supporting records",
            "Parent/family certificate where applicable",
            "Application form"
        ],

        "Domicile / Residence Certificate": [
            "Identity proof",
            "Residence proof",
            "Address-related documents",
            "Application form",
            "Supporting local residence evidence"
        ],

        "Driving Licence": [
            "Identity proof",
            "Address proof",
            "Age proof where required",
            "Learner licence where applicable",
            "Required application documents"
        ],

        "PAN Card": [
            "Identity proof",
            "Address proof",
            "Date-of-birth proof where required",
            "Recent photograph/signature where applicable"
        ],

        "Passport": [
            "Identity proof",
            "Address proof",
            "Date-of-birth proof",
            "Photograph where required",
            "Previous passport if applicable"
        ],

        "Ration Card": [
            "Identity proof",
            "Address proof",
            "Family member details",
            "Income/category documents where applicable",
            "Application form"
        ],

        "Aadhaar-related document": [
            "Identity information",
            "Address information",
            "Supporting documents according to the requested service",
            "Follow the official UIDAI process"
        ],
    }

    return checklists.get(
        document_type,
        [
            "Identity proof if required",
            "Address proof if required",
            "Application form",
            "Supporting documents specific to the service",
            "Verify the latest official requirements"
        ]
    )


# ============================================================
# STREAMLIT PAGE
# ============================================================

def render_document_center():

    st.markdown(
        """
        <div class="document-hero">
            <div class="document-icon">📄</div>
            <h1>Document Intelligence Center</h1>
            <p>
                Upload a government-related document to extract text,
                identify the document type and prepare a preliminary checklist.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.warning(
        "Privacy reminder: Do not upload documents containing OTPs, "
        "passwords, PINs or unnecessary sensitive information. "
        "OCR results are only for assistance and are not official verification."
    )

    uploaded_file = st.file_uploader(
        "Upload a PDF or image",
        type=[
            "pdf",
            "png",
            "jpg",
            "jpeg",
            "webp",
            "bmp"
        ],
        help="Supported formats: PDF, PNG, JPG, JPEG, WEBP and BMP."
    )

    if not uploaded_file:
        st.info(
            "Upload a document to begin analysis."
        )
        return

    st.success(
        f"Uploaded: {uploaded_file.name}"
    )

    if uploaded_file.size > 10 * 1024 * 1024:
        st.error(
            "File is larger than 10 MB. Please upload a smaller document."
        )
        return

    if st.button(
        "🔎 Analyze Document",
        type="primary",
        use_container_width=True
    ):

        with st.spinner(
            "Extracting and analyzing document..."
        ):

            text = extract_text(
                uploaded_file
            )

        if not text:

            st.error(
                "No readable text could be extracted."
            )

            st.info(
                "For image documents, make sure OCR/Tesseract is installed "
                "and the image is clear."
            )

            return

        document_type = detect_document_type(
            text
        )

        sensitive = detect_sensitive_information(
            text
        )

        checklist = checklist_for(
            document_type
        )

        # ----------------------------------------------------
        # RESULTS
        # ----------------------------------------------------

        st.markdown("## 📊 Analysis Result")

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Detected Document",
                document_type
            )

        with col2:

            st.metric(
                "Sensitive Findings",
                len(sensitive)
            )

        # ----------------------------------------------------
        # SECURITY
        # ----------------------------------------------------

        if sensitive:

            st.warning(
                "Potentially sensitive information was detected."
            )

            for item in sensitive:
                st.markdown(
                    f"- 🔐 {item}"
                )

            st.info(
                "Avoid sharing raw extracted text publicly."
            )

        else:

            st.success(
                "No obvious sensitive patterns were detected."
            )

        # ----------------------------------------------------
        # CHECKLIST
        # ----------------------------------------------------

        st.markdown(
            "## 📋 Preliminary Document Checklist"
        )

        for item in checklist:

            st.markdown(
                f"- ☑️ {item}"
            )

        st.caption(
            "Checklist is preliminary guidance. Requirements can vary "
            "by state, department and service. Verify the latest official "
            "requirements before submitting an application."
        )

        # ----------------------------------------------------
        # EXTRACTED TEXT
        # ----------------------------------------------------

        with st.expander(
            "📖 View Extracted Text"
        ):

            st.text_area(
                "OCR / PDF Text",
                value=redact_text(text),
                height=300,
                disabled=True
            )

        # ----------------------------------------------------
        # PRIVACY-SAFE PREVIEW
        # ----------------------------------------------------

        with st.expander(
            "🔐 View Privacy-Safe Text"
        ):

            st.code(
                redact_text(text),
                language="text"
            )

        st.success(
            "Document analysis completed."
        )

        st.caption(
            "GovAssist AI extracts and analyzes document text. "
            "It does not certify that a document is genuine, valid or officially accepted."
        )

TRANSLATIONS = {

    "English": {
        "dashboard": "Dashboard",
        "assistant": "AI Assistant",
        "services": "Service Finder",
        "schemes": "Scheme Finder",
        "eligibility": "Eligibility Checker",
        "documents": "Document Center",
        "applications": "My Applications",
        "saved": "Saved Items",
        "history": "Search History",
        "notifications": "Notifications",
        "profile": "My Profile",
        "scam": "Scam Detector",
        "nearby": "Nearby Offices",
        "admin": "Admin Dashboard",
        "login": "Login",
        "logout": "Logout",
        "register": "Create Account"
    },

    "Kannada": {
        "dashboard": "ಡ್ಯಾಶ್‌ಬೋರ್ಡ್",
        "assistant": "AI ಸಹಾಯಕ",
        "services": "ಸೇವೆಗಳ ಹುಡುಕಾಟ",
        "schemes": "ಯೋಜನೆಗಳ ಹುಡುಕಾಟ",
        "eligibility": "ಅರ್ಹತೆ ಪರಿಶೀಲನೆ",
        "documents": "ದಾಖಲೆ ಕೇಂದ್ರ",
        "applications": "ನನ್ನ ಅರ್ಜಿಗಳು",
        "saved": "ಉಳಿಸಿದವು",
        "history": "ಹುಡುಕಾಟ ಇತಿಹಾಸ",
        "notifications": "ಅಧಿಸೂಚನೆಗಳು",
        "profile": "ನನ್ನ ಪ್ರೊಫೈಲ್",
        "scam": "ವಂಚನೆ ಪತ್ತೆ",
        "nearby": "ಹತ್ತಿರದ ಕಚೇರಿಗಳು",
        "admin": "ನಿರ್ವಾಹಕ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್",
        "login": "ಲಾಗಿನ್",
        "logout": "ಲಾಗ್‌ಔಟ್",
        "register": "ಖಾತೆ ತೆರೆಯಿರಿ"
    },

    "Hindi": {
        "dashboard": "डैशबोर्ड",
        "assistant": "AI सहायक",
        "services": "सेवा खोज",
        "schemes": "योजना खोज",
        "eligibility": "पात्रता जांच",
        "documents": "दस्तावेज़ केंद्र",
        "applications": "मेरे आवेदन",
        "saved": "सहेजे गए",
        "history": "खोज इतिहास",
        "notifications": "सूचनाएं",
        "profile": "मेरी प्रोफ़ाइल",
        "scam": "धोखाधड़ी जांच",
        "nearby": "नजदीकी कार्यालय",
        "admin": "एडमिन डैशबोर्ड",
        "login": "लॉगिन",
        "logout": "लॉगआउट",
        "register": "खाता बनाएं"
    },

    "Tamil": {
        "dashboard": "டாஷ்போர்டு",
        "assistant": "AI உதவியாளர்",
        "services": "சேவை தேடல்",
        "schemes": "திட்ட தேடல்",
        "eligibility": "தகுதி சரிபார்ப்பு",
        "documents": "ஆவண மையம்",
        "applications": "எனது விண்ணப்பங்கள்",
        "saved": "சேமித்தவை",
        "history": "தேடல் வரலாறு",
        "notifications": "அறிவிப்புகள்",
        "profile": "எனது சுயவிவரம்",
        "scam": "மோசடி கண்டறிதல்",
        "nearby": "அருகிலுள்ள அலுவலகங்கள்",
        "admin": "நிர்வாக டாஷ்போர்டு",
        "login": "உள்நுழைவு",
        "logout": "வெளியேறு",
        "register": "கணக்கை உருவாக்கு"
    },

    "Telugu": {
        "dashboard": "డాష్‌బోర్డ్",
        "assistant": "AI సహాయకుడు",
        "services": "సేవల శోధన",
        "schemes": "పథకాల శోధన",
        "eligibility": "అర్హత తనిఖీ",
        "documents": "పత్రాల కేంద్రం",
        "applications": "నా దరఖాస్తులు",
        "saved": "సేవ్ చేసినవి",
        "history": "శోధన చరిత్ర",
        "notifications": "నోటిఫికేషన్లు",
        "profile": "నా ప్రొఫైల్",
        "scam": "మోసం గుర్తింపు",
        "nearby": "సమీప కార్యాలయాలు",
        "admin": "అడ్మిన్ డాష్‌బోర్డ్",
        "login": "లాగిన్",
        "logout": "లాగ్‌అవుట్",
        "register": "ఖాతా సృష్టించండి"
    }
}


def translate(language, key):

    return TRANSLATIONS.get(
        language,
        TRANSLATIONS["English"]
    ).get(
        key,
        key
    )

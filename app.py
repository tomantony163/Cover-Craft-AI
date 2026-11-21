"""
CoverCraft AI - Smart Cover Letter Generator
Topic 3 - AI Cover Letter Generator
Built with Python, Streamlit, and Google Gemini AI.
"""

import os
import certifi
import streamlit as st
from datetime import datetime
from dotenv import load_dotenv

# Ensure SSL certificates are properly resolved on Windows
os.environ.setdefault("SSL_CERT_FILE", certifi.where())

# Load environment variables from .env file if present
load_dotenv()

from generator import generate_cover_letter, generate_mock_cover_letter, calculate_word_count
from sample_data import SAMPLE_DATASETS

# --- Page Configuration ---
st.set_page_config(
    page_title="CoverCraft AI – Smart Cover Letter Generator",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom Styling (Modern, Clean, Professional) ---
st.markdown("""
<style>
    /* Global Styles */
    .main-title {
        font-size: 2.3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #1E3A8A 0%, #3B82F6 50%, #10B981 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    .badge {
        display: inline-block;
        padding: 0.25rem 0.6rem;
        font-size: 0.75rem;
        font-weight: 600;
        border-radius: 9999px;
        background-color: #E0E7FF;
        color: #3730A3;
        margin-right: 0.5rem;
    }
    .badge-success {
        background-color: #D1FAE5;
        color: #065F46;
    }
    .badge-warning {
        background-color: #FEF3C7;
        color: #92400E;
    }
    .section-card {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1.25rem;
        margin-bottom: 1rem;
    }
    .output-container {
        background-color: #FFFFFF;
        border: 1px solid #CBD5E1;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        font-family: 'Georgia', serif;
        line-height: 1.6;
        color: #1E293B;
        white-space: pre-wrap;
    }
    .metric-box {
        background-color: #F1F5F9;
        border-radius: 8px;
        padding: 0.75rem;
        text-align: center;
        border: 1px solid #E2E8F0;
    }
</style>
""", unsafe_allow_html=True)


# --- Helper to Initialize Session State ---
def init_session_state():
    default_state = {
        "full_name": "",
        "email": "",
        "phone": "",
        "location": "",
        "linkedin": "",
        "education": "",
        "skills": "",
        "projects": "",
        "company_name": "",
        "role": "",
        "hiring_manager": "",
        "job_description": "",
        "generated_letter": "",
        "word_count": 0,
        "is_mock": False
    }
    for key, val in default_state.items():
        if key not in st.session_state:
            st.session_state[key] = val


init_session_state()


def load_selected_sample(sample_key: str):
    """Loads chosen sample data into session state."""
    if sample_key in SAMPLE_DATASETS:
        data = SAMPLE_DATASETS[sample_key]
        for k, v in data["applicant"].items():
            st.session_state[k] = v
        for k, v in data["job"].items():
            st.session_state[k] = v


def clear_form_data():
    """Resets all fields in session state."""
    keys_to_clear = [
        "full_name", "email", "phone", "location", "linkedin",
        "education", "skills", "projects", "company_name", "role",
        "hiring_manager", "job_description", "generated_letter", "word_count"
    ]
    for k in keys_to_clear:
        st.session_state[k] = ""
    st.session_state["word_count"] = 0


# --- Sidebar Navigation & Configuration ---
with st.sidebar:
    st.image("https://api.iconify.design/lucide:sparkles.svg?color=%233b82f6", width=42)
    st.markdown("### ⚙️ CoverCraft Settings")
    st.caption("Configure AI Model & Generation Options")
    
    # 1. API Key Configuration
    env_api_key = os.getenv("GEMINI_API_KEY", "")
    api_key_input = st.text_input(
        "Gemini API Key",
        value=env_api_key,
        type="password",
        placeholder="AIzaSy...",
        help="Enter your Google Gemini API key. You can get one for free at https://aistudio.google.com/apikey"
    )
    
    if api_key_input:
        st.success("✅ API Key configured", icon="🔑")
    else:
        st.info("💡 Enter your Gemini API key above or toggle Demo Mode below.", icon="ℹ️")
        st.markdown("[Get a free Gemini API key →](https://aistudio.google.com/apikey)")

    # 2. Demo Mode Toggle (for testing without API key)
    demo_mode = st.checkbox(
        "Offline Demo Mode",
        value=not bool(api_key_input),
        help="Enable to test the UI and workflow without consuming an API key."
    )
    
    st.divider()

    # 3. Model & Tone Selection
    st.markdown("#### 🧠 AI Configuration")
    selected_model = st.selectbox(
        "Gemini Model",
        options=["gemini-3.5-flash-lite", "gemini-flash-lite-latest", "gemini-3.8-flash"],
        index=0,
        help="gemini-3.5-flash-lite delivers ultra-fast, high-quality, and reliable results."
    )

    selected_tone = st.selectbox(
        "Letter Tone & Style",
        options=[
            "Professional & Confident",
            "Enthusiastic & High-Energy",
            "Direct & Result-Oriented",
            "Technical & Analytical",
            "Creative & Story-driven"
        ],
        index=0
    )

    st.divider()

    # 4. Instant Sample Data Loader
    st.markdown("#### ⚡ Quick Demo Data")
    sample_choice = st.selectbox(
        "Choose a ready profile:",
        options=list(SAMPLE_DATASETS.keys()),
        index=0
    )
    
    col_sample, col_clear = st.columns(2)
    with col_sample:
        if st.button("🚀 Load Sample", use_container_width=True):
            load_selected_sample(sample_choice)
            st.toast("Sample profile loaded successfully!", icon="✅")
            st.rerun()

    with col_clear:
        if st.button("🗑️ Clear Form", use_container_width=True):
            clear_form_data()
            st.toast("Form cleared.", icon="🧹")
            st.rerun()

    st.divider()

    # 5. Project Metadata & Checklist Info
    st.markdown("#### 🎓 Project Metadata")
    st.caption("**Topic 3:** AI Cover Letter Generator")
    st.caption("**Task:** Task 2 (Applied AI / Generative AI)")
    st.caption("**Constraint:** < 300 words strict output")
    st.caption("**Export:** Download as .txt format")


# --- Main Application Header ---
st.markdown('<div class="main-title">CoverCraft AI</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Smart, ATS-friendly cover letter generator powered by <b>Google Gemini AI</b>. Crafted specifically for students and job seekers in fewer than 300 words.</div>',
    unsafe_allow_html=True
)

# Workflow Banner
st.markdown("""
<div style="display: flex; gap: 0.5rem; flex-wrap: wrap; margin-bottom: 1.25rem;">
    <span class="badge">1. Fill Details</span>
    <span class="badge">2. Target Job</span>
    <span class="badge">3. Gemini AI Analysis</span>
    <span class="badge badge-success">4. Under 300 Words</span>
    <span class="badge badge-success">5. Instant .TXT Export</span>
</div>
""", unsafe_allow_html=True)

# --- Input Form (Two Column Layout) ---
st.markdown("### 📋 Enter Information")

col_left, col_right = st.columns(2, gap="large")

with col_left:
    st.markdown("#### 👤 1. Applicant Profile")
    with st.container():
        full_name = st.text_input(
            "Full Name *",
            value=st.session_state["full_name"],
            placeholder="e.g. Tom Antony"
        )
        
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            email = st.text_input(
                "Email Address *",
                value=st.session_state["email"],
                placeholder="tom.antony@email.com"
            )
        with col_c2:
            phone = st.text_input(
                "Phone Number",
                value=st.session_state["phone"],
                placeholder="+91 98765 43210"
            )

        col_c3, col_c4 = st.columns(2)
        with col_c3:
            location = st.text_input(
                "Location / City",
                value=st.session_state["location"],
                placeholder="Bengaluru, India"
            )
        with col_c4:
            linkedin = st.text_input(
                "LinkedIn / Portfolio URL",
                value=st.session_state["linkedin"],
                placeholder="linkedin.com/in/tom-antony"
            )

        education = st.text_area(
            "Degree & Educational Background *",
            value=st.session_state["education"],
            height=70,
            placeholder="e.g. B.Tech in Artificial Intelligence & Data Science, XYZ University (2026)"
        )

        skills = st.text_area(
            "Key Technical & Soft Skills *",
            value=st.session_state["skills"],
            height=70,
            placeholder="e.g. Python, Gemini API, PyTorch, Streamlit, NLP, REST APIs, Git"
        )

        projects = st.text_area(
            "Key Projects & Practical Experience *",
            value=st.session_state["projects"],
            height=90,
            placeholder="e.g. CoverCraft AI (End-to-end LLM application for automated cover letter crafting), Sentiment Analyzer using Transformers..."
        )

with col_right:
    st.markdown("#### 🏢 2. Target Job & Company")
    with st.container():
        company_name = st.text_input(
            "Target Company Name *",
            value=st.session_state["company_name"],
            placeholder="e.g. Google"
        )

        role = st.text_input(
            "Target Position / Job Title *",
            value=st.session_state["role"],
            placeholder="e.g. AI Software Engineer Intern"
        )

        hiring_manager = st.text_input(
            "Hiring Manager / Team (Optional)",
            value=st.session_state["hiring_manager"],
            placeholder="e.g. Google Cloud AI Hiring Team (or leave blank for Hiring Team)"
        )

        job_description = st.text_area(
            "Target Job Description & Requirements *",
            value=st.session_state["job_description"],
            height=250,
            placeholder="Paste the key responsibilities, qualifications, and requirements from the job posting here..."
        )

# Update session state with current input values
st.session_state["full_name"] = full_name
st.session_state["email"] = email
st.session_state["phone"] = phone
st.session_state["location"] = location
st.session_state["linkedin"] = linkedin
st.session_state["education"] = education
st.session_state["skills"] = skills
st.session_state["projects"] = projects
st.session_state["company_name"] = company_name
st.session_state["role"] = role
st.session_state["hiring_manager"] = hiring_manager
st.session_state["job_description"] = job_description

st.divider()

# --- Generation Action Button ---
col_btn, col_info = st.columns([1, 2])
with col_btn:
    generate_clicked = st.button(
        "✨ Generate Cover Letter",
        type="primary",
        use_container_width=True
    )

with col_info:
    if demo_mode:
        st.info("ℹ️ Running in **Offline Demo Mode**. A structured preview will be generated without an API call.", icon="🧪")
    elif not api_key_input:
        st.warning("⚠️ Please provide a Gemini API Key in the sidebar or check Offline Demo Mode.", icon="🔑")

# --- Generation Logic ---
if generate_clicked:
    # Validation
    errors = []
    if not full_name.strip():
        errors.append("Applicant Full Name is required.")
    if not education.strip():
        errors.append("Degree / Education is required.")
    if not skills.strip():
        errors.append("Key Skills are required.")
    if not company_name.strip():
        errors.append("Target Company Name is required.")
    if not role.strip():
        errors.append("Target Job Title is required.")
    if not job_description.strip():
        errors.append("Job Description is required to tailor the letter.")

    if errors:
        for err in errors:
            st.error(f"• {err}")
    else:
        applicant_data = {
            "full_name": full_name.strip(),
            "email": email.strip(),
            "phone": phone.strip(),
            "location": location.strip(),
            "linkedin": linkedin.strip(),
            "education": education.strip(),
            "skills": skills.strip(),
            "projects": projects.strip(),
        }
        job_data = {
            "company_name": company_name.strip(),
            "role": role.strip(),
            "hiring_manager": hiring_manager.strip() if hiring_manager.strip() else "Hiring Manager",
            "job_description": job_description.strip(),
        }

        with st.spinner("🤖 Gemini AI is tailoring your cover letter to match the role requirements..."):
            if demo_mode or not api_key_input:
                success, letter_text, wc = generate_mock_cover_letter(applicant_data, job_data, tone=selected_tone)
                st.session_state["is_mock"] = True
            else:
                success, letter_text, wc = generate_cover_letter(
                    api_key=api_key_input,
                    applicant=applicant_data,
                    job=job_data,
                    tone=selected_tone,
                    model_name=selected_model
                )
                st.session_state["is_mock"] = False

        if success:
            st.session_state["generated_letter"] = letter_text
            st.session_state["word_count"] = wc
            st.toast("Cover letter generated successfully!", icon="🎉")
        else:
            st.error(letter_text)


# --- Output Section ---
if st.session_state.get("generated_letter"):
    st.markdown("---")
    st.markdown("### 📄 Generated Cover Letter")
    
    current_wc = calculate_word_count(st.session_state["generated_letter"])
    
    # Metrics Row
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Total Words", current_wc)
    with m2:
        status_label = "✅ Under 300 words" if current_wc <= 300 else "⚠️ Over 300 words"
        st.metric("Length Requirement", status_label)
    with m3:
        reading_time = f"{round(current_wc / 200, 1)} min"
        st.metric("Est. Reading Time", reading_time)
    with m4:
        engine_label = "Demo Simulation" if st.session_state.get("is_mock") else selected_model
        st.metric("Generated By", engine_label)

    # Word count alert banner
    if current_wc > 300:
        st.warning(f"⚠️ Current length ({current_wc} words) slightly exceeds the 300-word recommendation. You can trim minor details in the editor below.", icon="⚠️")
    else:
        st.success(f"🎯 Perfect length! Exactly {current_wc} words (strictly fewer than 300 words). Highly readable and ATS-friendly.", icon="🎯")

    # Editable Cover Letter Text Area
    edited_letter = st.text_area(
        "Review and Edit Your Cover Letter:",
        value=st.session_state["generated_letter"],
        height=380,
        help="You can edit any sentence or adjust formatting directly in this box before downloading."
    )
    st.session_state["generated_letter"] = edited_letter

    # File Name generation for download
    safe_name = "".join(c for c in full_name if c.isalnum() or c in (' ', '_', '-')).strip().replace(' ', '_')
    safe_company = "".join(c for c in company_name if c.isalnum() or c in (' ', '_', '-')).strip().replace(' ', '_')
    if not safe_name:
        safe_name = "Candidate"
    if not safe_company:
        safe_company = "Company"
    download_filename = f"Cover_Letter_{safe_name}_{safe_company}.txt"

    # Action Buttons: Download & Copy
    col_dl, col_txt = st.columns([1, 2])
    with col_dl:
        st.download_button(
            label="📥 Download as .TXT File",
            data=edited_letter,
            file_name=download_filename,
            mime="text/plain",
            type="primary",
            use_container_width=True
        )
    with col_txt:
        st.caption(f"💾 File ready for submission: `{download_filename}`")

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748B; font-size: 0.85rem; padding: 1rem 0;">
    <b>CoverCraft AI – Smart Cover Letter Generator</b> | Powered by Google Gemini AI & Streamlit<br/>
    Academic Submission Project • Task 2: Topic 3
</div>
""", unsafe_allow_html=True)

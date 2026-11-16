"""
CoverCraft AI - Core AI Generator Module
Handles prompt construction, Google Gemini API interaction, and letter generation.
"""

import os
from datetime import datetime
from typing import Dict, Tuple, Optional

# Attempt to import google-genai
try:
    from google import genai
    from google.genai import types
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False


def calculate_word_count(text: str) -> int:
    """Counts words in a text string accurately."""
    if not text:
        return 0
    return len(text.strip().split())


def build_generation_prompt(
    applicant: Dict[str, str],
    job: Dict[str, str],
    tone: str = "Professional & Confident"
) -> str:
    """Constructs a targeted prompt for Gemini AI with strict length constraints."""
    
    current_date = datetime.now().strftime("%B %d, %Y")
    
    prompt = f"""You are an elite career strategist and executive cover letter writer.
Write a personalized, highly compelling cover letter that bridges the applicant's real skills and projects directly to the employer's job requirements.

STRICT REQUIREMENTS:
1. WORD LIMIT: Strictly UNDER 300 WORDS (ideal range: 220 - 275 words). Be concise, punchy, and eliminate fluff.
2. TONE: {tone}.
3. FORMAT & STRUCTURE:
   - Header: Include current date ({current_date}), greeting to {job.get('hiring_manager', 'Hiring Team')}.
   - Opening Paragraph: Immediate hook expressing genuine enthusiasm for {job.get('company_name', 'the company')} and the {job.get('role', 'position')} role.
   - Body Paragraph(s): Concretely connect applicant's real projects and skills to the specific challenges and requirements mentioned in the job description. Show impact, not just responsibilities.
   - Closing Paragraph: Confident call-to-action requesting an interview, gratitude, and professional sign-off with the applicant's name.
4. ZERO PLACEHOLDERS: Do NOT output placeholder brackets like [Company], [Your Name], [Insert Date], [Phone]. All details must be fully filled in using the supplied data below.
5. CLEAN PLAIN TEXT: Do not wrap output in triple backticks or markdown code fences. Provide ready-to-use letter text.

--- APPLICANT PROFILE ---
Full Name: {applicant.get('full_name', 'Job Applicant')}
Email: {applicant.get('email', '')}
Phone: {applicant.get('phone', '')}
Location: {applicant.get('location', '')}
LinkedIn / Portfolio: {applicant.get('linkedin', '')}
Degree & Education: {applicant.get('education', '')}
Core Technical & Soft Skills: {applicant.get('skills', '')}
Key Projects & Experience: {applicant.get('projects', '')}

--- TARGET OPPORTUNITY ---
Company Name: {job.get('company_name', 'Target Company')}
Target Role: {job.get('role', 'Open Position')}
Hiring Manager / Team: {job.get('hiring_manager', 'Hiring Manager')}
Job Description & Requirements:
{job.get('job_description', '')}

Now, generate the complete, customized cover letter strictly under 300 words.
"""
    return prompt


def generate_cover_letter(
    api_key: str,
    applicant: Dict[str, str],
    job: Dict[str, str],
    tone: str = "Professional & Confident",
    model_name: str = "gemini-2.5-flash"
) -> Tuple[bool, str, int]:
    """
    Calls Google Gemini AI to generate a personalized cover letter.
    
    Returns:
        (success: bool, content_or_error_message: str, word_count: int)
    """
    if not api_key or not api_key.strip():
        return False, "Error: Gemini API key is missing. Please provide your API key in the sidebar or via .env file.", 0
    
    if not GENAI_AVAILABLE:
        return False, "Error: The `google-genai` package is not installed. Please install it using `pip install google-genai`.", 0

    prompt = build_generation_prompt(applicant, job, tone)

    try:
        # Initialize Google GenAI client
        client = genai.Client(api_key=api_key.strip())
        
        # Call the Gemini model
        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
        )
        
        if not response or not response.text:
            return False, "Error: Gemini returned an empty response. Please try again with different inputs.", 0
        
        letter_text = response.text.strip()
        
        # Clean up any accidental code fences if returned
        if letter_text.startswith("```"):
            lines = letter_text.splitlines()
            if lines and lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]
            letter_text = "\n".join(lines).strip()
            
        word_count = calculate_word_count(letter_text)
        return True, letter_text, word_count

    except Exception as e:
        error_str = str(e)
        if "API_KEY_INVALID" in error_str or "API key not valid" in error_str:
            return False, "Invalid API Key: The Gemini API key provided is not valid. Please check and re-enter your key from https://aistudio.google.com/apikey", 0
        elif "RESOURCE_EXHAUSTED" in error_str or "quota" in error_str.lower():
            return False, "Quota Exceeded: Your Gemini API quota limit was reached. Please wait a moment or try another model/key.", 0
        elif "not found" in error_str.lower() or "404" in error_str:
            # Fallback suggestion if specific model isn't available
            return False, f"Model '{model_name}' was not recognized or unavailable for your key. Try selecting 'gemini-1.5-flash' in the sidebar.", 0
        else:
            return False, f"API Error ({type(e).__name__}): {error_str}", 0


def generate_mock_cover_letter(
    applicant: Dict[str, str],
    job: Dict[str, str],
    tone: str = "Professional & Confident"
) -> Tuple[bool, str, int]:
    """
    Generates an intelligent simulated cover letter for offline demo/testing purposes
    when the user has not yet entered their Gemini API key.
    """
    current_date = datetime.now().strftime("%B %d, %Y")
    full_name = applicant.get("full_name") or "Applicant Name"
    email = applicant.get("email") or "applicant@email.com"
    phone = applicant.get("phone") or "+1 (555) 019-2834"
    education = applicant.get("education") or "B.Tech in Artificial Intelligence"
    skills = applicant.get("skills") or "Python, Machine Learning, Streamlit"
    projects = applicant.get("projects") or "AI Cover Letter Generator project"
    company = job.get("company_name") or "Innovative Tech Corp"
    role = job.get("role") or "AI Software Engineer Intern"
    hiring_manager = job.get("hiring_manager") or "Hiring Team"
    
    mock_text = f"""{full_name}
{email} | {phone}
{current_date}

Dear {hiring_manager} at {company},

I am writing to express my strong enthusiasm for the {role} position at {company}. With a strong foundation in {education} and hands-on expertise in {skills}, I am eager to contribute immediately to your team's mission.

During my academic and practical coursework, I spearheaded projects such as {projects}. Through this work, I developed robust problem-solving skills, implemented clean software architectures, and translated complex technical requirements into user-centric applications. The initiatives at {company} resonate deeply with my passion for creating intelligent, scalable software solutions.

I welcome the opportunity to discuss how my technical acumen, rapid learning agility, and dedication can support the {role} role at {company}. Thank you for your time and consideration.

Sincerely,

{full_name}"""

    word_count = calculate_word_count(mock_text)
    return True, mock_text.strip(), word_count

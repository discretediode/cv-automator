import os
import time
from dotenv import load_dotenv
import google.generativeai as genai

# 1. Configure your API key here
load_dotenv(override=True)
API_KEY = os.getenv("MY_API_KEY")

if not API_KEY:
    raise ValueError("🚨 API Key not found! Please check your .env file.")
genai.configure(api_key=API_KEY)

# 2. Select the model
model = genai.GenerativeModel('gemini-3.5-flash-lite')

# ==========================================
# CORE LLM FUNCTIONS (The Engine)
# ==========================================
def detect_language(job_description):
    """Detects if the job description is in German or English."""
    prompt = f"""
    Analyze the following job description and detect its primary language.
    If it is German, reply with exactly: Deutsch
    If it is English (or any other language), reply with exactly: English
    
    Do not output any punctuation, code blocks, or extra text. Just the single word.
    
    JOB DESCRIPTION:
    {job_description}
    """
    response = model.generate_content(prompt)
    return response.text.strip()

def generate_tailored_cv(job_description, vault_data, target_language):
    """Generates the initial CV draft based on the vault and detected language."""
    profile_context = ""
    for filename, content in vault_data.items():
        profile_context += f"\n--- {filename} ---\n{content}\n"

    print(f"Sending data to Gemini for CV... (Target Language: {target_language})")
    
    prompt = f"""
    You are an expert technical recruiter and resume writer.
    Below is my complete professional profile (extracted from my Markdown vault).
    
    MY PROFILE:
    {profile_context}
    
    JOB DESCRIPTION:
    {job_description}
    
    TASK:
    Read my profile and the job description. Pick the most relevant experiences, 
    projects, and skills. Write a highly tailored, professional summary and 
    bullet points that prove I am the best person fit for this specific job. 
    
    CRITICAL LANGUAGE RULE:
    The requested output language is: {target_language}.
    You MUST write the ENTIRE CV (including all bullet points, content, and headers) strictly in {target_language}. 
    If my profile is in a different language, translate it accurately to {target_language}.
    
    CRITICAL FORMATTING RULE:
    1. Do NOT include a header, contact information, or name at the top.
    2. Do NOT write a "Professional Summary" or "Objective" section. 
    3. You MUST organize the resume in this exact order (Translate these headers to {target_language}):
       - ## Work Experience
       - ## Skills and Competencies
       - ## Technical Projects
       - ## Extracurricular Activities
    4. Do NOT include an Education section (I will add this manually).
    
    Output the result in clean Markdown.
    """

    start_time = time.time()
    response = model.generate_content(prompt)
    end_time = time.time()
    
    print(f"✅ Generation complete! (Took {end_time - start_time:.1f} seconds)")
    return response.text

def generate_anschreiben(job_description, raw_cv, guidelines=""):
    """Generates the Anschreiben using the APPROVED tailored CV."""
    print("Sending data to Gemini for Anschreiben... (chaining the approved CV)")
    
    prompt = f"""
    You are an expert career coach and copywriter.
    
    MY TAILORED CV:
    {raw_cv}
    
    JOB DESCRIPTION:
    {job_description}

    MY PERSONAL WRITING GUIDELINES:
    {guidelines}
    
    TASK:
    Write a compelling, professional Cover Letter (Anschreiben) based ONLY on the 
    tailored CV provided above. Do not invent facts. Match the language of the 
    job description. Keep it concise, modern, and engaging. 
    Strictly follow any rules listed in MY PERSONAL WRITING GUIDELINES.
    Output in clean Markdown.
    
    CRITICAL FORMATTING RULE:
    Do NOT include a header, contact information, date, or subject line. 
    Do NOT use placeholders like [Your Name] or [Date]. 
    Start your response directly with the salutation (e.g., "Dear Hiring Manager,").
    End with "Best regards," for english or "Mit freundlichen Grüßen," for german.
    """
    
    start_time = time.time()
    response = model.generate_content(prompt)
    end_time = time.time()
    
    print(f"✅ Anschreiben generation complete! (Took {end_time - start_time:.1f} seconds)")
    return response.text

def refine_draft(current_draft, instruction):
    """Takes an existing draft and refines it based on a new user instruction."""
    prompt = f"""
    Here is my current document draft:
    {current_draft}
    
    Instruction to apply: {instruction}
    
    Rewrite the draft applying this instruction perfectly. Only output the raw markdown. 
    Do not include markdown code blocks (```markdown) in your response, just the text.
    """
    response = model.generate_content(prompt)
    return response.text
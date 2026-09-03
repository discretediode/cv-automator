import google.generativeai as genai
from vault_reader import read_vault, VAULT_PATH
import os
from pdf_generator import generate_pdf_from_markdown
from dotenv import load_dotenv
import time

# 1. Configure your API key here
load_dotenv()
API_KEY = os.getenv("MY_API_KEY")

if not API_KEY:
    raise ValueError("🚨 API Key not found! Please check your .env file.")
genai.configure(api_key=API_KEY)

# 2. Select the model
model = genai.GenerativeModel('gemini-3.5-flash-lite')

# ==========================================
# CORE LLM FUNCTIONS (The Engine)
# ==========================================

def generate_tailored_cv(job_description, vault_data):
    """Generates the initial CV draft based on the vault."""
    profile_context = ""
    for filename, content in vault_data.items():
        profile_context += f"\n--- {filename} ---\n{content}\n"

    print("Sending data to Gemini for CV... (excluding personal_info.md and education.md)")
    
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
    Output the result in clean Markdown.
    
    CRITICAL FORMATTING RULE:
    1. Do NOT include a header, contact information, or name at the top.
    2. Do NOT write a "Professional Summary" or "Objective" section. 
    3. You MUST organize the resume in this exact order:
       - ## Work Experience
       - ## Skills and Competencies
       - ## Technical Projects
       - ## Extracurricular Activities
    4. Do NOT include an Education section (I will add this manually).
    """

    print("\n⏳ Uploading to Gemini... (Please wait, this might take a moment)")
    start_time = time.time() # Start the stopwatch
    
    # Call the API (The terminal will pause on this exact line)
    response = model.generate_content(prompt)
    
    end_time = time.time() # Stop the stopwatch
    print(f"✅ Generation complete! (Took {end_time - start_time:.1f} seconds)")

    return response.text


def revise_document(current_draft, feedback, document_type="document"):
    """Takes an existing draft and user feedback to generate a revised version."""
    print(f"Asking Gemini to revise the {document_type}...")
    
    prompt = f"""
    You are an expert technical recruiter and career coach.
    Here is a draft of my {document_type}:
    
    CURRENT DRAFT:
    {current_draft}
    
    USER FEEDBACK:
    {feedback}
    
    TASK:
    Update the CURRENT DRAFT strictly based on the USER FEEDBACK. 
    Keep the professional tone and output the result in clean Markdown.
    """
    
    return model.generate_content(prompt).text

def generate_anschreiben(job_description, raw_cv):
    """Generates the Anschreiben using the APPROVED tailored CV."""
    print("Sending data to Gemini for Anschreiben... (chaining the approved CV)")
    
    prompt = f"""
    You are an expert career coach and copywriter.
    
    MY TAILORED CV:
    {raw_cv}
    
    JOB DESCRIPTION:
    {job_description}
    
    TASK:
    Write a compelling, professional Cover Letter (Anschreiben) based ONLY on the 
    tailored CV provided above. Do not invent facts. Match the language of the 
    job description. Keep it concise, modern, and engaging. Output in clean Markdown.
    
    CRITICAL FORMATTING RULE:
    Do NOT include a header, contact information, date, or subject line. 
    Do NOT use placeholders like [Your Name] or [Date]. 
    Start your response directly with the salutation (e.g., "Dear Hiring Manager,").
    """
    
    # 1. Start the timer
    import time
    start_time = time.time()
    
    # 2. Call the API
    response = model.generate_content(prompt)
    
    # 3. Stop the timer and print
    end_time = time.time()
    print(f"✅ Anschreiben generation complete! (Took {end_time - start_time:.1f} seconds)")
    
    return response.text

# ==========================================
# CLI INTERACTION HELPER (Terminal UI)
# ==========================================

def review_and_edit_loop(doc_name, current_draft, personal_info):
    """
    A generic loop for Terminal human approval:
    Allows accepting, editing manually in a temp file, or prompting AI.
    """
    temp_filename = f"temp_{doc_name.lower().replace(' ', '_')}.md"
    
    while True:
        print(f"\n================ CURRENT {doc_name.upper()} DRAFT ================\n")
        print(f"{personal_info}\n\n---\n\n{current_draft}")
        print(f"\n=========================================================\n")
        
        print(f"What would you like to do with this {doc_name}?")
        print(f"[A]ccept and proceed")
        print(f"[M]anually edit in '{temp_filename}'")
        print(f"[P]rompt the AI to make a change")
        
        choice = input("Enter your choice (A/M/P): ").strip().lower()
        
        if choice == 'a':
            print(f"\n✅ {doc_name} Approved!")
            return current_draft
            
        elif choice == 'm':
            with open(temp_filename, "w", encoding="utf-8") as f:
                f.write(current_draft)
            
            print(f"\n⏸️ Draft saved to '{temp_filename}'.")
            input("Open the file, edit, save it, and press ENTER here to reload...")
            
            with open(temp_filename, "r", encoding="utf-8") as f:
                current_draft = f.read()
            print(f"✅ Manual edits to {doc_name} loaded.")
            
        elif choice == 'p':
            feedback = input(f"\nWhat should the AI change in the {doc_name}?: ")
            current_draft = revise_document(current_draft, feedback, document_type=doc_name)
            
        else:
            print("❌ Invalid choice. Please type A, M, or P.")

# ==========================================
# MAIN EXECUTION FLOW
# ==========================================

if __name__ == "__main__":
    test_job = """
    Looking for a Junior Embedded Software Engineer. 
    Must have experience with C/C++, microcontrollers (STM32 preferred), 
    and hardware debugging. Experience with Python is a plus.
    """
    
    print("Starting LLM Engine...\n")
    
    # 1. Read vault and isolate personal info
    my_vault_data = read_vault(VAULT_PATH)
    personal_info = my_vault_data.pop("personal_info.md", "")
    education_info = my_vault_data.pop("education.md", "")
    signature_info = my_vault_data.pop("signature.md", "")
    
    # 2. Generate initial CV draft
    raw_cv = generate_tailored_cv(test_job, my_vault_data)
    
    # 3. CV Approval Loop (Human-in-the-loop Step 3)
    approved_cv = review_and_edit_loop("CV", raw_cv, personal_info)
    
    # 4. Generate Anschreiben using the APPROVED CV
    print("\n--- Generating Anschreiben ---")
    raw_anschreiben = generate_anschreiben(test_job, approved_cv)
    
    # 5. Anschreiben Approval Loop (Human-in-the-loop Step 5)
    approved_anschreiben = review_and_edit_loop("Anschreiben", raw_anschreiben, personal_info)
    
    # 6. Final Assemble
    final_cv = f"{personal_info}\n\n{education_info}\n\n---\n\n{approved_cv}"
    final_anschreiben = f"{personal_info}\n\n---\n\n{approved_anschreiben}\n\n{signature_info}"
    
    print("\n🎉 Both documents have been approved by you!")

    # 7. Local PDF Generation (Zero LLM API calls here!)
    generate_pdf_from_markdown(final_cv, "My_Tailored_CV.pdf", doc_type="cv")
    generate_pdf_from_markdown(final_anschreiben, "My_Anschreiben.pdf", doc_type="anschreiben")
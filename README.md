# Personal AI CV & Cover Letter Automator

A local, Python-based automation tool that uses the Google Gemini API to generate tailored resumes and cover letters from your Markdown notes. It uses a strict privacy-first architecture to ensure Personal Identifiable Information (PII) never leaves your local machine.

## 1. Prerequisites
* **Python 3.10+**
* A **Google Gemini API Key** (available for free from Google AI Studio)

## 2. Environment Setup

**1. Create and activate a virtual environment:**
```bash
python -m venv .venv
source .venv/bin/activate  # On Mac/Linux
# OR: .venv\Scripts\activate  # On Windows

**2. Install all dependencies:**
pip install google-generativeai python-dotenv markdown xhtml2pdf streamlit

**3. API Key Setup:**
In the root directory of this project, rename the `.env.example` file into exactly `.env` and insert your Gemini API key there:
```ini
MY_API_KEY="AIzaSy...your_api_key_here"
```
*(IMPORTANT: `.env` should be added to your `.gitignore` to prevent your key from leaking online).*

---

## 📁 3. Obsidian Vault Setup

To set up your personal data, duplicate the existing my_profile_template folder and rename the copy to my_profile. Open the files inside and replace the placeholders with your real information.

### **Images (Place in the root directory):**
* `profile.jpg`: Professional application photo (Ideally 95x125 px).
* `signature.png`: Your signature with a white or transparent background.

### **Static Files (Kept local, NOT sent to AI):**
These files are "popped" out of the vault data by the Python script to protect your privacy and ensure consistent formatting.
* `personal_info.md`: Your name, contact info, and profile image layout (HTML table).
* `education.md`: Your degrees, universities, dates, and grades.
* `signature.md`: Contains the image link to your signature and your typed name.

### **Dynamic Files (Sent to the AI for tailoring):**
These files act as your "professional brain". The AI will read these to map your background to the job description.
* `experiences.md`: Your past work history and responsibilities.
* `projects.md`: Technical projects (e.g., CV Automator, STM32 Controller).
* `skills.md`: Programming languages, tools, and spoken languages.

---

## 4. Running the App

Once your environment and profile are configured, you can start the application:

```bash
streamlit run app.py
```

### **The Workflow:**
1. The script securely reads your vault and isolates your static PII.
2. It sends your dynamic experiences and the target job description to the Gemini Model.
3. You review the generated markdown drafts in the terminal.
4. Upon approval, Python locally merges your static files (Name, Photo, Education, Signature) with the AI draft.
5. `xhtml2pdf` dynamically renders the final, styling-applied PDF files directly to your computer.

### Troubleshooting
* **`403 Permission Denied`**: Double-check that your API key in the `.env` file is correct and that you saved the file.
* **`429 Resource Exhausted`**: You hit the free-tier rate limit (20 requests per minute). Wait 15-30 seconds and try again. 
* **Testing UI/CSS**: If you are only tweaking the PDF layout (margins, colors), comment out the API call in `llm_engine.py` and return hardcoded Markdown dummy text to avoid hitting rate limits.# cv_automator
# cv_automator

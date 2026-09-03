# Privacy-First AI CV & Cover Letter Automator

A local, Python-based automation tool that leverages the Google Gemini API (Flash 3.6) to instantly generate highly tailored Resumes (CVs) and Cover Letters (Anschreiben) directly from an Obsidian knowledge vault. 

Designed with a strict "human-in-the-loop" privacy architecture, it ensures Personal Identifiable Information (PII) never leaves your local machine.

---

## 🚀 1. Prerequisites
Before running the engine, ensure you have the following installed:
* **Python 3.10+**
* A **Google Gemini API Key** (Get one for free from [Google AI Studio](https://aistudio.google.com/app/apikey))

## ⚙️ 2. Environment Setup

**1. Create and activate a virtual environment:**
```bash
python -m venv .venv
source .venv/bin/activate  # On Mac/Linux
# OR: .venv\Scripts\activate  # On Windows
```

**2. Install required dependencies:**
This project relies entirely on pure-Python libraries. (No heavy system graphics libraries like Homebrew/Cairo are required!)
```bash
pip install google-generativeai python-dotenv markdown xhtml2pdf
```

**3. Set up your API Key:**
In the root directory of this project, create a file named exactly `.env` and add your Gemini API key:
```ini
MY_API_KEY="AIzaSy...your_api_key_here"
```
*(Note: `.env` should be added to your `.gitignore` to prevent your key from leaking online).*

---

## 📁 3. Obsidian Vault Structure

To prevent the AI from processing irrelevant data or altering static facts (like your GPA or Name), you must organize your Markdown files into a specific folder (e.g., `Career_Profile`). Update the `VAULT_PATH` in `llm_engine.py` to point to this folder.

### **Images (Place in the root python project folder):**
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

## 🛠️ 4. Running the Engine

Once your vault is set up and your `.env` file is saved, you can run the script:

```bash
python llm_engine.py
```

### **The Workflow:**
1. The script securely reads your vault and isolates your static PII.
2. It sends your dynamic experiences and the target job description to the Gemini 3.6 Flash model.
3. You review the generated markdown drafts in the terminal.
4. Upon approval, Python locally merges your static files (Name, Photo, Education, Signature) with the AI draft.
5. `xhtml2pdf` dynamically renders the final, styling-applied PDF files directly to your computer.

### ⚠️ Troubleshooting
* **`403 Permission Denied`**: Double-check that your API key in the `.env` file is correct and that you saved the file.
* **`429 Resource Exhausted`**: You hit the free-tier rate limit (20 requests per minute). Wait 15-30 seconds and try again. 
* **Testing UI/CSS**: If you are only tweaking the PDF layout (margins, colors), comment out the API call in `llm_engine.py` and return hardcoded Markdown dummy text to avoid hitting rate limits.# cv_automator
# cv_automator

import streamlit as st
import time
from pathlib import Path

# Import your custom modules
# Make sure detect_language is added to llm_engine.py!
from vault_reader import read_vault
from llm_engine import generate_tailored_cv, generate_anschreiben, refine_draft, detect_language
from pdf_generator import generate_pdf_from_markdown

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="CV Automator", page_icon="📄", layout="wide")
st.title("CV & Cover Letter Automator")
st.markdown("Generate highly tailored, locally-secured job applications.")

# --- SESSION STATE INITIALIZATION ---
if "cv_draft" not in st.session_state:
    st.session_state.cv_draft = ""
if "letter_draft" not in st.session_state:
    st.session_state.letter_draft = ""
if "vault_data" not in st.session_state:
    st.session_state.vault_data = None
if "lang_suffix" not in st.session_state:
    st.session_state.lang_suffix = ""
# Add these two new version counters:
if "cv_version" not in st.session_state:
    st.session_state.cv_version = 0
if "letter_version" not in st.session_state:
    st.session_state.letter_version = 0

# --- 1. VAULT LOADING & DATA EXTRACTION ---
if st.session_state.vault_data is None:
    # Hardcoded to look for the my_profile folder
    full_vault = read_vault(Path("my_profile")) 
    
    # Securely pop static files (leaving education_de.md in the vault for the AI)
    st.session_state.static_files = {
        "personal_info": full_vault.pop("personal_info.md", ""),
        "personal_info_de": full_vault.pop("personal_info_de.md", ""),
        "education": full_vault.pop("education.md", ""), 
        "education_de": full_vault.pop("education_de.md", ""),
        "signature": full_vault.pop("signature.md", ""),
        "anschreiben_guidelines": full_vault.pop("guidelines_for_anschreiben.md", "")
    }
    
    # Save the remaining dynamic files for the AI
    st.session_state.vault_data = full_vault
    
    # Save the remaining dynamic files for the AI
    st.session_state.vault_data = full_vault

# --- 2. USER INPUT ---
st.info(f"📁 Loaded Dynamic Vault Files for AI: {list(st.session_state.vault_data.keys())}")

st.header("1. Job Description")
job_description = st.text_area(
    "Paste the job description here:",
    height=200,
    placeholder="e.g., We are looking for a Junior Embedded Software Engineer with STM32 experience..."
)

# --- 3. DRAFT GENERATION ---
if st.button("🚀 Generate Initial Drafts", type="primary"):
    if not job_description.strip():
        st.warning("Please paste a job description first!")
    else:
        # 1. Detect Language First
        with st.spinner("Detecting language..."):
            detected_lang = detect_language(job_description)
            st.session_state.lang_suffix = "_de" if "Deutsch" in detected_lang else ""
            st.info(f"🌐 Detected Language: {detected_lang}")

        # 2. Generate Drafts (Now passing detected_lang to the CV generator!)
        with st.spinner("Generating Tailored CV... (This takes a few seconds)"):
            st.session_state.cv_draft = generate_tailored_cv(job_description, st.session_state.vault_data, detected_lang)
            
        with st.spinner("Generating Cover Letter..."):
            st.session_state.letter_draft = generate_anschreiben(job_description, 
                                                                 st.session_state.cv_draft, 
                                                                 st.session_state.static_files["anschreiben_guidelines"]
                                                                 )
        st.session_state.cv_version += 1
        st.session_state.letter_version += 1
        
        st.success("CV generated successfully! Review and refine below.")
            
        with st.spinner("Generating Cover Letter..."):
            st.session_state.letter_draft = generate_anschreiben(job_description, 
                                                                 st.session_state.cv_draft, 
                                                                 st.session_state.static_files["anschreiben_guidelines"]
                                                                 )
            
        st.success("Cover letter generated successfully! Review and refine below.")

# --- 4. HUMAN-IN-THE-LOOP REVIEW & REFINEMENT ---
if st.session_state.cv_draft or st.session_state.letter_draft:
    st.header("2. Review & Refine Drafts")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Tailored CV")
        
        # The dynamic key forces the widget to refresh ONLY when the AI updates it
        edited_cv = st.text_area(
            "Edit CV Markdown:", 
            value=st.session_state.cv_draft, 
            height=400,
            key=f"cv_box_{st.session_state.cv_version}"
        )
        
        # Save any manual typing seamlessly
        st.session_state.cv_draft = edited_cv
        
        cv_instruction = st.text_input("🤖 Prompt AI to adjust CV:", placeholder="e.g., Make the skills more prominent")
        if st.button("✨ Refine CV"):
            with st.spinner("Refining CV..."):
                st.session_state.cv_draft = refine_draft(edited_cv, cv_instruction)
                st.session_state.cv_version += 1  # ⬅️ The secret sauce to force the UI to update
                st.rerun() 
        
    with col2:
        st.subheader("Cover Letter (Anschreiben)")
        
        edited_letter = st.text_area(
            "Edit Cover Letter Markdown:", 
            value=st.session_state.letter_draft, 
            height=400,
            key=f"letter_box_{st.session_state.letter_version}"
        )
        
        st.session_state.letter_draft = edited_letter
        
        letter_instruction = st.text_input("🤖 Prompt AI to adjust Cover Letter:", placeholder="e.g., Translate to German and make it formal")
        if st.button("✨ Refine Cover Letter"):
            with st.spinner("Refining Letter..."):
                st.session_state.letter_draft = refine_draft(edited_letter, letter_instruction)
                st.session_state.letter_version += 1  # ⬅️ Update the UI
                st.rerun()

    # --- 5. FINAL PDF ASSEMBLY ---
    st.header("3. Generate Final PDFs")
    if st.button("💾 Approve & Save as PDF", type="primary"):
        with st.spinner("Assembling and rendering PDFs..."):
            
            # 1. Fetch correct language static files (Crash-proof fallback)
            suffix = st.session_state.lang_suffix
            
            p_info = st.session_state.static_files.get(f"personal_info{suffix}") or st.session_state.static_files.get("personal_info", "")
            edu_info = st.session_state.static_files.get(f"education{suffix}") or st.session_state.static_files.get("education", "")
            sig_info = st.session_state.static_files.get(f"signature{suffix}") or st.session_state.static_files.get("signature", "")
            
            # 2. Assemble the CV
            final_cv = f"{p_info}\n\n{edu_info}\n\n---\n\n{st.session_state.cv_draft}"
            
            # 3. Assemble the Anschreiben
            final_anschreiben = f"{p_info}\n\n---\n\n{st.session_state.letter_draft}\n\n{sig_info}"
            
            # 4. Generate PDFs using xhtml2pdf
            generate_pdf_from_markdown(final_cv, "Dalfin_Solihin_CV.pdf", doc_type="cv")
            generate_pdf_from_markdown(final_anschreiben, "Dalfin_Solihin_CoverLetter.pdf", doc_type="anschreiben")
            
            st.success("🎉 PDFs successfully generated and saved to your folder!")
            st.balloons()
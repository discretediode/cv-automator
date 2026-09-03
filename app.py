import streamlit as st
import time
from pathlib import Path

# Import your custom modules
# Make sure these match the actual function names in your files!
from vault_reader import read_vault
from llm_engine import generate_tailored_cv, generate_anschreiben
from pdf_generator import generate_pdf_from_markdown

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="CV Automator", page_icon="📄", layout="wide")
st.title("📄 CV & Cover Letter Automator")
st.markdown("Generate highly tailored, locally-secured job applications.")

# --- SESSION STATE INITIALIZATION ---
# This keeps your drafts saved on the screen while you edit them
if "raw_cv" not in st.session_state:
    st.session_state.raw_cv = ""
if "raw_anschreiben" not in st.session_state:
    st.session_state.raw_anschreiben = ""
if "vault_data" not in st.session_state:
    st.session_state.vault_data = None

# --- 1. VAULT LOADING & DATA EXTRACTION ---
# Load the vault once and pop the static files for privacy
if st.session_state.vault_data is None:
    # Wrap the string in Path()
    full_vault = read_vault(Path("my_profile")) 
    
    # Securely pop the static files before the AI sees the data
    st.session_state.personal_info = full_vault.pop("personal_info.md", "")
    st.session_state.education = full_vault.pop("education.md", "")
    st.session_state.signature = full_vault.pop("signature.md", "")
    
    # Save the remaining dynamic files for the AI
    st.session_state.vault_data = full_vault

# --- 2. USER INPUT ---
st.info(f"📁 Loaded Dynamic Vault Files: {list(st.session_state.vault_data.keys())}")

st.header("1. Job Description")
job_description = st.text_area(
    "Paste the job description here:",
    height=200,
    placeholder="e.g., We are looking for a Junior Embedded Software Engineer with STM32 experience..."
)

# --- 3. DRAFT GENERATION ---
if st.button("🚀 Generate Drafts", type="primary"):
    if not job_description.strip():
        st.warning("Please paste a job description first!")
    else:
        with st.spinner("Generating Tailored CV... (This takes a few seconds)"):
            st.session_state.raw_cv = generate_tailored_cv(job_description, st.session_state.vault_data)
            
        with st.spinner("Generating Cover Letter..."):
            st.session_state.raw_anschreiben = generate_anschreiben(job_description, st.session_state.raw_cv)
            
        st.success("Drafts generated successfully! Please review below.")

# --- 4. HUMAN-IN-THE-LOOP REVIEW ---
if st.session_state.raw_cv or st.session_state.raw_anschreiben:
    st.header("2. Review & Edit Drafts")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Tailored CV")
        # Allow the user to manually edit the generated draft
        approved_cv = st.text_area("Edit CV Markdown:", value=st.session_state.raw_cv, height=400)
        
    with col2:
        st.subheader("Cover Letter (Anschreiben)")
        # Allow the user to manually edit the generated letter
        approved_anschreiben = st.text_area("Edit Cover Letter Markdown:", value=st.session_state.raw_anschreiben, height=400)

    # --- 5. FINAL PDF ASSEMBLY ---
    st.header("3. Generate Final PDFs")
    if st.button("💾 Approve & Save as PDF", type="primary"):
        with st.spinner("Assembling and rendering PDFs..."):
            
            # 1. Assemble the CV
            final_cv = f"{st.session_state.personal_info}\n\n{st.session_state.education}\n\n---\n\n{approved_cv}"
            
            # 2. Assemble the Anschreiben
            final_anschreiben = f"{st.session_state.personal_info}\n\n---\n\n{approved_anschreiben}\n\n{st.session_state.signature}"
            
            # 3. Generate PDFs using xhtml2pdf
            generate_pdf_from_markdown(final_cv, "Dalfin_Solihin_CV.pdf", doc_type="cv")
            generate_pdf_from_markdown(final_anschreiben, "Dalfin_Solihin_CoverLetter.pdf", doc_type="anschreiben")
            
            st.success("🎉 PDFs successfully generated and saved to your folder!")
            st.balloons()
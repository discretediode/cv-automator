# pdf_generator.py
import markdown
from xhtml2pdf import pisa

def get_css(doc_type):
    """Returns the CSS styling for the PDF (Black & White, Compact)."""
    base_css = """
    @page {
        size: a4 portrait;
        margin: 1.2cm 1.5cm; /* Tighter margins to fit more on the page */
    }
    body {
        font-family: Helvetica, Arial, sans-serif;
        color: #000000; /* Pure Black */
        font-size: 10.5pt; /* Slightly smaller for compactness */
        line-height: 1.25; /* Tighter line height */
    }
    h1 {
        color: #000000; 
        font-size: 18pt;
        border-bottom: 1px solid #000000; /* Black underline */
        padding-bottom: 4px;
        margin-bottom: 2px;
    }
    h2 {
        color: #000000;
        font-size: 13pt;
        margin-top: 10px;
        margin-bottom: 4px;
    }
    h3 {
        font-size: 11pt;
        margin-top: 6px;
        margin-bottom: 2px;
    }
    p {
        margin-bottom: 5px;
    }
    ul {
        margin-bottom: 6px;
        margin-top: 2px;
    }
    li {
        margin-bottom: 2px;
    }
    """
    
    if doc_type == "anschreiben":
        base_css += """
        body { font-size: 11pt; line-height: 1.3; }
        p { text-align: justify; margin-bottom: 10px; }
        h1 { border-bottom: none; margin-bottom: 12px; }
        """
        
    return base_css

def generate_pdf_from_markdown(markdown_text, output_filename, doc_type="cv"):
    """
    Converts Markdown to HTML, injects CSS, and renders a PDF using pure Python.
    """
    print(f"🎨 Rendering {output_filename} locally...")
    
    # 1. Convert Markdown string to HTML string
    html_content = markdown.markdown(markdown_text, extensions=['extra', 'nl2br'])
    
    # 2. Get the appropriate CSS
    css_styles = get_css(doc_type)
    
    # 3. Wrap it in standard HTML boilerplate
    full_html = f"""
    <html>
    <head>
        <style>
            {css_styles}
        </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """
    
    # 4. Use xhtml2pdf to generate the file
    with open(output_filename, "w+b") as result_file:
        # pisa.CreatePDF converts the HTML string to a PDF file
        pisa_status = pisa.CreatePDF(full_html, dest=result_file)
        
    if pisa_status.err:
        print(f"❌ Error generating PDF: {output_filename}")
    else:
        print(f"✅ Success! PDF saved as {output_filename}")
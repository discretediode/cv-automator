import markdown
from xhtml2pdf import pisa

def get_css(doc_type):
    """Returns the CSS styling for the PDF (Black & White, Compact)."""
    base_css = """
    @page {
        size: a4 portrait;
        margin: 1.0cm 1.2cm; /* Even tighter margins to maximize page real estate */
    }
    body {
        font-family: Helvetica, Arial, sans-serif;
        color: #000000;
        font-size: 9.5pt; /* Shrink slightly to match the dense, technical look */
        line-height: 1.15; /* Ultra-compact vertical spacing */
    }
    h1 {
        color: #000000; 
        font-size: 16pt;
        border-bottom: 1px solid #000000;
        padding-bottom: 2px;
        margin-top: 0;
        margin-bottom: 4px;
    }
    h2 {
        color: #000000;
        font-size: 11pt;
        text-transform: uppercase; /* Forces section headers to caps for a cleaner look */
        margin-top: 8px;
        margin-bottom: 3px;
    }
    h3 {
        font-size: 10pt;
        font-weight: bold;
        margin-top: 4px;
        margin-bottom: 1px;
    }
    p {
        margin-top: 1px;
        margin-bottom: 3px;
        text-align: justify; /* THIS creates the flush-right blocky text effect */
    }
    ul {
        margin-top: 1px;
        margin-bottom: 5px;
        padding-left: 15px; /* Pulls bullet points closer to the left margin */
    }
    li {
        margin-bottom: 2px;
        text-align: justify; /* Justifies multi-line bullet points */
    }
    """
    
    if doc_type == "anschreiben":
        base_css += """
        body { font-size: 11pt; line-height: 1.3; }
        p { text-align: justify; margin-bottom: 10px; margin-top: 4px; }
        h1 { border-bottom: none; margin-bottom: 12px; }
        """
        
    return base_css

def generate_pdf_from_markdown(markdown_text, output_filename, doc_type="cv"):
    """
    Converts Markdown to HTML, injects CSS, and renders a PDF using pure Python.
    """
    print(f"🎨 Rendering {output_filename} locally...")
    
    # Convert Markdown string to HTML string
    html_content = markdown.markdown(markdown_text, extensions=['extra', 'nl2br'])
    
    # Get the appropriate CSS
    css_styles = get_css(doc_type)
    
    # Wrap it in standard HTML boilerplate
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
    
    # Use xhtml2pdf to generate the file
    with open(output_filename, "w+b") as result_file:
        pisa_status = pisa.CreatePDF(full_html, dest=result_file)
        
    if pisa_status.err:
        print(f"❌ Error generating PDF: {output_filename}")
    else:
        print(f"✅ Success! PDF saved as {output_filename}")
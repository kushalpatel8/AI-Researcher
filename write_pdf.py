from langchain_core.tools import tool
from markdown_pdf import MarkdownPdf, Section
from datetime import datetime
from pathlib import Path

@tool
def render_markdown_pdf(markdown_content: str) -> str:
    """Render a Markdown document to PDF."""
    try:
        output_dir = Path("output").absolute()
        output_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        pdf_filename = output_dir / f"paper_{timestamp}.pdf"
        
        # Convert Markdown to PDF
        pdf = MarkdownPdf(toc_level=2)
        pdf.add_section(Section(markdown_content))
        pdf.save(str(pdf_filename))
        
        print(f"Successfully generated PDF at {pdf_filename}")
        return str(pdf_filename)

    except Exception as e:
        print(f"Error rendering PDF: {str(e)}")
        raise
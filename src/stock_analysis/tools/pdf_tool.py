import pdfkit

class PDFTool:
	name: str = "PDFTool"
	description: str = "Tool for creating a PDF from HTML content."
	args: dict = {
		"html_content": "HTML content to be converted to a PDF.",
		"output_path": "Path to save the resulting PDF file."
	}

	def __init__(self, name: str = "PDFTool"):
		self.name = name

	def create_pdf_from_html(self, html_content, output_path):
		"""
		Create a PDF file from HTML content.
		"""
		try:
			pdfkit.from_string(html_content, output_path)
			return f"PDF created successfully at {output_path}"
		except Exception as e:
			return f"Error creating PDF: {str(e)}"
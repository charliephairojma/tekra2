import pdfkit
from crewai_tools import BaseTool
from pydantic import BaseModel, Field
from typing import Any, Type


class PDFToolArgs(BaseModel):
	html_content: str = Field(..., description="Mandatory HTML content to be converted to a PDF.")
	output_path: str = Field(..., description="Mandatory path to save the resulting PDF file.")


class PDFTool(BaseTool):
	name: str = "PDFTool"
	description: str = "Tool for creating a PDF from HTML content."
	args_schema: Type[BaseModel] = PDFToolArgs

	def _run(self, html_content: str, output_path: str) -> Any:
		return self.create_pdf_from_html(html_content, output_path)

	def create_pdf_from_html(self, html_content, output_path):
		"""
		Create a PDF file from HTML content.
		"""
		try:
			pdfkit.from_string(html_content, output_path)
			return f"PDF created successfully at {output_path}"
		except Exception as e:
			return f"Error creating PDF: {str(e)}"
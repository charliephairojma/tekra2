import pdfkit
from crewai_tools import BaseTool
from pydantic import BaseModel, Field
from typing import Any, Type


class HTMLToolArgs(BaseModel):
	html_content: str = Field(..., description="Mandatory HTML content to be saved to a file.")
	output_path: str = Field(..., description="Mandatory path to save the resulting HTML file.")


class HTMLTool(BaseTool):
	name: str = "HTMLTool"
	description: str = "Tool for saving HTML content to a file."
	args_schema: Type[BaseModel] = HTMLToolArgs

	def _run(self, html_content: str, output_path: str) -> Any:
		return self.save_html_to_file(html_content, output_path)

	def save_html_to_file(self, html_content, output_path):
		"""
		Save HTML content to a file.
		"""
		try:
			with open(output_path, 'w') as file:
				file.write(html_content)
			return f"HTML file created successfully at {output_path}"
		except Exception as e:
			return f"Error creating HTML file: {str(e)}"
import os
from crewai_tools import PDFSearchTool

def load_pdfs_from_folder(folder_path):
    pdf_tools = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(folder_path, filename)
            pdf_tool = PDFSearchTool(pdf=pdf_path)
            pdf_tools.append(pdf_tool)
    return pdf_tools

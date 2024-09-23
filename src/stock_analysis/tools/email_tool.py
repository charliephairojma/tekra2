import smtplib
from typing import Any, Type

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from crewai_tools import BaseTool
from pydantic import BaseModel, Field


class EmailToolArgs(BaseModel):
	recipient: str = Field(..., description="Mandatory recipient's email address.")
	subject: str = Field(..., description="Mandatory subject of the email.")
	body: str = Field(..., description="Mandatory body of the email.")
	attachment_path: str = Field(..., description="Mandatory path to the attachment file.")


class EmailTool(BaseTool):
	name: str = "EmailTool"
	description: str = "Tool for sending an email with an attachment."
	args_schema: Type[BaseModel] = EmailToolArgs

	def _run(self, recipient: str, subject: str, body: str, attachment_path: str) -> Any:
		return self.send_email_with_attachment(recipient, subject, body, attachment_path)

	def send_email_with_attachment(self, recipient, subject, body, attachment_path):
		"""
		Send an email with an attachment.
		"""
		try:
			msg = MIMEMultipart()
			msg['From'] = 'your_email@example.com'
			msg['To'] = recipient
			msg['Subject'] = subject

			msg.attach(MIMEText(body, 'plain'))

			with open(attachment_path, "rb") as file:
				part = MIMEApplication(file.read(), Name=attachment_path.split('/')[-1])
			part['Content-Disposition'] = f'attachment; filename="{attachment_path.split("/")[-1]}"'
			msg.attach(part)

			server = smtplib.SMTP('smtp.gmail.com', 587)
			server.starttls()
			server.login('your_email@example.com', 'your_password')
			server.send_message(msg)
			server.quit()

			return "Email sent successfully"
		except Exception as e:
			return f"Error sending email: {str(e)}"
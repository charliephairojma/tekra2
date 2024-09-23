import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

class EmailTool:
	name: str = "EmailTool"
	description: str = "Tool for sending an email with an attachment."
	args: dict = {
		"recipient": "Recipient's email address.",
		"subject": "Subject of the email.",
		"body": "Body of the email.",
		"attachment_path": "Path to the attachment file."
	}

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
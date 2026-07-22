import smtplib
import mimetypes
from pathlib import Path
from typing import Union, List, Tuple, Optional
from core.config.config import get_data, change_data
from email.message import EmailMessage

class EmailService:
    @staticmethod
    def send_email(
        recipients: Union[str, List[str]],
        subject: str,
        body: Union[str, List[str]],
        attachments: Optional[List[Union[str, Path, Tuple[bytes, str]]]] = None
    ) -> None:
        """
        Sends a general text email with optional attachments.

        :param recipients: Single email string or list of email strings.
        :param subject: Email subject line.
        :param body: Main body text as a string, or a list of strings (joined by newlines).
        :param attachments: List containing either:
                            - File path strings or Path objects
                            - Tuples of (bytes_data, filename_str)
        """
        SMTP_SERVER = "smtp.gmail.com"
        SMTP_PORT = 587
        SENDER_EMAIL = get_data("email")
        SENDER_PASSWORD = get_data("email_pass")

        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = SENDER_EMAIL

        # Standardize recipients to a comma-separated string for headers
        if isinstance(recipients, list):
            msg['To'] = ", ".join(recipients)
        else:
            msg['To'] = recipients

        # Standardize body content
        if isinstance(body, list):
            body_text = "\n\n".join(body)
        else:
            body_text = body

        msg.set_content(body_text)

        # Process optional attachments
        if attachments:
            for item in attachments:
                # Case 1: In-memory bytes passed as (raw_bytes, filename)
                if isinstance(item, tuple):
                    file_bytes, filename = item
                    mime_type, _ = mimetypes.guess_type(filename)
                    maintype, subtype = (mime_type.split('/', 1) if mime_type else ('application', 'octet-stream'))

                    msg.add_attachment(
                        file_bytes,
                        maintype=maintype,
                        subtype=subtype,
                        filename=filename
                    )

                # Case 2: File paths passed as string or Path objects
                elif isinstance(item, (str, Path)):
                    file_path = Path(item)
                    if not file_path.is_file():
                        raise FileNotFoundError(f"Attachment file not found: {file_path}")

                    mime_type, _ = mimetypes.guess_type(file_path)
                    maintype, subtype = (mime_type.split('/', 1) if mime_type else ('application', 'octet-stream'))

                    with open(file_path, 'rb') as f:
                        msg.add_attachment(
                            f.read(),
                            maintype=maintype,
                            subtype=subtype,
                            filename=file_path.name
                        )

        # Send message
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)

    @staticmethod
    def send_export_email(recipient_email: str, excel_bytes: bytes, pdf_bytes: bytes) -> None:
        """Sends email with predefined export attachments (convenience wrapper)"""
        body = [
            "Hello,",
            "Please find attached the requested Library Dashboard data export, including the PDF visual summary and the Excel data sheets.",
            "Regards,\nLibrary Admin System"
        ]
        
        attachments = [
            (excel_bytes, 'Library_Data_Export.xlsx'),
            (pdf_bytes, 'Library_Dashboard_Summary.pdf')
        ]

        EmailService.send_email(
            recipients=recipient_email,
            subject='Library System - Exported Data Dashboard',
            body=body,
            attachments=attachments
        )

    def change_email(self, email: str) -> None:
        """Change email account"""
        change_data("email", email)

    def change_email_pass(self, email_pass: str) -> None:
        """Change email password"""
        change_data("email_pass", email_pass)
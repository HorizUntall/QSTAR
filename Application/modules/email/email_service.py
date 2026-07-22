import smtplib
from core.config.config import get_data, change_data
from email.message import EmailMessage

class EmailService:
    @staticmethod
    def send_export_email(recipient_email: str, excel_bytes: bytes, pdf_bytes: bytes) -> None:
        """Sends email"""
        SMTP_SERVER = "smtp.gmail.com" 
        SMTP_PORT = 587
        SENDER_EMAIL = get_data("email")
        SENDER_PASSWORD = get_data("email_pass")


        # 1. Build the modern message structure
        msg = EmailMessage()
        msg['Subject'] = 'Library System - Exported Data Dashboard'
        msg['From'] = SENDER_EMAIL
        msg['To'] = recipient_email
        msg.set_content(
            "Hello,\n\n"
            "Please find attached the requested Library Dashboard data export, "
            "including the PDF visual summary and the Excel data sheets.\n\n"
            "Regards,\n"
            "Library Admin System"
        )

        # Attach Excel in-memory data bytes
        msg.add_attachment(
            excel_bytes, 
            maintype='application', 
            subtype='vnd.openxmlformats-officedocument.spreadsheetml.sheet', 
            filename='Library_Data_Export.xlsx'
        )
        
        # Attach PDF in-memory data bytes
        msg.add_attachment(
            pdf_bytes, 
            maintype='application', 
            subtype='pdf', 
            filename='Library_Dashboard_Summary.pdf'
        )

        # 2. Fix the connection matching the legacy strategy (Port 587 + starttls)
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Secure the connection explicitly
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)

    def change_email(self, email: str) -> None:
        """Change email account"""
        change_data("email", email)

    def change_email_pass(self, email_pass: str) -> None:
        """Change email password"""
        change_data("email_pass", email_pass)
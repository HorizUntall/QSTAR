import smtplib
from email.message import EmailMessage

class EmailService:
    @staticmethod
    def send_export_email(recipient_email, excel_bytes, pdf_bytes):

        SMTP_SERVER = "smtp.gmail.com" 
        SMTP_PORT = 587
        SENDER_EMAIL = "qstarlibraryzrc@gmail.com"
        SENDER_PASSWORD = "owll nqwi cbew jhhq" 
        # --------------------------------------------------

        msg = EmailMessage()
        msg['Subject'] = 'Library System - Exported Data Dashboard'
        msg['From'] = SENDER_EMAIL
        msg['To'] = recipient_email
        msg.set_content("Hello,\n\nPlease find attached the requested Library Dashboard data export, including the PDF visual summary and the Excel data sheets.\n\nRegards,\nLibrary Admin System")

        # Attach Excel
        msg.add_attachment(excel_bytes, maintype='application', subtype='vnd.openxmlformats-officedocument.spreadsheetml.sheet', filename='Library_Data_Export.xlsx')
        
        # Attach PDF
        msg.add_attachment(pdf_bytes, maintype='application', subtype='pdf', filename='Library_Dashboard_Summary.pdf')

        # Send via SMTP over SSL
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
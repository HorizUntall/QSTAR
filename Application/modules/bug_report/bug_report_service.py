from datetime import datetime
from pathlib import Path

from modules.email.email_service import EmailService
from core.config.config import get_data
from core.log.logger import LOG_FILE

class BugReportService:
    def __init__(self, email_service: EmailService):
        self._email_service = email_service

    def report_bug(self, details: str) -> None:
        now = datetime.now()
        formatted_date_time = now.strftime('%b. %d, %Y %I:%M:%S %p').lower()

        recipient = get_data("email")
        subject = f"Bug Report: {formatted_date_time}"

        log_path = Path(LOG_FILE) if LOG_FILE else None
        attachments = [log_path] if log_path and log_path.is_file() else None

        self._email_service.send_email(
            recipients=recipient,
            subject=subject,
            body=details,
            attachments=attachments
        )
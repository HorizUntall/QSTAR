from email_validator import validate_email, EmailNotValidError
import logging
from typing import Dict, Any

from modules.email.email_service import EmailService
from modules.auth.decorators import admin_required

logger = logging.getLogger()

class EmailController:
    def __init__(self, email_service: EmailService) -> None:
        self._service = email_service

    # Public
    @admin_required
    def change_email(self, email: str) -> Dict[str, Any]:
        """Endpoint for changing/updating email"""
        try:
            email_info = validate_email(email, check_deliverability=False)
            self._service.change_email(email_info.email)

            return {
                "status": "success",
                "message": "Email updated successfully"
            }

        except EmailNotValidError as e:
            return {
                "status": "invalid",
                "message": "Invalid email"
            }

        except Exception as e:
            logger.exception(f"Exception occurred while changing email at email_controller: {str(e)}")
            return {
                "status": "error",
                "message": "Unexpected Exception"
            }

    # Public
    @admin_required
    def change_email_pass(self, email_pass: str) -> Dict[str, Any]:
        """Endpoint for changing/updating email password"""
        try:
            self._service.change_email_pass(email_pass)

            return {
                "status": "success",
                "message": "Email password updated successfully"
            }

        except Exception as e:
            logger.exception(f"Exception occurred while changing email password at email_controller: {str(e)}")
            return {
                "status": "error",
                "message": "Unexpected Exception"
            }
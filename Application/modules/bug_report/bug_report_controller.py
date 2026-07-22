import logging
from modules.bug_report.bug_report_service import BugReportService

logger = logging.getLogger()

class BugReportController:
    def __init__(self, bug_report_service: BugReportService):
        self._service = bug_report_service

    # Public
    def report_bug(self, details: str) -> None:
        try:
            self._service.report_bug(details=details)
            return {
                "status": "success",
                "message": "Report sent successfully"
            }

        except Exception as e:
            logger.exception(f"Exception occurred while reporting bugs: {str(e)}")
            return {
                "status": "error",
                "message": "Unexpected error occurred."
            }
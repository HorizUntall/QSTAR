from typing import Dict, Any
from pathlib import Path
from tkinter import filedialog, Tk

from modules.auth.decorators import admin_required
from modules.dashboard.dashboard_models import DashboardFiltersDTO
from modules.dashboard.dashboard_service import DashboardService

from modules.export.export_service import ExportService
from modules.email.email_service import EmailService

class DashboardController:
    def __init__(self, dashboard_service: DashboardService) -> None:
        self._service = dashboard_service

    # Public
    @admin_required
    def get_dashboard_data(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """Frontend calls this to populate the dashboard"""

        filters_dict: Dict[str, Any] = form_data.get("filters", {})
        filters = DashboardFiltersDTO(
            start_date=filters_dict.get("start_date"),
            end_date=filters_dict.get("end_date"),
            search_name=filters_dict.get("search_name"),
            batch=filters_dict.get("batch"),
            sex=filters_dict.get("sex"),
        )
        topUsersLimit = form_data.get("topUsersLimit", 5)
        num_batches = form_data.get("num_batches", 6)
        
        return {"status": "success", 
                "data": self._service.get_processed_dashboard_data(filters=filters, 
                                                                            topUsersLimit=topUsersLimit, 
                                                                            num_batches=num_batches)}
    
    # Public
    @admin_required
    def get_attendance_history(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """Frontend calls this to populate attendance history"""
        # page -> Page index
        # page_size -> amount of rows/data in a single page
        
        filters_dict: Dict[str, Any] = form_data.get("filters", {})
        filters = DashboardFiltersDTO(
            start_date=filters_dict.get("start_date"),
            end_date=filters_dict.get("end_date"),
            search_name=filters_dict.get("search_name"),
            batch=filters_dict.get("batch"),
            sex=filters_dict.get("sex"),
        )
        page = form_data.get("page", 1)
        page_size = form_data.get("page_size", 100)
        
        return {"status": "success", 
                "data": self._service.get_processed_attendance_history(filters=filters,
                                                                    page=page,
                                                                    page_size=page_size)}
    
    # Public
    @admin_required
    def get_registered_users(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """Frontend calls this to populate registered users list"""
        # page -> Page index
        # page_size -> amount of rows/data in a single page
        
        filters_dict: Dict[str, Any] = form_data.get("filters", {})
        filters = DashboardFiltersDTO(
            start_date=filters_dict.get("start_date"),
            end_date=filters_dict.get("end_date"),
            search_name=filters_dict.get("search_name"),
            batch=filters_dict.get("batch"),
            sex=filters_dict.get("sex"),
        )
        page = form_data.get("page", 1)
        page_size = form_data.get("page_size", 100)
        
        return {"status": "success", 
                "data": self._service.get_processed_registered_users(filters=filters,
                                                                page=page,
                                                                page_size=page_size)}
    
    # Public
    @admin_required
    def trigger_data_export(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """Frontend calls this to generate and route PDF/Excel exports"""
        try:
            # 1. Map the frontend filters to your DashboardFiltersDTO
            filters_dict: Dict[str, Any] = form_data.get("filters", {})
            filters = DashboardFiltersDTO(
                start_date=filters_dict.get("start_date"),
                end_date=filters_dict.get("end_date"),
                search_name=filters_dict.get("search_name"),
                batch=filters_dict.get("batch"),
                sex=filters_dict.get("sex"),
            )

            # 2. Fetch the Data 
            MAX_RECORDS = 1000000 
            
            history_res = self._service.get_processed_attendance_history(
                filters=filters, page=1, page_size=MAX_RECORDS
            )
            
            users_res = self._service.get_processed_registered_users(
                filters=filters, page=1, page_size=MAX_RECORDS
            )

            # 3. Clean and Split the Data for the Excel Tabs
            all_users = users_res.get("data", [])
            students = [u for u in all_users if u.get("user_type") == "student"]
            faculty = [u for u in all_users if u.get("user_type") == "faculty"]

            db_data = {
                'history': history_res.get("data", []),
                'users': students,
                'faculty': faculty
            }

            # 4. Generate the Binary Files in-memory
            # Fetch the actual dashboard aggregate data for the PDF charts
            dashboard_res = self._service.get_processed_dashboard_data(
                filters=filters, topUsersLimit=5, num_batches=6
            )

            excel_bytes = ExportService.generate_excel(db_data)
            
            # Pass the backend data instead of frontend base64 images
            pdf_bytes = ExportService.generate_pdf(
                dashboard_data=dashboard_res,
                start_date=filters.start_date,
                end_date=filters.end_date
            )

            export_method = form_data.get('export_method')

            # 5. Route the generated files based on user choice
            if export_method == 'email':
                target_email = form_data.get('target_email')
                if not target_email:
                    return {"status": "error", "message": "Email address is required."}
                
                EmailService.send_export_email(target_email, excel_bytes, pdf_bytes)
                return {"status": "success", "message": "Email sent successfully."}

            elif export_method == 'local':
                # Open native folder selection dialog (hidden main tkinter window)
                root = Tk()
                root.withdraw() 
                root.attributes('-topmost', True) 
                
                folder_path = filedialog.askdirectory(title="Select Folder to Save Export Files")
                root.destroy()
                
                if not folder_path:
                    return {"status": "error", "message": "Save cancelled by user."}

                target_dir = Path(folder_path)
                
                excel_file = target_dir / "Library_Data_Export.xlsx"
                pdf_file = target_dir / "Library_Dashboard_Summary.pdf"
                
                # pathlib allows us to write bytes directly without context managers
                excel_file.write_bytes(excel_bytes)
                pdf_file.write_bytes(pdf_bytes)

                return {"status": "success", "message": "Files saved locally."}
            
            else:
                return {"status": "error", "message": "Invalid export method selected."}

        except Exception as e:
            # Catching generic errors to prevent pywebview from silently crashing on bridge failures
            return {"status": "error", "message": f"Export failed: {str(e)}"}
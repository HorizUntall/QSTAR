import pandas as pd
from typing import Dict, Any, List

from modules.dashboard.dashboard_models import DashboardFiltersDTO
from modules.dashboard.dashboard_repo import DashboardRepository

class DashboardService:
    def __init__(self, dashboard_repo: DashboardRepository) -> None:
        self.repo = dashboard_repo

    def get_processed_dashboard_data(self, filters: DashboardFiltersDTO, topUsersLimit: int = 5, num_batches: int = 6) -> Dict[str, List[Dict[str, Any]] | Dict[str, Any]]:
        """Returns processed dashboard data using the filters"""

        visits_vs_time = self.repo.get_library_visits_vs_time(filters=filters)
        top_goers = self.repo.get_top_library_goers(filters=filters, limit=topUsersLimit)
        batch_visits = self.repo.get_visits_per_batch(filters=filters, num_batches=num_batches)

        gender: Dict[str, Any]
        gender_df = self.repo.get_gender_development(filters=filters)
        if gender_df.empty or gender_df['total_visits'].iloc[0] == 0:
            gender = {"total_visits": 0, "male_pct": 0.0, "female_pct": 0.0}
        else:
            row = gender_df.iloc[0]
            total = row['total_visits']
            gender = {
                "total_visits": int(total),
                "male_pct": round((row['male_count'] / total) * 100, 2),
                "female_pct": round((row['female_count'] / total) * 100, 2)
            }

        kpis: Dict[str, Any]
        kpis_df = self.repo.get_kpis(filters=filters)
        row = kpis_df.iloc[0]
        active_days = row['active_days'] or 1
        total_visits = row['total_visits'] or 0
        kpis = {
            "total_visits": int(total_visits),
            "avg_visits_per_day": round(total_visits / active_days, 2) if total_visits > 0 else 0.0,
            "avg_time_spent_minutes": round(row['avg_minutes_spent'], 2) if pd.notnull(row['avg_minutes_spent']) else 0.0
        }

        return {
            "visits_vs_time": visits_vs_time.to_dict(orient="records"),
            "top_goers": top_goers.to_dict(orient="records"),
            "batch_visits": batch_visits.to_dict(orient="records"),
            "gender": gender,
            "kpis": kpis
        }
    
    def get_processed_attendance_history(self, filters: DashboardFiltersDTO, page: int = 1, page_size: int = 100) -> Dict[str, Any]:
        """Returns processed attendance history using the filters"""
        
        df, total_records = self.repo.get_attendance_history(filters=filters, page=page, page_size=page_size)
        return {
            "data": df.to_dict(orient="records"),
            "pagination": {
                "total_records": total_records,
                "current_page": page, 
                "page_size": page_size,
                "total_pages": (total_records + page_size - 1) // page_size if total_records > 0 and page_size > 0 else 1
            }
        }
    
    def get_processed_registered_users(self, filters: DashboardFiltersDTO, page: int = 1, page_size: int = 100) -> Dict[str, Any]:
        """Returns processed registered users list using the filters"""

        df, total_records = self.repo.get_registered_users(filters=filters, page=page, page_size=page_size)
        return {
            "data": df.to_dict(orient="records"),
            "pagination": {
                "total_records": total_records,
                "current_page": page,
                "page_size": page_size,
                "total_pages": (total_records + page_size - 1) // page_size if total_records > 0 and page_size > 0 else 1
            }
        }
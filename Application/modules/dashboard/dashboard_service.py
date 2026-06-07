from modules.dashboard.dashboard_repo import DashboardRepository

class DashboardService:
    def __init__(self, dashboard_repo: DashboardRepository) -> None:
        self.repo = dashboard_repo
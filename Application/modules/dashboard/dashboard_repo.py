import pandas as pd
import sqlite3
import logging
from typing import Tuple, List, Any, Dict

from modules.dashboard.dashboard_models import DashboardFiltersDTO

class DashboardRepository:
    def __init__(self, db_conn: sqlite3.Connection) -> None:
        self.conn = db_conn

    def _build_base_query(self, filters: DashboardFiltersDTO) -> Tuple[str, List[Any]]:
        """
        Builds a common table expression (CTE) and dynamic WHERE clause.
        Returns the CTE SQL string and the list of parameters
        """

        # Unify students and faculties into a single temporary view for the query
        cte = """
        WITH CombinedUsers AS (
            SELECT id, first_name, last_name, batch, sex, 'student' AS user_type FROM student
            UNION ALL
            SELECT id, first_name, last_name, 'Faculty' as batch, sex, 'faculty' as user_type FROM faculty
        ),
        FilteredAttendance AS (
            SELECT 
                a.id as attendance_id, a.user_id, a.user_type, a.time_in, a.time_out,
                u.first_name, u.last_name, u.batch, u.sex
            FROM attendance a
            INNER JOIN CombinedUsers u ON a.user_id = u.id AND a.user_type = u.user_type
            WHERE 1=1
        """

        conditions = []
        params = []

        if filters.start_date:
            conditions.append("a.time_in >= ?")
            params.append(filters.start_date)

        if filters.end_date:
            conditions.append("a.time_in <= ?")
            params.append(filters.end_date)

        if filters.search_name:
            conditions.append("(u.first_name LIKE ? OR u.last_name LIKE ?)")
            search_term = f"%{filters.search_name}%"
            params.extend([search_term, search_term])

        if filters.sex:
            conditions.append("u.sex = ?")
            params.append(filters.sex.upper())

        if filters.batch:
            conditions.append("u.batch = ?")
            params.append(filters.batch)

        if conditions:
            cte += " AND " + " AND ".join(conditions)
        
        cte += "\n)" # Close the CTE
        return cte, params
    
    # ---------------------------------------------------------
    # 1. Library Visits vs Time
    # ---------------------------------------------------------
    def get_library_visits_vs_time(self, filters: DashboardFiltersDTO) -> pd.DataFrame:
        cte, params = self._build_base_query(filters)
        query  = cte + """
        SELECT DATE(time_in) as visit_date, COUNT(*) as frequency
        FROM FilteredAttendance
        GROUP BY DATE(time_in)
        ORDER BY visit_date ASC
        """
        return pd.read_sql_query(query, self.conn, params=params)
    
    # ---------------------------------------------------------
    # 2. Top Library Goers
    # ---------------------------------------------------------
    def get_top_library_goers(self, filters: DashboardFiltersDTO, limit: int = 5) -> pd.DataFrame:
        cte, params = self._build_base_query(filters)
        query = cte + """
        SELECT user_id, first_name, last_name, user_type, batch, COUNT(*) as total_visits
        FROM FilteredAttendance
        GROUP BY user_id, user_type, first_name, last_name, batch
        ORDER BY total_visits DESC
        LIMIT ?
        """
        params.append(limit)
        return pd.read_sql_query(query, self.conn, params=params)
    
    # ---------------------------------------------------------
    # 3. Library Visits per Batch
    # ---------------------------------------------------------
    def get_visits_per_batch(self, filters: DashboardFiltersDTO, num_batches: int = 6) -> pd.DataFrame:
        cte, params = self._build_base_query(filters)

        # Group by batch. Order Faculty to the end, and sort batches descending.
        query = cte + """
        SELECT batch, COUNT(*) as frequency
        FROM FilteredAttendance
        GROUP BY batch
        ORDER BY
            CASE WHEN batch = 'Faculty' THEN 1 ELSE 0 END ASC,
            batch DESC
        LIMIT ?
        """
        params.append(num_batches)
        return pd.read_sql_query(query, self.conn, params=params)
    
    # ---------------------------------------------------------
    # 4. Gender and Development
    # ---------------------------------------------------------
    def get_gender_development(self, filters: DashboardFiltersDTO) -> pd.DataFrame:
        cte, params = self._build_base_query(filters)
        query = cte + """
        SELECT
            COUNT(*) as total_visits,
            SUM(CASE WHEN sex = 'M' THEN 1 ELSE 0 END) as male_count,
            SUM(CASE WHEN sex = 'F' THEN 1 ELSE 0 END) as female_count
        FROM FilteredAttendance
        """
        return pd.read_sql_query(query, self.conn, params=params)
    
    # ---------------------------------------------------------
    # 5. Others (KPIs)
    # ---------------------------------------------------------
    def get_kpis(self, filters: DashboardFiltersDTO) -> pd.DataFrame:
        cte, params = self._build_base_query(filters)
        # SQLite Julianday returns fractional days. So, multiply by 24*60 for minutes
        query = cte + """
        SELECT
            COUNT(*) as total_visits,
            COUNT(DISTINCT DATE(time_in)) as active_days,
            AVG((JULIANDAY(time_out) - JULIANDAY(time_in)) * 24 * 60) as avg_minutes_spent
        FROM FilteredAttendance
        """
        return pd.read_sql_query(query, self.conn, params=params)
    
    # ---------------------------------------------------------
    # 6. Paginated Attendance History List
    # ---------------------------------------------------------
    def get_attendance_history(self, filters: DashboardFiltersDTO, page: int = 1, page_size: int = 100) -> Tuple[pd.DataFrame, int]:
        cte, params = self._build_base_query(filters)
        offset = (page - 1) * page_size

        # Query 1: Get Total Count for UI pagination logic
        count_query = cte + "SELECT COUNT(*) as total FROM FilteredAttendance"
        cursor = self.conn.cursor()
        cursor.execute(count_query, params)
        total_records = cursor.fetchone()[0] or 0

        # Query 2: Get Paginated Data
        data_query = cte + """
        SELECT attendance_id, user_id, first_name, last_name, user_type, batch, time_in, time_out
        FROM FilteredAttendance
        ORDER BY time_in DESC
        LIMIT ? OFFSET ?
        """

        # Create a new list of params to avoid appending to the original list multiple times
        data_params = params + [page_size, offset]
        df = pd.read_sql_query(data_query, self.conn, params=data_params)

        return df, total_records
    
    # ---------------------------------------------------------
    # 7. Paginated Registered Users
    # ---------------------------------------------------------
    def get_registered_users(self, filters: DashboardFiltersDTO, page: int = 1, page_size: int = 100) -> Tuple[pd.DataFrame, int]:
        """
        This targets the CombinedUsers view directly, completely ignoring attendance.
        """
        cte = """
        WITH CombinedUsers AS (
            SELECT id, first_name, last_name, batch, sex, 'student' AS user_type FROM student
            UNION ALL 
            SELECT id, first_name, last_name, 'Faculty' as batch, sex, 'faculty' as user_type FROM faculty
        )
        """

        conditions = []
        params = []

        if filters.search_name:
            conditions.append("(first_name LIKE ? OR last_name LIKE ?)")
            search_term = f"%{filters.search_name}%"
            params.extend([search_term, search_term])
        if filters.sex:
            conditions.append("sex = ?")
            params.append(filters.sex.upper())
        if filters.batch:
            conditions.append("batch = ?")
            params.append(filters.batch)
        
        where_clause = ""
        if conditions:
            where_clause = " WHERE " + " AND ".join(conditions)
        
        offset = (page - 1) * page_size

        # Query Count
        cursor = self.conn.cursor()
        cursor.execute(cte + f"SELECT COUNT(*) as total FROM CombinedUsers {where_clause}", params)
        total_records = cursor.fetchone()[0] or 0

        # Query Data
        data_query = cte + f"""
        SELECT id, first_name, last_name, batch, sex, user_type
        FROM CombinedUsers
        {where_clause}
        ORDER BY last_name ASC, first_name ASC
        LIMIT ? OFFSET ?
        """
        df = pd.read_sql_query(data_query, self.conn, params=params + [page_size, offset])

        return df, total_records
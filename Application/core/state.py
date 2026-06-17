class AppState:
    def __init__(self):
        # Starts as False every time the desktop app opens
        self.is_admin_logged_in = False  

    def log_in(self):
        self.is_admin_logged_in = True

    def log_out(self):
        self.is_admin_logged_in = False

app_state = AppState()
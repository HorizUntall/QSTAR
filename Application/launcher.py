# launcher.py
import os
import sys
import json
import zipfile
import subprocess
import urllib.request
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, ttk
import shutil

REPO_SLUG = "HorizUntall/QSTAR"
URL = f"https://api.github.com/repos/{REPO_SLUG}/releases/latest"

class AppLauncher:
    def __init__(self):
        if getattr(sys, 'frozen', False):
            self.install_dir = Path(sys.executable).parent
            self.version_file = self.install_dir / "_internal" / "version.json"
            self.main_app_exe = self.install_dir / "QSTAR_Engine.exe"
        else:
            self.install_dir = Path(__file__).parent
            self.version_file = self.install_dir / "version.json"
            self.main_app_exe = self.install_dir / "main.py"

    def get_local_version(self):
        try:
            with open(self.version_file, "r") as f:
                return json.load(f).get("version", "2.0.0").strip()
        except Exception:
            return "2.0.0"

    def execute_pipeline(self):
        # Create a hidden base Tkinter window to host native system dialog boxes safely
        root = tk.Tk()
        root.withdraw()

        # 1. Connection Verification
        try:
            urllib.request.urlopen("https://api.github.com", timeout=3)
            has_internet = True
        except Exception:
            has_internet = False

        if not has_internet:
            self.launch_engine()
            return

        # 2. Query Remote GitHub Repository Assets
        try:
            local_v = self.get_local_version()
            req = urllib.request.Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode())
            latest_v = data["tag_name"].replace("v", "").strip()

            # 3. Handle Active Update Match
            if latest_v > local_v:
                user_consent = messagebox.askyesno(
                    "Update Found!",
                    f"A newer patch deployment (v{latest_v}) is available.\n"
                    f"Your current baseline is v{local_v}.\n\n"
                    "Would you like to install the update now?"
                )
                
                if user_consent:
                    download_url = None
                    for asset in data.get("assets", []):
                        if asset["name"] == "update.zip":
                            download_url = asset["browser_download_url"]
                            break
                    
                    if download_url:
                        self.render_loading_window(download_url)
                        return

        except Exception as err:
            print(f"Network checking layer safely bypassed: {err}")

        self.launch_engine()

    def render_loading_window(self, download_url):
        # Build clean window asset overlay
        loader = tk.Tk()
        loader.title("QSTAR System Update")
        loader.geometry("380x160")
        loader.resizable(False, False)
        loader.eval('tk::PlaceWindow . center')

        status_lbl = ttk.Label(loader, text="Initializing network connection...", font=("Arial", 10))
        status_lbl.pack(pady=20)

        progress_bar = ttk.Progressbar(loader, orient="horizontal", length=300, mode="determinate")
        progress_bar.pack(pady=5)

        def download_sequence():
            try:
                zip_path = self.install_dir / "update.zip"
                
                # Update bar live relative to chunk byte sizes
                def network_hook(block_num, block_size, total_size):
                    if total_size > 0:
                        bytes_read = block_num * block_size
                        percentage = int((bytes_read / total_size) * 100)
                        progress_bar['value'] = min(percentage, 100)
                        loader.update_idletasks()

                status_lbl.config(text="Downloading application package from GitHub...")
                urllib.request.urlretrieve(download_url, zip_path, reporthook=network_hook)
                
                status_lbl.config(text="Extracting patch structures...")
                progress_bar.config(mode="indeterminate")
                progress_bar.start(12)
                loader.update_idletasks()

                # --- SAFE OVERWRITE HANDLING ---
                # Delete the old engine core executable first to ensure it's unblocked
                if self.main_app_exe.exists():
                    try:
                        os.remove(self.main_app_exe)
                    except Exception:
                        pass # Ignore if Windows is delaying file handle disposal

                # Extract update package directly over the current running directory layout.
                # ZipFile automatically overwrites existing files inside _internal/ smoothly.
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(self.install_dir)
                
                try:
                    os.remove(zip_path)
                except Exception:
                    pass
                    
                progress_bar.stop()
                
                messagebox.showinfo("Update Complete", "Patch applied successfully! Launching QSTAR Attendance...")
                loader.destroy()
                self.launch_engine()

            except Exception as failure:
                messagebox.showerror("Deployment Error", f"Failed to complete patch installation: {failure}")
                loader.destroy()
                self.launch_engine()

        loader.after(200, download_sequence)
        loader.mainloop()

    def launch_engine(self):
        # Spawn our standalone engine binary and drop launcher context seamlessly
        if getattr(sys, 'frozen', False):
            if self.main_app_exe.exists():
                subprocess.Popen([str(self.main_app_exe)])
            else:
                messagebox.showerror("Error", "QSTAR_Engine.exe could not be found in the current directory.")
        else:
            subprocess.Popen([sys.executable, str(self.main_app_exe)])
        sys.exit(0)

if __name__ == "__main__":
    launcher = AppLauncher()
    launcher.execute_pipeline()
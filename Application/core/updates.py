import os
import sys
import json
import zipfile
import urllib.request
from pathlib import Path
import webview

class AppUpdater:
    def __init__(self, window: webview.Window, root_dir: Path, repo_slug: str) -> None:
        """
        Handles the background update sequence.
        """
        self.window = window
        self.root_dir = root_dir
        self.repo_url = f"https://api.github.com/repos/{repo_slug}/releases/latest"

    def run_check(self) -> None:
        # 1. Quick connection check (FIXED: Changed http to https)
        try:
            urllib.request.urlopen("https://api.github.com", timeout=3)
        except Exception as conn_err:
            print(f"[Updater] Network test failed: {conn_err}. Skipping.")
            return
        
        # 2. Read local version from json
        try:
            with open(self.root_dir / "version.json", "r") as f:
                local_version = json.load(f).get("version", "2.0.0").strip()
        except Exception as file_err:
            print(f"[Updater] version.json missing or unreadable: {file_err}")
            local_version = "2.0.0"

        # 3. Pull latest release info from GitHub API
        try:
            req = urllib.request.Request(self.repo_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                release_data = json.loads(response.read().decode())

            latest_version = release_data["tag_name"].replace("v", "").strip()
            
            print(f"[Updater] Version check -> Local: {local_version} | GitHub: {latest_version}")

            # 4. Prompt user if an update is found
            # Note: String comparison ("2.0.3" > "2.0.0") works perfectly here.
            if latest_version > local_version:
                
                # Double check that pywebview window object is alive and ready
                if not self.window:
                    print("[Updater] Window not ready to display dialog.")
                    return

                user_accepted = self.window.create_confirmation_dialog(
                    "Update Found!",
                    f"A new update (v{latest_version}) is available. Do you want to install it?"
                )

                if user_accepted:
                    # Find update.zip asset
                    download_url = None
                    for asset in release_data.get("assets", []):
                        if asset["name"] == "update.zip":
                            download_url = asset["browser_download_url"]
                            break
                    
                    if not download_url:
                        print("[Updater] Error: 'update.zip' not found in release assets.")
                        return
                    
                    # Download and extract directly into _internal/
                    print("[Updater] Downloading patch...")
                    zip_path = self.root_dir / "update.zip"
                    urllib.request.urlretrieve(download_url, zip_path)

                    print("[Updater] Overwriting old program code...")
                    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                        zip_ref.extractall(self.root_dir)

                    os.remove(zip_path)

                    # Notify and terminate for a clean reboot
                    self.window.create_confirmation_dialog(
                        "Update Complete",
                        "The update was successfully installed! Please reopen the application to apply changes."
                    )
                    os._exit(0)
            else:
                print("[Updater] Application is completely up to date.")

        except Exception as e:
            print(f"[Updater] Background process error: {e}")
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
        # Quick connection check (3-sec timeout)
        try:
            urllib.request.urlopen("http://api.github.com", timeout=3)
        except Exception:
            print("[Updater] Offline mode or connection timeout. Skipping.")
            return
        
        # Read local version from json
        try:
            with open(self.root_dir / "version.json", "r") as f:
                local_version = json.load(f).get("version", "2.0.0")
        except Exception:
            local_version = "2.0.0"

        # Pull latest release info from GitHub API
        try:
            req = urllib.request.Request(self.repo_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                release_data = json.loads(response.read().decode())

            latest_version = release_data["tag_name"].replace("v", "")

            # Prompt user if an update is found
            if latest_version > local_version:
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

                    # 6. Notify and terminate for a clean reboot
                    self.window.create_confirmation_dialog(
                        "Update Complete",
                        "The update was successfully installed! Please reopen the application to apply changes."
                    )
                    os._exit(0)

        except Exception as e:
            print(f"[Updater] Background process error: {e}")
from modules.scanner.qrscanner import QRCodeScanner
from webview import Window
import json

class ScannerAPI:
    def __init__(self, qrscanner: QRCodeScanner) -> None:
        self._scanner: QRCodeScanner = qrscanner
        self._window: Window | None = None

    # Private
    def _setWindow(self, window_instance: Window):
        self._window = window_instance
        self._scanner.handleScan = self._handle_qr_detected

    # Private
    def _handle_qr_detected(self, code: str) -> None:
        """When the qrcodescanner method detects a valid qr, it informs the frontend"""
        if not self._window: 
            return
        
        escaped_code = json.dumps(code)
        js_code = f"window.dispatchEvent(new CustomEvent('qrDetected', {{detail: '{escaped_code}'}}));"
        
        self._window.evaluate_js(js_code)

    # Public
    def fetch_frame(self) -> str:
        """Frontend calls this to fetch frame from the camera """
        if not self._scanner.update_frames:
            return ""

        b64frame = self._scanner.fetch_frame()
        if not b64frame:
            return ""
        
        return f"data:image/jpeg;base64,{b64frame}"
    
    # Public
    def pause_camera(self) -> None: 
        """Pauses the camera to prevent accientally scanning QR Code when not needed"""
        self._scanner.stop_scanning()

    # Public
    def resume_camera(self) -> None:
        self._scanner.start_scanning()

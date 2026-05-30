import cv2
from threading import Thread, Timer

class QRCodeScanner:
    def __init__(self, verifierFunction: function, attendanceFunction: function, scan_interval: int = 10, vidSrc: int = 0) -> None:
        self.running: bool  = False
        self.last_scanned_qr: str = None
        self.capture_thread: Thread = None
        self.timer_thread: Timer = None
        self.scan_interval: int = scan_interval
        self.vidSrc: int | str = vidSrc
        self.cap: cv2.VideoCapture = None
        self.verifier: function = verifierFunction
        self.attendance: function = attendanceFunction
        self.update_frames: bool = False

    def capture_frames(self):
        if self.cap is None:
            self.cap = cv2.VideoCapture(self.vidSrc)

        while self.running:
            
            if self.cap:

                success, img = self.cap.read()

                if not success: continue

                if self.update_frames:
                    ...


    def start_scanning(self):
        if not self.running:
            self.running = True
            self.capture_thread = Thread(target=self.capture_frames)
            self.capture_thread.daemon = True
            self.capture_thread.start()
        self.update_frames = True

    def stop_scanning(self):
        self.update_frames = False
    
    def start_timer(self):
        if self.timer_thread and self.timer_thread.is_alive():
            self.timer_thread.cancel()
        self.timer_thread = Timer(self.scan_interval, self.clear_last_scanned_qr)
        self.timer_thread.start()

    def clear_last_scanned_qr(self):
        self.last_scanned_qr = None

    def cleanup(self):
        self.running = False
        if self.capture_thread is not None:
            self.capture_thread.join(timeout=1)
        if self.cap is not None:
            self.cap.release()
        if self.timer_thread is not None:
            self.timer_thread.cancel()
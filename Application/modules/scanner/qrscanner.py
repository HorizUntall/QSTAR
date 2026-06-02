import time
import cv2
import logging
from threading import Thread, Timer
from pyzbar.pyzbar import decode
import base64
from typing import Callable
from webview import Window

class QRCodeScanner:
    def __init__(self, verifierFunction: Callable, attendanceFunction: Callable, scan_interval: int = 10, vidSrc: int = 0) -> None:
        self.running: bool  = False
        self.last_scanned_qr: str = None
        self.capture_thread: Thread = None
        self.timer_thread: Timer = None
        self.scan_interval: int = scan_interval
        self.vidSrc: int | str = vidSrc
        self.cap: cv2.VideoCapture = None
        self.verifier: Callable = verifierFunction
        self.attendance: Callable = attendanceFunction
        self.update_frames: bool = False
        self.window: Window | None = None
        self.frame_counter: int = 0
        self.sending_frame: bool = False

    def capture_frames(self):
        if self.cap is None:
            self.cap = cv2.VideoCapture(self.vidSrc)

        while self.running:

            start_time = time.time()
            
            if self.cap:

                success, img = self.cap.read()

                if not success: 
                    continue

                if self.update_frames:
                    
                    try:
                        # _, buffer = cv2.imencode('.jpg', cv2.flip(img, 1))
                        frame = cv2.flip(img, 1)
                        frame = cv2.resize(frame, (640, 480))
                        _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 60])

                        frame_bytes = base64.b64encode(buffer)

                        if self.window and not self.sending_frame:
                            self.sending_frame = True

                            b64frame = frame_bytes.decode('utf-8')
                            js = f"""
                            updateFrame("data:image/jpeg;base64,{b64frame}");
                            """

                            try: 
                                self.window.evaluate_js(js)
                            except Exception as e:
                                logging.error("Error in qrscanner.py window,", exc_info=True)
                            finally:
                                self.sending_frame = False

                        self.frame_counter += 1
                        if self.frame_counter == 3:
                            self.frame_counter = 0

                            for code in decode(img):
                                decoded_data = code.data.decode("utf-8")

                                if decoded_data and decoded_data != self.last_scanned_qr:
                                    self.last_scanned_qr = decoded_data
                                    self.start_timer()
                                    self.attendance(self.verifier(decoded_data))

                    except Exception as e:
                        ...
                        # logging.error("Error in qrscanner.py loop", exc_info=True)

            # 15 FPS
            elapsed = time.time() - start_time
            sleep_time = max(0, (1 / 15) - elapsed)
            time.sleep(sleep_time)


    def start_scanning(self):
        if not self.running:
            self.running = True
            self.capture_thread = Thread(target=self.capture_frames, daemon=True)
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
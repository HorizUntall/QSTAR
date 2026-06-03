import cv2
import base64
import threading
from threading import Lock
import webview
from pyzbar.pyzbar import decode
import sys
import time
from webview.errors import JavascriptException, WebViewException

window = None
stop_event = threading.Event()
window_alive = True

window_lock = Lock()

def camera_loop():
    global window_alive, window_lock
    cap = cv2.VideoCapture(2)

    while not stop_event.is_set():
        time.sleep(0.01) # This line of code prevents error when closing the program
        ret, frame = cap.read()
        if not ret:
            continue

        if not window_alive or stop_event.is_set():
            break

        _, buffer = cv2.imencode('.jpg', frame)

        b64 = base64.b64encode(buffer).decode('utf-8')

        js = f"""
        updateFrame("data:image/jpeg;base64,{b64}");
        """

        try:
            # window.evaluate_js(js)
            window.run_js(js)
        except WebViewException:
            print("sds")
            pass
        except:
            break

        for code in decode(frame):
            decoded_data = code.data.decode("utf-8")

        time.sleep(0.03)

    cap.release()

def start_camera():
    threading.Thread(target=camera_loop, daemon=True).start()

def on_closing():
    global window_alive
    window_alive = False
    stop_event.set()

html = """
<!DOCTYPE html>
<html>
<body>
    <img id="video" width="640">

    <script>
        function updateFrame(src) {
            document.getElementById("video").src = src;
        }
    </script>
</body>
</html>
"""

window = webview.create_window("Camera", html=html)
window.events.closing += on_closing
start_camera()
webview.start()
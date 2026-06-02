import cv2
import base64
import threading
import webview
from pyzbar.pyzbar import decode

window = None

def camera_loop():
    cap = cv2.VideoCapture(2)

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        _, buffer = cv2.imencode('.jpg', frame)

        b64 = base64.b64encode(buffer).decode('utf-8')

        js = f"""
        updateFrame("data:image/jpeg;base64,{b64}");
        """

        try:
            window.evaluate_js(js)
        except:
            break

        for code in decode(frame):
            decoded_data = code.data.decode("utf-8")

def start_camera():
    threading.Thread(target=camera_loop, daemon=True).start()

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
start_camera()
webview.start()
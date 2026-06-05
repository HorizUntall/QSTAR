// ========= Handles Camera View ==============
function updateFrame(src) {
  document.getElementById("cameraFeed").src = src;
}

function streamCamera() {
  pywebview.api.scanner
    .fetch_frame()
    .then((frameData) => {
      if (frameData) {
        updateFrame(frameData);
      }
      requestAnimationFrame(streamCamera);
    })
    .catch((err) => {
      console.log("App is closing, stream is stopped");
    });
}

window.addEventListener("pywebviewready", streamCamera);

// =========== QR Code Detected ================
window.addEventListener("qrDetected", async (event) => {
  const qrCodeData = event.detail;

  // const response = await pywebview.api.verifyAndProcessQR(qrCodeData);

  // if (response.status === "success") {
  //   console.log("Success");
  // } else {
  //   console.log("Invalid");
  // }

  // ==== Test Register
  data = {
    id: qrCodeData,
    firstName: "testFirstname",
    lastName: "testLastname",
    sex: "male",
    type: "student",
    batch: 2024,
  };

  const response = await pywebview.api.register_new_user(data);

  if (response.status === "success") {
    console.log("Successs");
  } else {
    console.log("Invalid");
  }
});

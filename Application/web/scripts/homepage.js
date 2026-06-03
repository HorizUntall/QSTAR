function updateFrame(src) {
  document.getElementById("cameraFeed").src = src;
}

function streamCamera() {
  pywebview.api
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

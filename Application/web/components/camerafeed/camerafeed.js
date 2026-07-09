class CameraFeedComponent extends HTMLElement {
  constructor() {
    super();
    this.cameraAnimationId = null;
    this.isStreaming = false;
    this.isChangingCamera = false;
    this.currentCameraId = 0;
    this.minCameraId = 0;
    this.maxCameraId = 5;
  }

  connectedCallback() {
    this.innerHTML = this.layout();
    this.isStreaming = true;

    if (
      window.pywebview &&
      window.pywebview.api &&
      window.pywebview.api.scanner.get_cam_id
    ) {
      window.pywebview.api.scanner
        .get_cam_id()
        .then((realId) => {
          this.currentCameraId = realId;
          const label = this.querySelector("#cameraLabel");
          if (label) label.textContent = `Camera ${this.currentCameraId}`;
        })
        .catch((err) =>
          console.error("Could not fetch initial camera ID", err),
        );
    }

    window.pywebview.api.scanner.resume_camera();
    this.streamCamera();
    this.setupCameraControls();
  }

  disconnectedCallback() {
    this.isStreaming = false;
    if (this.cameraAnimationId) {
      cancelAnimationFrame(this.cameraAnimationId);
      window.pywebview.api.scanner.pause_camera();
      this.cameraAnimationId = null;
    }
  }

  streamCamera() {
    if (!this.isStreaming) return;

    if (this.isChangingCamera) {
      this.cameraAnimationId = requestAnimationFrame(() => this.streamCamera());
      return;
    }

    window.pywebview.api.scanner
      .fetch_frame()
      .then((frameData) => {
        if (!this.isStreaming) return;

        const feedImg = document.getElementById("cameraFeed");
        const errorOverlay = document.getElementById("cameraError");

        if (frameData) {
          // Frame exists: show image, hide error overlay
          if (feedImg) {
            feedImg.src = frameData;
            feedImg.style.display = "block";
          }
          if (errorOverlay) errorOverlay.style.display = "none";
        } else {
          // No frame from Python backend: hide image, show error message
          if (feedImg) feedImg.style.display = "none";
          if (errorOverlay) {
            errorOverlay.textContent = `Camera index ${this.currentCameraId} is unavailable or disconnected.`;
            errorOverlay.style.display = "flex";
          }
        }

        this.cameraAnimationId = requestAnimationFrame(() =>
          this.streamCamera(),
        );
      })
      .catch((err) => {
        console.log("Stream stopped or interrupted", err);
        this.cameraAnimationId = requestAnimationFrame(() =>
          this.streamCamera(),
        );
      });
  }

  setupCameraControls() {
    const prevBtn = this.querySelector("#prevCamera");
    const nextBtn = this.querySelector("#nextCamera");

    prevBtn?.addEventListener("click", () => this.updateCameraId(-1));
    nextBtn?.addEventListener("click", () => this.updateCameraId(1));
  }

  updateCameraId(direction) {
    if (this.isChangingCamera) return;

    let newId = this.currentCameraId + direction;

    if (newId >= this.minCameraId && newId <= this.maxCameraId) {
      this.currentCameraId = newId;
      this.isChangingCamera = true;

      const label = this.querySelector("#cameraLabel");
      if (label) label.textContent = `Camera ${this.currentCameraId}`;

      // Show temporary loading status inside container
      const errorOverlay = document.getElementById("cameraError");
      const feedImg = document.getElementById("cameraFeed");
      if (feedImg) feedImg.style.display = "none";
      if (errorOverlay) {
        errorOverlay.textContent = "Switching camera resource...";
        errorOverlay.style.display = "flex";
      }

      if (
        window.pywebview.api &&
        window.pywebview.api.scanner &&
        window.pywebview.api.scanner.change_camera
      ) {
        window.pywebview.api.scanner.change_camera(this.currentCameraId);

        // Give the backend thread 800ms to test initialization before letting stream resume
        setTimeout(() => {
          this.isChangingCamera = false;
        }, 800);
      } else {
        this.isChangingCamera = false;
      }
    }
  }

  layout() {
    return /*html*/ `
    <div class="camera-container" style="position: relative;">
        <div id="cameraError" style="display: none; width: 100%; height: 100%; color: #fff; background: #222; align-items: center; justify-content: center; text-align: center; padding: 20px; font-family: sans-serif; box-sizing: border-box;"></div>
        <img id="cameraFeed" src="" alt="camera" /> 
    </div>
    <div class="camera-controls">
        <button id="prevCamera" class="control-btn" aria-label="Previous Camera">◀</button>
        <span id="cameraLabel">Camera ${this.currentCameraId}</span>
        <button id="nextCamera" class="control-btn" aria-label="Next Camera">▶</button>
    </div>
        `;
  }
}

customElements.define("app-camerafeed", CameraFeedComponent);

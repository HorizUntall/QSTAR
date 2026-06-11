class CameraFeedComponent extends HTMLElement {
  constructor() {
    super();
    this.cameraAnimationId = null;
    this.isStreaming = false;
  }

  connectedCallback() {
    this.innerHTML = this.layout();
    this.isStreaming = true;
    this.streamCamera();
  }

  disconnectedCallback() {
    this.isStreaming = false;
    if (this.cameraAnimationId) {
      cancelAnimationFrame(this.cameraAnimationId);
      this.cameraAnimationId = null;
    }
  }

  streamCamera() {
    if (!this.isStreaming) return;

    window.pywebview.api.scanner
      .fetch_frame()
      .then((frameData) => {
        if (!this.isStreaming) return;

        const feedImg = document.getElementById("cameraFeed");
        if (feedImg && frameData) {
          feedImg.src = frameData;
          this.cameraAnimationId = requestAnimationFrame(() =>
            this.streamCamera(),
          );
        }
      })
      .catch((err) => console.log("Stream stopped or interrupted", err));
  }

  layout() {
    return /*html*/ `
    <div class="camera-container">
        <img id="cameraFeed" src="" alt="camera" /> 
    </div>
        `;
  }
}

// Custom Element Tag Name
customElements.define("app-camerafeed", CameraFeedComponent);

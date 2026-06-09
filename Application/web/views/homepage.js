class HomepageComponent extends HTMLElement {
  constructor() {
    super();
    this.cameraAnimationId = null;
  }

  connectedCallback() {
    this.innerHTML = /*html*/ `<nav>
        <div class="nav-left">
          <h1>Q-STAR</h1>
          <h2>QR-Based Attendance</h2>
        </div>
      </nav>
      <main>
        <h2>Homepage View</h2>
        <div class="camera">
          <img id="cameraFeed" src="" alt="camera" />
        </div>
      </main> `;

    console.log("Homepage layout attached natively. Starting stream...");
    this.streamCamera();
  }

  // Cleanup
  disconnectedCallback() {
    console.log("Leaving homepage layout. Clearing animation frame loops.");
    if (this.cameraAnimationId) {
      cancelAnimationFrame(this.cameraAnimationId);
    }
  }

  streamCamera() {
    window.pywebview.api.scanner
      .fetch_frame()
      .then((frameData) => {
        const feedImg = document.getElementById("cameraFeed");
        if (feedImg && frameData) {
          feedImg.src = frameData;
          this.cameraAnimationId = requestAnimationFrame(() =>
            this.streamCamera(),
          );
        }
      })
      .catch((err) => console.log("Stream stopped or interrupted"));
  }
}

// Custom Element Tag Name
customElements.define("app-homepage", HomepageComponent);

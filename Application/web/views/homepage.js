// Import components
import "../components/navbar.js";

class HomepageComponent extends HTMLElement {
  constructor() {
    super();
    this.cameraAnimationId = null;

    // Bind listener to the class instance so it can be cleanly removed later
    this.handleQRScan = async (event) => {
      const qrCodeData = event.detail;
      console.log("QR caught by component logic:", qrCodeData);

      const response =
        await window.pywebview.api.processScannedCode(qrCodeData);
    };
  }

  // Runs instantly when opening this page
  connectedCallback() {
    this.innerHTML = this.layout();
    console.log("Homepage layout attached natively. Starting stream...");
    this.streamCamera();

    // Listens for qr detection
    window.addEventListener("qrDetected", this.handleQRScan);
  }

  // Cleanup when switching page
  disconnectedCallback() {
    console.log("Leaving homepage layout. Clearing animation frame loops.");
    if (this.cameraAnimationId) {
      cancelAnimationFrame(this.cameraAnimationId);
    }

    window.removeEventListener("qrDetected", this.handleQRScan);
    console.log("Cleaned up camera loops and QR event listeners successfully.");
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

  // HTML Code goes here
  layout() {
    return /*html*/ `
    <app-navbar></app-navbar>
    <main>
      <h2>Homepage View</h2>
      <div class="camera">
        <img id="cameraFeed" src="" alt="camera" />
      </div>
    </main> `;
  }
}

// Custom Element Tag Name
customElements.define("app-homepage", HomepageComponent);

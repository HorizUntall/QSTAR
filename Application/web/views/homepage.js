// Import components
import "../components/navbar.js";
import "../components/camerafeed.js";
import "../components/clock.js";
import "../components/todayTable.js";

class HomepageComponent extends HTMLElement {
  constructor() {
    super();

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

    // Listens for qr detection
    window.addEventListener("qrDetected", this.handleQRScan);
  }

  // Cleanup when switching page
  disconnectedCallback() {
    console.log("Leaving homepage layout. Clearing animation frame loops.");

    window.removeEventListener("qrDetected", this.handleQRScan);
    console.log("Cleaned up camera loops and QR event listeners successfully.");
  }

  // HTML Code goes here
  layout() {
    return /*html*/ `
    <app-navbar></app-navbar>
    <main>
      <div class="left">
        <div class="logo-background-wrap">
          <img id="pshs-logo-bg" src="../assets/images/PSHS-ZRC LOGO-modified.png" alt="pshs-logo">
        </div>    

        <app-todaytable></app-todaytable>
      </div>

      <div class="right"> 
        <app-camerafeed></app-camerafeed>
        <app-clock></app-clock>
      </div>
    </main> `;
  }
}

// Custom Element Tag Name
customElements.define("app-homepage", HomepageComponent);

// Import components
import "../../components/navbar/navbar.js";
import "../../components/camerafeed/camerafeed.js";
import "../../components/clock/clock.js";
import "../../components/todayTable/todayTable.js";

class HomepageComponent extends HTMLElement {
  constructor() {
    super();

    // Bind listener to the class instance so it can be cleanly removed later
    this.handleQRScan = async (event) => {
      const qrCodeData = event.detail;
      console.log("QR caught by component logic:", qrCodeData);

      const response =
        await window.pywebview.api.processScannedCode(qrCodeData);

      if (response.status === "invalid") {
        console.error("Invalid QR Data"); // <-- UPGRADE: Instead, a window or dialog must pop up that tells that data is invalid
        return;
      }

      // If ID is valid but not yet registered
      if (response.status === "not_found") {
        alert("You are not registered yet. Please register first"); // <--- UPGRADE: Instead, a window must pop up.
        await window.router("registration", response);
        return;
      }

      // If ID is valid and registered, proceed with logging in/out
      if (response.status === "success") {
        if (response.action === "check_in") {
          console.log("Checking in"); // <--- UPGRADE
        } else {
          console.log("Checking Out");
        }

        const todayTable = this.querySelector("app-todaytable");
        if (todayTable && typeof todayTable.fetchAndRender === "function") {
          todayTable.fetchAndRender();
        } else {
          console.warn(
            "Could not find app-todaytable or fetchAndRender is not defined.",
          );
        }
      }
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

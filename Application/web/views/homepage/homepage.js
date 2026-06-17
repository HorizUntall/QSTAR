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

      try {
        const response =
          await window.pywebview.api.attendance.processScannedCode(qrCodeData);

        // 1. INVALID DATA UPGRADE: Custom Dialog
        if (response.status === "invalid") {
          this.showNotification(
            "Invalid Data",
            response.message || "The scanned QR code is invalid.",
            "error",
          );
          return;
        }

        // 2. NOT REGISTERED UPGRADE: Custom Dialog before routing
        if (response.status === "not_found") {
          this.showNotification(
            "Registration Required",
            "You are not registered yet. Redirecting to registration...",
            "warning",
          );

          // Small delay so the user can actually read the notification before the page switches
          setTimeout(async () => {
            await window.router("registration", response);
          }, 2000);
          return;
        }

        // 3. SUCCESS UPGRADE: Pastel Status Flashes
        if (response.status === "success") {
          if (response.action === "check_in") {
            this.showNotification(
              "Success",
              "Successfully Checked In!",
              "check-in",
            );
          } else {
            this.showNotification(
              "Success",
              "Successfully Checked Out!",
              "check-out",
            );
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
      } catch (err) {
        console.error("API Error:", err);
        this.showNotification(
          "Error",
          "Failed to communicate with the system.",
          "error",
        );
      }
    };
  }

  // Helper method to trigger custom popups and flash overlays
  showNotification(title, message, type) {
    const overlay = this.querySelector("#status-overlay");
    const modal = this.querySelector("#status-modal");
    const modalTitle = this.querySelector("#modal-title");
    const modalMessage = this.querySelector("#modal-message");

    if (!overlay || !modal) return;

    // Reset styles
    overlay.className = "status-overlay";
    modal.className = "status-modal";

    // Set text content safely
    modalTitle.textContent = title;
    modalMessage.textContent = message;

    // Apply type-specific styling
    if (type === "check-in" || type === "overwrite_checkout") {
      overlay.classList.add("flash-check-in");
      modal.classList.add("modal-success");
    } else if (type === "check-out") {
      overlay.classList.add("flash-check-out");
      modal.classList.add("modal-info");
    } else if (type === "error") {
      modal.classList.add("modal-error");
    } else if (type === "warning") {
      modal.classList.add("modal-warning");
    }

    // Show the elements
    overlay.classList.add("active");
    modal.classList.add("active");

    // Auto-hide after 2.5 seconds (except for warning which handles its own routing)
    if (type !== "warning") {
      setTimeout(() => {
        overlay.classList.remove("active");
        modal.classList.remove("active");
      }, 2500);
    }
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
    <main>
      <div id="status-overlay" class="status-overlay"></div>
      <div id="status-modal" class="status-modal">
        <h3 id="modal-title">Notice</h3>
        <p id="modal-message">Processing...</p>
      </div>

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

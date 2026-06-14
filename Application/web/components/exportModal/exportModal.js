class ExportModalComponent extends HTMLElement {
  constructor() {
    super();
    this.payload = null; // Will hold the filters and chart images
  }

  connectedCallback() {
    this.innerHTML = this.layout();

    this.setupEventListeners();
  }

  setupEventListeners() {
    const overlay = this.querySelector("#export-overlay");
    const radios = this.querySelectorAll('input[name="export-dest"]');
    const emailGroup = this.querySelector("#email-input-group");
    const confirmBtn = this.querySelector("#confirm-export-btn");
    const cancelBtn = this.querySelector("#cancel-export-btn");
    const statusMsg = this.querySelector("#export-status");

    // Toggle email input visibility
    radios.forEach((radio) => {
      radio.addEventListener("change", (e) => {
        if (e.target.value === "email") {
          emailGroup.classList.remove("hidden");
        } else {
          emailGroup.classList.add("hidden");
        }
      });
    });

    // Close modal
    cancelBtn.addEventListener("click", () => this.close());

    // Confirm Export
    confirmBtn.addEventListener("click", async () => {
      const dest = this.querySelector(
        'input[name="export-dest"]:checked',
      ).value;
      const email = this.querySelector("#target-email").value;

      if (dest === "email" && !email) {
        alert("Please enter a valid email address.");
        return;
      }

      // Update UI to show loading state
      confirmBtn.disabled = true;
      cancelBtn.disabled = true;
      statusMsg.textContent = "Generating files... please wait.";
      statusMsg.classList.remove("hidden", "success", "error");

      // Attach export config to the main payload
      const finalPayload = {
        ...this.payload,
        export_method: dest,
        target_email: dest === "email" ? email : null,
      };

      try {
        const response =
          await window.pywebview.api.trigger_data_export(finalPayload);

        if (response.status === "success") {
          statusMsg.textContent =
            dest === "local"
              ? "Files saved successfully!"
              : "Email sent successfully!";
          statusMsg.classList.add("success");
          setTimeout(() => this.close(), 2000); // Auto-close after 2 seconds
        } else {
          statusMsg.textContent = "Error: " + response.message;
          statusMsg.classList.add("error");
          confirmBtn.disabled = false;
          cancelBtn.disabled = false;
        }
      } catch (err) {
        console.error(err);
        statusMsg.textContent = "A system error occurred during export.";
        statusMsg.classList.add("error");
        confirmBtn.disabled = false;
        cancelBtn.disabled = false;
      }
    });
  }

  open(payload) {
    this.payload = payload;
    this.querySelector("#export-overlay").classList.remove("hidden");

    // Reset state
    this.querySelector("#confirm-export-btn").disabled = false;
    this.querySelector("#cancel-export-btn").disabled = false;
    this.querySelector("#export-status").classList.add("hidden");
    this.querySelector('input[value="local"]').checked = true;
    this.querySelector("#email-input-group").classList.add("hidden");
    this.querySelector("#target-email").value = "";
  }

  close() {
    this.querySelector("#export-overlay").classList.add("hidden");
  }

  layout() {
    return /*html*/ `
      <div class="modal-overlay hidden" id="export-overlay">
        <div class="modal-content">
          <h3>Export Dashboard Data</h3>
          <p class="modal-subtext">Choose how you want to receive your PDF summary and Excel data.</p>
          
          <div class="export-options">
            <label class="radio-label">
              <input type="radio" name="export-dest" value="local" checked>
              Download Files Locally
            </label>
            <label class="radio-label">
              <input type="radio" name="export-dest" value="email">
              Send to Email Address
            </label>
          </div>

          <div class="input-group hidden" id="email-input-group">
            <input type="email" id="target-email" placeholder="Enter recipient email address...">
          </div>

          <div id="export-status" class="status-message hidden">Processing...</div>

          <div class="modal-actions">
            <button id="cancel-export-btn" class="action-btn cancel">Cancel</button>
            <button id="confirm-export-btn" class="action-btn confirm">Generate Export</button>
          </div>
        </div>
      </div>
    `;
  }
}
customElements.define("app-export-modal", ExportModalComponent);

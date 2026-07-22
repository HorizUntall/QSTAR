class BugReportComponent extends HTMLElement {
  constructor() {
    super();

    this.handleOpen = () => this.toggleModal(true);
    this.handleClose = () => this.toggleModal(false);
    this.handleSubmit = async (e) => {
      e.preventDefault();
      const textarea = this.querySelector("#bug-details");
      const submitBtn = this.querySelector("#bug-submit-btn");
      const statusMsg = this.querySelector("#bug-status-msg");

      const details = textarea.value.trim();
      if (!details) {
        statusMsg.textContent = "Please enter some details before submitting.";
        statusMsg.className = "bug-status error";
        return;
      }

      // UI Loading State
      submitBtn.disabled = true;
      submitBtn.textContent = "Sending...";
      statusMsg.textContent = "";

      try {
        // Call your pywebview API bridge
        await window.pywebview.api.bug_report.report_bug(details);

        statusMsg.textContent = "Bug report submitted! Thank you.";
        statusMsg.className = "bug-status success";
        textarea.value = "";

        // Auto-close modal after 2 seconds
        setTimeout(() => {
          this.toggleModal(false);
          statusMsg.textContent = "";
          submitBtn.disabled = false;
          submitBtn.textContent = "Submit Report";
        }, 2000);
      } catch (err) {
        console.error("Failed to send bug report:", err);
        statusMsg.textContent = "Failed to send report. Please try again.";
        statusMsg.className = "bug-status error";
        submitBtn.disabled = false;
        submitBtn.textContent = "Submit Report";
      }
    };
  }

  toggleModal(show) {
    const modal = this.querySelector("#bug-modal-overlay");
    if (show) {
      modal.classList.add("active");
    } else {
      modal.classList.remove("active");
    }
  }

  connectedCallback() {
    this.innerHTML = this.layout();

    this.querySelector("#open-bug-btn").addEventListener(
      "click",
      this.handleOpen,
    );
    this.querySelector("#close-bug-btn").addEventListener(
      "click",
      this.handleClose,
    );
    this.querySelector("#bug-form").addEventListener(
      "submit",
      this.handleSubmit,
    );
  }

  disconnectedCallback() {
    const openBtn = this.querySelector("#open-bug-btn");
    const closeBtn = this.querySelector("#close-bug-btn");
    const form = this.querySelector("#bug-form");

    if (openBtn) openBtn.removeEventListener("click", this.handleOpen);
    if (closeBtn) closeBtn.removeEventListener("click", this.handleClose);
    if (form) form.removeEventListener("submit", this.handleSubmit);
  }

  layout() {
    return /*html*/ `
      <div class="bug-report-trigger">
        <p>Found a bug or issue? <button id="open-bug-btn" class="link-btn">Report here</button></p>
      </div>

      <!-- Modal Overlay -->
      <div id="bug-modal-overlay" class="bug-modal-overlay">
        <div class="bug-modal-card">
          <div class="bug-modal-header">
            <h3>Report a Bug</h3>
            <button id="close-bug-btn" class="close-btn">&times;</button>
          </div>
          
          <form id="bug-form">
            <p class="bug-instructions">
              Please describe what went wrong or how to reproduce the issue.
            </p>
            
            <!-- Plain-text multi-line input -->
            <textarea 
              id="bug-details" 
              rows="5" 
              placeholder="Describe the issue here..."
              required
            ></textarea>

            <div id="bug-status-msg" class="bug-status"></div>

            <div class="bug-modal-actions">
              <button type="submit" id="bug-submit-btn" class="submit-btn">Submit Report</button>
            </div>
          </form>
        </div>
      </div>
    `;
  }
}

customElements.define("app-bugreport", BugReportComponent);

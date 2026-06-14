class LoginComponent extends HTMLElement {
  constructor() {
    super();
    this.attempts = 0;
    this.maxAttempts = 3;
  }

  connectedCallback() {
    this.innerHTML = this.layout();
    this.setupEventListeners();

    // Globally hide the navbar while on this full-screen gate page
    const globalNavbar = document.querySelector("app-navbar");
    if (globalNavbar) globalNavbar.style.display = "none";
  }

  disconnectedCallback() {
    // Restore the navbar layout when leaving this page
    const globalNavbar = document.querySelector("app-navbar");
    if (globalNavbar) globalNavbar.style.display = "";
  }

  setupEventListeners() {
    // Return / Close 'X' Button
    const returnBtn = this.querySelector("#returnBtn");
    returnBtn.addEventListener("click", async () => {
      await window.router("homepage");
    });

    // PASSWORD VISIBILITY IMAGE TOGGLE LOGIC
    const togglePassword = this.querySelector("#togglePassword");
    const passwordInput = this.querySelector("#password");

    togglePassword.addEventListener("click", () => {
      const isPassword = passwordInput.getAttribute("type") === "password";

      if (isPassword) {
        passwordInput.setAttribute("type", "text");
        togglePassword.src = "../../assets/images/blind.png"; // Switch to closed eye asset
      } else {
        passwordInput.setAttribute("type", "password");
        togglePassword.src = "../../assets/images/view.png"; // Switch back to open eye asset
      }
    });

    // Form Processing
    const form = this.querySelector("#login-form");
    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      this.attemptLogin(passwordInput.value);
    });
  }

  async attemptLogin(password) {
    const errorMsgElement = this.querySelector("#error-message");
    errorMsgElement.classList.remove("visible"); // Reset error text state

    try {
      const response = await window.pywebview.api.loginAdmin(password);

      if (response.status === "success") {
        await window.router("dashboard");
      } else {
        this.handleFailure(response.message || "Invalid password.");
      }
    } catch (err) {
      // Fallback local mock simulation in case backend isn't linked up yet
      this.handleFailure("Invalid password.");
    }
  }

  handleFailure(message) {
    this.attempts++;
    const errorMsgElement = this.querySelector("#error-message");
    const remaining = this.maxAttempts - this.attempts;

    if (this.attempts >= this.maxAttempts) {
      alert("Too many failed attempts! Returning to home.");
      window.router("homepage");
    } else {
      errorMsgElement.innerText = `${message} (${remaining} attempts remaining)`;
      errorMsgElement.classList.add("visible");

      // Clear password input field box for convenience
      this.querySelector("#password").value = "";
    }
  }

  layout() {
    return /*html*/ `
    <div class="login-wrapper">
      <div class="verification-card">
        <button id="returnBtn" class="close-btn" title="Cancel">&times;</button>
        
        <header class="card-header">
          <h1>Data Dashboard</h1>
          <h2>Verification</h2>
        </header>

        <form id="login-form">
          <div class="input-container">
            <input type="password" id="password" placeholder="Password" required autocomplete="off">
            <img id="togglePassword" class="eye-icon" src="../../assets/images/view.png" alt="Toggle Visibility">
          </div>
          
          <div id="error-message" class="error-text"></div>

          <button type="submit" class="submit-btn">Submit</button>
        </form>
      </div>
    </div>
    `;
  }
}

customElements.define("app-login", LoginComponent);

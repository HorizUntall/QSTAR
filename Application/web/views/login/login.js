import "../../components/navbar/navbar.js";

class LoginComponent extends HTMLElement {
  connectedCallback() {
    this.innerHTML = this.layout();

    const returnBtn = document.getElementById("returnBtn");
    returnBtn.addEventListener("click", async () => {
      await window.router("homepage");
    });

    const form = document.getElementById("login-form");
    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      const pw = document.getElementById("password");
      this.attemptLogin(pw.value);
    });
  }

  async attemptLogin(password) {
    const response = await window.pywebview.api.loginAdmin(password);
    if (response.status === "success") {
      console.log(response.message);
      await window.router("dashboard");
    } else {
      console.log(response.message);
    }
  }

  layout() {
    return /*html*/ `
    <main>
        <h1>Hello World</h1>
        <button id="returnBtn">Return</button>
        <form id="login-form" action="submit">
            <label for="password">Enter password</label>
            <input type="password" id="password" required>
            <button type="submit">Login</button>
        </form>
    </main>
    
    `;
  }
}

// Custom Element Tag Name
customElements.define("app-login", LoginComponent);

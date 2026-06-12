import "../../../components/navbar/navbar.js";

class SettingsViewComponent extends HTMLElement {
  connectedCallback() {
    this.innerHTML = this.layout();

    const testBtn = document.getElementById("testBtn");
    testBtn.addEventListener("click", async () => {
      await window.router("dashboard");
    });
  }

  layout() {
    return /*html*/ `
    <app-navbar></app-navbar>
    <main>
        <h2>This is settings page</h2>
        <!-- Test -->
        <button id="testBtn">Switch page</button>
    </main>
    `;
  }
}

customElements.define("app-settings", SettingsViewComponent);

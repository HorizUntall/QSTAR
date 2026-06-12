import "../../../components/navbar/navbar.js";

class DashboardViewComponent extends HTMLElement {
  connectedCallback() {
    this.innerHTML = this.layout();
    const testBtn = document.getElementById("testBtn");

    testBtn.addEventListener("click", async () => {
      await window.router("settings");
    });
  }

  layout() {
    return /*html*/ `
    <app-navbar></app-navbar>
    <main>
        <h2>Dashboard</h2>
        <!-- Test -->
         <button id="testBtn">Go to settings</button>
    </main>
    `;
  }
}

customElements.define("app-dashboard", DashboardViewComponent);

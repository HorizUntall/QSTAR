import "../../components/navbar/navbar.js";

class AboutViewComponent extends HTMLElement {
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
            <h2>This is about page</h2>
            <!-- Test -->
             <button id="testBtn">Switch page</button>
        </main>
        `;
  }
}

customElements.define("app-about", AboutViewComponent);

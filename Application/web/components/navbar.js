class NavbarComponent extends HTMLElement {
  connectedCallback() {
    this.innerHTML = this.layout();
  }

  layout() {
    return /*html*/ `
        <nav>
        <div class="nav-left">
          <h1>Q-STAR</h1>
          <h2>QR-Based Attendance</h2>
        </div>
      </nav>
        `;
  }
}

customElements.define("app-navbar", NavbarComponent);

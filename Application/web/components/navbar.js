class NavbarComponent extends HTMLElement {
  connectedCallback() {
    this.innerHTML = this.layout();
  }

  layout() {
    return /*html*/ `

        <nav>
        <div class="nav-left">
          <h1>Q-STAR</h1>
          <h2>QR-Based Student and Teacher Attendance Recorder</h2>
        </div>

        <div class="nav-right">
          <ul>
            <li><a href="#">Home</a></li>
            <li><a href="#">Data Dashboard</a></li>
            <li><a href="#">About</a></li>
          </ul>
        </div>
      </nav>
        `;
  }
}

customElements.define("app-navbar", NavbarComponent);

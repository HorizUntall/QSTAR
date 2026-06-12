class NavbarComponent extends HTMLElement {
  connectedCallback() {
    this.innerHTML = this.layout();

    const homeLink = document.getElementById("homeLink");
    homeLink.addEventListener("click", async (e) => {
      e.preventDefault();
      await window.router("homepage");
    });

    const dashboardLink = document.getElementById("dashboardLink");
    dashboardLink.addEventListener("click", async (e) => {
      e.preventDefault();
      await window.router("login");
    });

    const aboutLink = document.getElementById("aboutLink");
    aboutLink.addEventListener("click", async (e) => {
      e.preventDefault();
      await window.router("about");
    });
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
            <li><a href="#" id="homeLink">Home</a></li>
            <li><a href="#" id="dashboardLink">Data Dashboard</a></li>
            <li><a href="#" id="aboutLink">About</a></li>
          </ul>
        </div>
      </nav>
        `;
  }
}

customElements.define("app-navbar", NavbarComponent);

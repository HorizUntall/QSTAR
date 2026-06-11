// Import components
import "../components/navbar.js";

class HomepageComponent extends HTMLElement {
  constructor() {
    super();
    this.cameraAnimationId = null;
    this.timeInterval = null;

    // Bind listener to the class instance so it can be cleanly removed later
    this.handleQRScan = async (event) => {
      const qrCodeData = event.detail;
      console.log("QR caught by component logic:", qrCodeData);

      const response =
        await window.pywebview.api.processScannedCode(qrCodeData);
    };
  }

  // Runs instantly when opening this page
  connectedCallback() {
    this.innerHTML = this.layout();
    console.log("Homepage layout attached natively. Starting stream...");
    this.streamCamera();

    // For date and time
    this.startLiveClock();

    // Scroll down
    this.scrollToBottom();

    // Listens for qr detection
    window.addEventListener("qrDetected", this.handleQRScan);
  }

  // Cleanup when switching page
  disconnectedCallback() {
    console.log("Leaving homepage layout. Clearing animation frame loops.");
    if (this.cameraAnimationId) {
      cancelAnimationFrame(this.cameraAnimationId);
    }

    window.removeEventListener("qrDetected", this.handleQRScan);
    console.log("Cleaned up camera loops and QR event listeners successfully.");
  }

  streamCamera() {
    window.pywebview.api.scanner
      .fetch_frame()
      .then((frameData) => {
        const feedImg = document.getElementById("cameraFeed");
        if (feedImg && frameData) {
          feedImg.src = frameData;
          this.cameraAnimationId = requestAnimationFrame(() =>
            this.streamCamera(),
          );
        }
      })
      .catch((err) => console.log("Stream stopped or interrupted"));
  }

  startLiveClock() {
    const timeEl = this.querySelector("#live-time");
    const dateEl = this.querySelector("#live-date");

    const updateClock = () => {
      const now = new Date();

      // Format Time: "12:11 PM"
      let hours = now.getHours();
      const minutes = String(now.getMinutes()).padStart(2, "0");
      const ampm = hours >= 12 ? "PM" : "AM";
      hours = hours % 12 || 12; // convert 0 to 12

      // Format Date: "Jun. 11, 2026 Thursday"
      const months = [
        "Jan.",
        "Feb.",
        "Mar.",
        "Apr.",
        "May",
        "Jun.",
        "Jul.",
        "Aug.",
        "Sep.",
        "Oct.",
        "Nov.",
        "Dec.",
      ];
      const days = [
        "Sunday",
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
      ];

      if (timeEl) timeEl.textContent = `${hours}:${minutes} ${ampm}`;
      if (dateEl)
        dateEl.textContent = `${months[now.getMonth()]} ${now.getDate()}, ${now.getFullYear()} ${days[now.getDay()]}`;
    };

    updateClock(); // Run instantly on load
    this.timerInterval = setInterval(updateClock, 1000);
  }

  scrollToBottom() {
    const container = this.querySelector(".table-container");
    if (container) {
      container.scrollTo({
        top: container.scrollHeight,
        behavior: "smooth",
      });
    }
  }

  // HTML Code goes here
  layout() {
    return /*html*/ `
    <app-navbar></app-navbar>
    <main>
      <div class="left">
        <div class="logo-background-wrap">
          <img id="pshs-logo-bg" src="../assets/images/PSHS-ZRC LOGO-modified.png" alt="pshs-logo">
        </div>

        <div class="table-container">
          <table class="attendance-table">
            <thead>
              <tr>
                <th class="no-col">No.</th>
                <th class="name-col">Name</th>
                <th class="time-col">Time-In</th>
                <th class="time-col">Time-Out</th>
              </tr>
            </thead>
            <tbody>
              <tr><td>1</td><td>John Doe</td><td>07:45 AM</td><td>--:--</td></tr>
              <tr><td>2</td><td>Jane Smith</td><td>07:52 AM</td><td>12:05 PM</td></tr>
              <tr><td>3</td><td>Alex Rivera</td><td>08:02 AM</td><td>--:--</td></tr>
              <tr><td>4</td><td>John Doe</td><td>07:45 AM</td><td>--:--</td></tr>
              <tr><td>5</td><td>Jane Smith</td><td>07:52 AM</td><td>12:05 PM</td></tr>
              <tr><td>6</td><td>Alex Rivera</td><td>08:02 AM</td><td>--:--</td></tr>
              <tr><td>7</td><td>John Doe</td><td>07:45 AM</td><td>--:--</td></tr>
              <tr><td>8</td><td>Jane Smith</td><td>07:52 AM</td><td>12:05 PM</td></tr>
              <tr><td>9</td><td>Alex Rivera</td><td>08:02 AM</td><td>--:--</td></tr>
              <tr><td>10</td><td>John Doe</td><td>07:45 AM</td><td>--:--</td></tr>
              <tr><td>11</td><td>Jane Smith</td><td>07:52 AM</td><td>12:05 PM</td></tr>
              <tr><td>12</td><td>Alex Rivera</td><td>08:02 AM</td><td>--:--</td></tr>
              <tr><td>12</td><td>Alex Rivera</td><td>08:02 AM</td><td>--:--</td></tr>
              <tr><td>12</td><td>Alex Rivera</td><td>08:02 AM</td><td>--:--</td></tr>
              <tr><td>12</td><td>Alex Rivera</td><td>08:02 AM</td><td>--:--</td></tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="right">
        <div class="camera-container">
          <img id="cameraFeed" src="" alt="camera" /> 
        </div>
        
        <div class="clock-container">
          <h1 id="live-time" class="time-display">--:-- --</h1>
          <p id="live-date" class="date-display">--------</p>
        </div>
      </div>
    </main> `;
  }
}

// Custom Element Tag Name
customElements.define("app-homepage", HomepageComponent);

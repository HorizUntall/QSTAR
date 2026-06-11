class ClockComponent extends HTMLElement {
  connectedCallback() {
    this.innerHTML = this.layout();

    // For date and time
    this.startLiveClock();
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

  layout() {
    return /*html*/ `
         <div class="clock-container">
          <h1 id="live-time" class="time-display">--:-- --</h1>
          <p id="live-date" class="date-display">--------</p>
        </div>
    
    `;
  }
}

// Custom Element Tag Name
customElements.define("app-clock", ClockComponent);

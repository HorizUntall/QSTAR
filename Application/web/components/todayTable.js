class TodayTableComponent extends HTMLElement {
  async connectedCallback() {
    this.innerHTML = this.layout();

    try {
      if (!window.pywebview || !window.pywebview.api) {
        await new Promise((resolve) =>
          window.addEventListener("pywebviewready", resolve),
        );
      }

      const data = await window.pywebview.api.get_today_attendance();
      this.renderRows(data);
    } catch (error) {
      console.error("Failed to load today's attendance:", error);
      this.querySelector("tbody").innerHTML =
        `<tr><td colspan="4" style="text-align:center; color:red;">Error loading data</td></tr>`;
    }
  }

  renderRows(data) {
    const tbody = this.querySelector("tbody");
    if (!tbody) return;

    if (data.length === 0) {
      tbody.innerHTML = `<tr><td colspan="4" style="text-align:center;">No attendance records for today yet.</td></tr>`;
      return;
    }

    // Helper to format "YYYY-MM-DD HH:MM:SS" string to "H:MM PM/AM"
    const formatTime = (dateTimeString) => {
      if (!dateTimeString) return null;

      const timePart = dateTimeString.split(" ")[1];
      if (!timePart) return dateTimeString;

      const [hoursStr, minutesStr] = timePart.split(":");
      let hours = parseInt(hoursStr, 10);
      const minutes = minutesStr;

      const ampm = hours >= 12 ? "PM" : "AM";
      hours = hours % 12;
      hours = hours ? hours : 12; // convert '0' to '12'

      return `${hours}:${minutes} ${ampm}`;
    };

    tbody.innerHTML = data
      .map((row, index) => {
        // Format time strings cleanly
        const formattedIn = formatTime(row.time_in);
        const formattedOut = formatTime(row.time_out);

        const timeOutDisplay = formattedOut
          ? formattedOut
          : '<span class="status-active">Active</span>';

        return /*html*/ `
        <tr>
          <td class="no-col">${index + 1}</td>
          <td class="name-col">${row.first_name} ${row.last_name}</td>
          <td class="time-col">${formattedIn}</td>
          <td class="time-col">${timeOutDisplay}</td>
        </tr>
      `;
      })
      .join("");

    this.scrollToBottom();
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

  layout() {
    return /*html*/ `
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
              <tr><td colspan="4" style="text-align:center; color:gray;">Loading today's records...</td></tr>
            </tbody>
          </table>
        </div>
        `;
  }
}

// Custom Element Tag Name
customElements.define("app-todaytable", TodayTableComponent);

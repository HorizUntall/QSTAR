class TodayTableComponent extends HTMLElement {
  connectedCallback() {
    this.innerHTML = this.layout();

    // Scroll down
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
        `;
  }
}

// Custom Element Tag Name
customElements.define("app-todaytable", TodayTableComponent);

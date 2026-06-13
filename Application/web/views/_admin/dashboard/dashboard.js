import "../../../components/navbar/navbar.js";

class DashboardViewComponent extends HTMLElement {
  constructor() {
    super();
    this.currentTab = "summary"; // 'summary', 'history', 'registered'

    // Store chart instances so we can destroy them before re-rendering
    // to prevent memory leaks and canvas errors
    this.chartInstances = {
      visits: null,
      topGoers: null,
      batch: null,
    };
  }

  connectedCallback() {
    this.innerHTML = this.layout();
    this.setupEventListeners();

    // Fetch initial data for the default tab when component loads
    this.fetchData();
  }

  setupEventListeners() {
    // Tab Switching Logic
    const tabs = this.querySelectorAll(".tab-btn");
    tabs.forEach((tab) => {
      tab.addEventListener("click", (e) => {
        // Update active styling
        tabs.forEach((t) => t.classList.remove("active"));
        e.target.classList.add("active");

        // Hide all views, show the selected one
        this.querySelectorAll(".view-section").forEach((view) =>
          view.classList.add("hidden"),
        );
        this.currentTab = e.target.dataset.tab;
        this.querySelector(`#${this.currentTab}-view`).classList.remove(
          "hidden",
        );

        // Automatically fetch data for the new tab
        this.fetchData();
      });
    });

    // Go Button Logic (Centralized Fetch)
    const goBtn = this.querySelector("#go-btn");
    goBtn.addEventListener("click", () => this.fetchData());

    // Settings Button (Placeholder based on your initial code)
    const settingsBtn = this.querySelector("#settingsBtn");
    settingsBtn.addEventListener("click", async () => {
      if (window.router) await window.router("settings");
    });

    // Export Button (Placeholder)
    const exportBtn = this.querySelector("#export-btn");
    exportBtn.addEventListener("click", () => {
      console.log("Export button clicked - functionality to be added");
    });
  }

  getFormData() {
    // Extracts all current values from the input fields
    return {
      filters: {
        start_date: this.querySelector("#start-date").value,
        end_date: this.querySelector("#end-date").value,
        search_name: this.querySelector("#search-name").value,
        batch: this.querySelector("#batch").value,
        sex: this.querySelector("#sex").value || null,
      },
      topUsersLimit: this.querySelector("#topUsersLimit").value,
      num_batches: this.querySelector("#num_batches").value,
      page: this.querySelector("#page").value,
      page_size: this.querySelector("#page_size").value,
    };
  }

  async fetchData() {
    const form_data = this.getFormData();
    console.log(`Fetching data for ${this.currentTab}...`, form_data);

    try {
      if (this.currentTab === "summary") {
        const response =
          await window.pywebview.api.get_dashboard_data(form_data);
        if (response.status === "success") {
          this.renderSummary(response.data);
        } else console.error("Error fetching summary data");
      } else if (this.currentTab === "history") {
        const response =
          await window.pywebview.api.get_attendance_history(form_data);
        if (response.status === "success") {
          // Note: response.data.data accesses the array inside the pagination object
          this.renderTable("history-table-body", response.data.data, [
            "user_id",
            "first_name",
            "last_name",
            "batch",
            "user_type",
            "time_in",
            "time_out",
          ]);
        } else console.error("Error fetching history data");
      } else if (this.currentTab === "registered") {
        const response =
          await window.pywebview.api.get_registered_users(form_data);
        if (response.status === "success") {
          this.renderTable("registered-table-body", response.data.data, [
            "id",
            "first_name",
            "last_name",
            "batch",
            "sex",
          ]);
        } else console.error("Error fetching registered data");
      }
    } catch (error) {
      console.error("API call failed:", error);
    }
  }

  renderSummary(data) {
    // 1. Update KPIs
    if (data.kpis) {
      this.querySelector("#kpi-time").textContent =
        `${data.kpis.avg_time_spent_minutes.toFixed(2)} mins`;
      this.querySelector("#kpi-visits-day").textContent =
        data.kpis.avg_visits_per_day;
      this.querySelector("#kpi-total").textContent = data.kpis.total_visits;
    }

    // 2. Update Gender Text
    if (data.gender) {
      this.querySelector("#female-pct").textContent =
        `${data.gender.female_pct}%`;
      this.querySelector("#male-pct").textContent = `${data.gender.male_pct}%`;
      this.querySelector("#gender-subtext").textContent =
        `of the ${data.gender.total_visits} visits in the library recorded.`;
    }

    // 3. Render Charts
    if (data.visits_vs_time) this.renderVisitsChart(data.visits_vs_time);
    if (data.top_goers) this.renderTopGoersChart(data.top_goers);
    if (data.batch_visits) this.renderBatchChart(data.batch_visits);
  }

  renderVisitsChart(chartData) {
    const ctx = this.querySelector("#visitsChart").getContext("2d");

    if (this.chartInstances.visits) {
      this.chartInstances.visits.destroy();
    }

    const labels = chartData.map((item) => item.visit_date);
    const dataPoints = chartData.map((item) => item.frequency);

    this.chartInstances.visits = new Chart(ctx, {
      type: "line",
      data: {
        labels: labels,
        datasets: [
          {
            label: "Number of Visits",
            data: dataPoints,
            borderColor: "#FF6B81",
            backgroundColor: "rgba(255, 107, 129, 0.2)",
            borderWidth: 2,
            tension: 0.3,
            fill: true,
          },
        ],
      },
      options: { responsive: true, maintainAspectRatio: false },
    });
  }

  renderTopGoersChart(chartData) {
    const ctx = this.querySelector("#topGoersChart").getContext("2d");

    if (this.chartInstances.topGoers) {
      this.chartInstances.topGoers.destroy();
    }

    const labels = chartData.map(
      (item) => `${item.first_name} ${item.last_name}`,
    );
    const dataPoints = chartData.map((item) => item.total_visits);

    this.chartInstances.topGoers = new Chart(ctx, {
      type: "bar",
      data: {
        labels: labels,
        datasets: [
          {
            label: "Total Visits",
            data: dataPoints,
            backgroundColor: "#FF6B81",
          },
        ],
      },
      options: { responsive: true, maintainAspectRatio: false },
    });
  }

  renderBatchChart(chartData) {
    const ctx = this.querySelector("#batchChart").getContext("2d");

    if (this.chartInstances.batch) {
      this.chartInstances.batch.destroy();
    }

    const labels = chartData.map((item) => item.batch);
    const dataPoints = chartData.map((item) => item.frequency);

    this.chartInstances.batch = new Chart(ctx, {
      type: "bar",
      data: {
        labels: labels,
        datasets: [
          {
            label: "Visits per Batch",
            data: dataPoints,
            backgroundColor: "#FF6B81",
          },
        ],
      },
      options: { responsive: true, maintainAspectRatio: false },
    });
  }

  renderTable(tbodyId, dataArray, columns) {
    const tbody = this.querySelector(`#${tbodyId}`);
    tbody.innerHTML = ""; // Clear existing table data

    if (!dataArray || dataArray.length === 0) {
      tbody.innerHTML = `<tr><td colspan="${columns.length + 1}">No records found</td></tr>`;
      return;
    }

    dataArray.forEach((row, index) => {
      const tr = document.createElement("tr");

      // Calculate row number based on pagination (assuming page starts at 1)
      const page = parseInt(this.querySelector("#page").value) || 1;
      const pageSize = parseInt(this.querySelector("#page_size").value) || 100;
      const rowNum = (page - 1) * pageSize + index + 1;

      tr.innerHTML =
        `<td>${rowNum}</td>` +
        columns.map((col) => `<td>${row[col] || ""}</td>`).join("");
      tbody.appendChild(tr);
    });
  }

  layout() {
    return /*html*/ `
    <app-navbar></app-navbar>
    <main class="dashboard-container">
      
      <div class="tabs-header">
        <button class="tab-btn active" data-tab="summary">Data Summary</button>
        <button class="tab-btn" data-tab="history">Attendance History</button>
        <button class="tab-btn" data-tab="registered">Registered</button>
        <div class="spacer"></div>
        <button class="icon-btn" id="settingsBtn" title="Settings">⚙️</button>
      </div>

      <div class="filters-row">
        <div class="filter-group">
          <span>Filter Options:</span>
          <label><input type="radio" name="time-filter" value="today" checked> Today</label>
          <label><input type="radio" name="time-filter" value="custom"> Custom Time Range</label>
          <input type="date" id="start-date">
          <span>-</span>
          <input type="date" id="end-date">
        </div>
        <div class="filter-group">
          <input type="text" id="search-name" placeholder="Name">
          <select id="sex">
            <option value="">Sex</option>
            <option value="M">Male</option>
            <option value="F">Female</option>
          </select>
          <input type="text" id="batch" placeholder="Batch">
        </div>
        <button id="go-btn" class="action-btn">Go!</button>
        <button id="export-btn" class="action-btn export">Export Data</button>
      </div>

      <div class="advanced-filters">
          <label>Page: <input type="number" id="page" value="1" min="1"></label>
          <label>Per Page: <input type="number" id="page_size" value="100"></label>
          <label>Top Users Limit: <input type="number" id="topUsersLimit" value="5"></label>
          <label>Batch Limit: <input type="number" id="num_batches" value="6"></label>
      </div>

      <div class="view-container">
        
        <div id="summary-view" class="view-section">
          <div class="dashboard-grid">
            <div class="card graph-card main-graph">
              <h3>Library Visits vs Time</h3>
              <div style="position: relative; height: 300px; width: 100%;">
                <canvas id="visitsChart"></canvas>
              </div>
            </div>
            <div class="card graph-card top-goers">
              <h3>Top Library Goers</h3>
              <div style="position: relative; height: 250px; width: 100%;">
                <canvas id="topGoersChart"></canvas>
              </div>
            </div>
            <div class="card graph-card batch-visits">
              <h3>Library Visits per Batch</h3>
              <div style="position: relative; height: 250px; width: 100%;">
                <canvas id="batchChart"></canvas>
              </div>
            </div>
            <div class="card info-card gender-dev">
              <h3>Gender and Development</h3>
              <div class="gender-stats">
                <div class="stat"><span id="female-pct" class="female">0%</span> Female</div>
                <div class="stat"><span id="male-pct" class="male">0%</span> Male</div>
              </div>
              <p id="gender-subtext" class="subtext">of the visits in the library recorded.</p>
            </div>
            <div class="card info-card kpis">
              <h3>Others</h3>
              <div class="kpi-row">
                <div class="kpi-item"><h2 id="kpi-time">0 hrs</h2><p>Average time spent in the library</p></div>
                <div class="kpi-item"><h2 id="kpi-visits-day">0</h2><p>Average number of visits per day</p></div>
                <div class="kpi-item"><h2 id="kpi-total">0</h2><p>Total number of visits</p></div>
              </div>
            </div>
          </div>
        </div>

        <div id="history-view" class="view-section hidden">
          <table class="data-table">
            <thead>
              <tr>
                <th>No.</th><th>ID No.</th><th>First Name</th><th>Last Name</th>
                <th>Batch</th><th>User Type</th><th>Time-In</th><th>Time-Out</th>
              </tr>
            </thead>
            <tbody id="history-table-body"></tbody>
          </table>
        </div>

        <div id="registered-view" class="view-section hidden">
          <table class="data-table">
            <thead>
              <tr>
                <th>No.</th><th>ID No.</th><th>First Name</th><th>Last Name</th><th>Batch</th><th>Sex</th>
              </tr>
            </thead>
            <tbody id="registered-table-body"></tbody>
          </table>
        </div>

      </div>
    </main>
    `;
  }
}

customElements.define("app-dashboard", DashboardViewComponent);

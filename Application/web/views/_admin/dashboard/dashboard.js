import "../../../components/navbar/navbar.js";
import "../../../components/dashboardSummary/dashboardSummary.js";
import "../../../components/dashboardTable/dashboardTable.js";

class DashboardViewComponent extends HTMLElement {
  constructor() {
    super();
    this.currentTab = "summary";
  }

  connectedCallback() {
    this.innerHTML = this.layout();
    this.setupEventListeners();
    this.fetchData();
  }

  setupEventListeners() {
    const tabs = this.querySelectorAll(".tab-btn");
    tabs.forEach((tab) => {
      tab.addEventListener("click", (e) => {
        tabs.forEach((t) => t.classList.remove("active"));
        e.target.classList.add("active");

        this.querySelectorAll(".view-section").forEach((view) =>
          view.classList.add("hidden"),
        );
        this.currentTab = e.target.dataset.tab;
        this.querySelector(`#${this.currentTab}-view`).classList.remove(
          "hidden",
        );

        this.fetchData();
      });
    });

    this.querySelector("#go-btn").addEventListener("click", () => {
      const tableComp = this.querySelector(
        `${this.currentTab === "history" ? "#history-table" : "#registered-table"}`,
      );
      if (tableComp) tableComp.page = 1;
      this.fetchData();
    });

    this.addEventListener("config-change", () => this.fetchData());
    this.addEventListener("page-change", () => this.fetchData());

    this.querySelector("#settingsBtn").addEventListener("click", async () => {
      if (window.router) await window.router("settings");
    });
  }

  getPayload() {
    const summaryComp = this.querySelector("dashboard-summary");
    const historyComp = this.querySelector("#history-table");
    const registeredComp = this.querySelector("#registered-table");

    const tuning = summaryComp
      ? summaryComp.getTuningValues()
      : { topUsersLimit: 5, num_batches: 6 };
    const activeTable =
      this.currentTab === "history" ? historyComp : registeredComp;

    return {
      filters: {
        start_date: this.querySelector("#start-date").value,
        end_date: this.querySelector("#end-date").value,
        search_name: this.querySelector("#search-name").value,
        batch: this.querySelector("#batch").value,
        sex: this.querySelector("#sex").value || null,
      },
      topUsersLimit: tuning.topUsersLimit,
      num_batches: tuning.num_batches,
      page: activeTable ? activeTable.page : 1,
      page_size: activeTable ? activeTable.limit : 100,
    };
  }

  async fetchData() {
    const payload = this.getPayload();
    console.log(
      `Fetching parameters for unified tab scope [${this.currentTab}]:`,
      payload,
    );

    try {
      if (this.currentTab === "summary") {
        const res = await window.pywebview.api.get_dashboard_data(payload);
        if (res.status === "success")
          this.querySelector("dashboard-summary").updateData(res.data);
      } else if (this.currentTab === "history") {
        const res = await window.pywebview.api.get_attendance_history(payload);
        if (res.status === "success") {
          this.querySelector("#history-table").updateTable(
            res.data.data,
            res.data.pagination.total_pages,
          );
        }
      } else if (this.currentTab === "registered") {
        const res = await window.pywebview.api.get_registered_users(payload);
        if (res.status === "success") {
          this.querySelector("#registered-table").updateTable(
            res.data.data,
            res.data.pagination.total_pages,
          );
        }
      }
    } catch (err) {
      console.error("Local pywebview bridge execution failed:", err);
    }
  }

  layout() {
    return /*html*/ `
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

      <div class="view-container">
        <div id="summary-view" class="view-section">
          <dashboard-summary></dashboard-summary>
        </div>

        <div id="history-view" class="view-section hidden">
          <dashboard-table id="history-table" 
            headers='["ID No.", "First Name", "Last Name", "Batch", "User Type", "Time-In", "Time-Out"]'
            columns='["user_id", "first_name", "last_name", "batch", "user_type", "time_in", "time_out"]'>
          </dashboard-table>
        </div>

        <div id="registered-view" class="view-section hidden">
          <dashboard-table id="registered-table" 
            headers='["ID No.", "First Name", "Last Name", "Batch", "Sex"]'
            columns='["id", "first_name", "last_name", "batch", "sex"]'>
          </dashboard-table>
        </div>
      </div>
    </main>
    `;
  }
}
customElements.define("app-dashboard", DashboardViewComponent);

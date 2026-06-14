class DashboardSummaryComponent extends HTMLElement {
  constructor() {
    super();
    this.chartInstances = { visits: null, topGoers: null, batch: null };
  }

  connectedCallback() {
    this.innerHTML = this.layout();

    this.querySelector("#topUsersLimit").addEventListener("change", () =>
      this.dispatchConfigChange(),
    );
    this.querySelector("#num_batches").addEventListener("change", () =>
      this.dispatchConfigChange(),
    );
  }

  getTuningValues() {
    return {
      topUsersLimit: this.querySelector("#topUsersLimit").value || 5,
      num_batches: this.querySelector("#num_batches").value || 6,
    };
  }

  dispatchConfigChange() {
    this.dispatchEvent(new CustomEvent("config-change", { bubbles: true }));
  }

  updateData(data) {
    if (data.kpis) {
      this.querySelector("#kpi-time").textContent =
        `${data.kpis.avg_time_spent_minutes.toFixed(2)} mins`;
      this.querySelector("#kpi-visits-day").textContent =
        data.kpis.avg_visits_per_day;
      this.querySelector("#kpi-total").textContent = data.kpis.total_visits;
    }

    if (data.gender) {
      this.querySelector("#female-pct").textContent =
        `${data.gender.female_pct}%`;
      this.querySelector("#male-pct").textContent = `${data.gender.male_pct}%`;
      this.querySelector("#gender-subtext").textContent =
        `of the ${data.gender.total_visits} visits in the library recorded.`;
    }

    if (data.visits_vs_time) this.renderVisitsChart(data.visits_vs_time);
    if (data.top_goers) this.renderTopGoersChart(data.top_goers);
    if (data.batch_visits) this.renderBatchChart(data.batch_visits);
  }

  renderVisitsChart(chartData) {
    const ctx = this.querySelector("#visitsChart").getContext("2d");
    if (this.chartInstances.visits) this.chartInstances.visits.destroy();
    this.chartInstances.visits = new Chart(ctx, {
      type: "line",
      data: {
        labels: chartData.map((item) => item.visit_date),
        datasets: [
          {
            label: "Number of Visits",
            data: chartData.map((item) => item.frequency),
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
    if (this.chartInstances.topGoers) this.chartInstances.topGoers.destroy();
    this.chartInstances.topGoers = new Chart(ctx, {
      type: "bar",
      data: {
        labels: chartData.map((item) => `${item.first_name} ${item.last_name}`),
        datasets: [
          {
            label: "Total Visits",
            data: chartData.map((item) => item.total_visits),
            backgroundColor: "#FF6B81",
          },
        ],
      },
      options: { responsive: true, maintainAspectRatio: false },
    });
  }

  renderBatchChart(chartData) {
    const ctx = this.querySelector("#batchChart").getContext("2d");
    if (this.chartInstances.batch) this.chartInstances.batch.destroy();
    this.chartInstances.batch = new Chart(ctx, {
      type: "bar",
      data: {
        labels: chartData.map((item) => item.batch),
        datasets: [
          {
            label: "Visits per Batch",
            data: chartData.map((item) => item.frequency),
            backgroundColor: "#FF6B81",
          },
        ],
      },
      options: { responsive: true, maintainAspectRatio: false },
    });
  }

  layout() {
    return /*html*/ `
      <div class="summary-tuning-bar">
        <label>Top Users Limit: <input type="number" id="topUsersLimit" value="5" min="1"></label>
        <label>Batch Limit: <input type="number" id="num_batches" value="6" min="1"></label>
      </div>

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
            <div class="kpi-item"><h2 id="kpi-time">0 mins</h2><p>Average time spent</p></div>
            <div class="kpi-item"><h2 id="kpi-visits-day">0</h2><p>Average visits/day</p></div>
            <div class="kpi-item"><h2 id="kpi-total">0</h2><p>Total visits</p></div>
          </div>
        </div>
      </div>
    `;
  }
}
customElements.define("dashboard-summary", DashboardSummaryComponent);

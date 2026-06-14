class DashboardTableComponent extends HTMLElement {
  constructor() {
    super();
    this.page = 1;
    this.limit = 100;
    this.totalPages = 1;
    this.columns = [];
    this.headers = [];
  }

  connectedCallback() {
    this.columns = JSON.parse(this.getAttribute("columns") || "[]");
    this.headers = JSON.parse(this.getAttribute("headers") || "[]");

    this.innerHTML = this.layout();

    this.querySelector(".limit-select").addEventListener("change", (e) => {
      this.limit = parseInt(e.target.value);
      this.page = 1;
      this.dispatchPageChange();
    });
  }

  dispatchPageChange() {
    this.dispatchEvent(new CustomEvent("page-change", { bubbles: true }));
  }

  updateTable(dataArray, totalPages) {
    this.totalPages = totalPages;
    const tbody = this.querySelector(".table-body");
    tbody.innerHTML = "";

    if (!dataArray || dataArray.length === 0) {
      tbody.innerHTML = `<tr><td colspan="${this.columns.length + 1}">No records found</td></tr>`;
      this.renderPagination();
      return;
    }

    dataArray.forEach((row, index) => {
      const tr = document.createElement("tr");
      const rowNum = (this.page - 1) * this.limit + index + 1;
      tr.innerHTML =
        `<td>${rowNum}</td>` +
        this.columns.map((col) => `<td>${row[col] || ""}</td>`).join("");
      tbody.appendChild(tr);
    });

    this.renderPagination();
  }

  renderPagination() {
    const container = this.querySelector(".pages-container");
    container.innerHTML = "";
    if (this.totalPages <= 1) return;

    const createButton = (text, targetPage, isActive = false) => {
      const btn = document.createElement("button");
      btn.textContent = text;
      btn.className = `page-num-btn ${isActive ? "active" : ""}`;
      btn.disabled = targetPage === null;
      if (targetPage !== null && !isActive) {
        btn.addEventListener("click", () => {
          this.page = targetPage;
          this.dispatchPageChange();
        });
      }
      return btn;
    };

    container.appendChild(
      createButton("◀", this.page > 1 ? this.page - 1 : null),
    );

    let pages = [];
    if (this.totalPages <= 5) {
      pages = Array.from({ length: this.totalPages }, (_, i) => i + 1);
    } else {
      if (this.page <= 3) {
        pages = [1, 2, 3, "...", this.totalPages];
      } else if (this.page >= this.totalPages - 2) {
        pages = [
          1,
          "...",
          this.totalPages - 2,
          this.totalPages - 1,
          this.totalPages,
        ];
      } else {
        pages = [
          1,
          "...",
          this.page - 1,
          this.page,
          this.page + 1,
          "...",
          this.totalPages,
        ];
      }
    }

    pages.forEach((p) => {
      if (p === "...") {
        const span = document.createElement("span");
        span.textContent = "...";
        span.className = "page-ellipsis";
        container.appendChild(span);
      } else {
        container.appendChild(createButton(p, p, p === this.page));
      }
    });

    container.appendChild(
      createButton("▶", this.page < this.totalPages ? this.page + 1 : null),
    );
  }

  layout() {
    return /*html*/ `
      <div class="table-scroll-container">
        <table class="data-table">
          <thead>
            <tr>
              <th>No.</th>
              ${this.headers.map((h) => `<th>${h}</th>`).join("")}
            </tr>
          </thead>
          <tbody class="table-body"></tbody>
        </table>
      </div>
      
      <div class="pagination-footer">
        <div class="limit-selector-group">
          <span>Show entries per page:</span>
          <select class="limit-select">
            <option value="10">10</option>
            <option value="25">25</option>
            <option value="50">50</option>
            <option value="100" selected>100</option>
          </select>
        </div>
        <div class="pages-container pages-links-group"></div>
      </div>
    `;
  }
}
customElements.define("dashboard-table", DashboardTableComponent);

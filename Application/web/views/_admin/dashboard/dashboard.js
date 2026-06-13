import "../../../components/navbar/navbar.js";

class DashboardViewComponent extends HTMLElement {
  connectedCallback() {
    this.innerHTML = this.layout();
    const testBtn = document.getElementById("testBtn");

    testBtn.addEventListener("click", async () => {
      await window.router("settings");
    });

    const dashboardDataBtn = document.getElementById("dashboardDataBtn");
    dashboardDataBtn.addEventListener("click", async () => {
      const form_data = {
        filters: {
          start_date: document.getElementById("start-date").value,
          end_date: document.getElementById("end-date").value,
          search_name: document.getElementById("search-name").value,
          batch: document.getElementById("batch").value,
          sex: document.getElementById("sex").value,
        },
        topUsersLimit: document.getElementById("topUsersLimit").value,
        num_batches: document.getElementById("num_batches").value,
        page: document.getElementById("page").value,
        page_size: document.getElementById("page_size").value,
      };

      console.log(form_data);

      const response = await window.pywebview.api.get_dashboard_data(form_data);
      if (response.status === "success") {
        console.log(response.data);
      } else console.log("error occured");
    });

    const attendanceHistoryBtn = document.getElementById(
      "attendanceHistoryBtn",
    );
    attendanceHistoryBtn.addEventListener("click", async () => {
      const form_data = {
        filters: {
          start_date: document.getElementById("start-date").value,
          end_date: document.getElementById("end-date").value,
          search_name: document.getElementById("search-name").value,
          batch: document.getElementById("batch").value,
          sex: document.getElementById("sex").value,
        },
        topUsersLimit: document.getElementById("topUsersLimit").value,
        num_batches: document.getElementById("num_batches").value,
        page: document.getElementById("page").value,
        page_size: document.getElementById("page_size").value,
      };

      console.log(form_data);

      const response =
        await window.pywebview.api.get_attendance_history(form_data);
      if (response.status === "success") {
        console.log(response.data);
      } else console.log("error occured");
    });

    const registeredUsersBtn = document.getElementById("registeredUsersBtn");
    registeredUsersBtn.addEventListener("click", async () => {
      const form_data = {
        filters: {
          start_date: document.getElementById("start-date").value,
          end_date: document.getElementById("end-date").value,
          search_name: document.getElementById("search-name").value,
          batch: document.getElementById("batch").value,
          sex: document.getElementById("sex").value,
        },
        topUsersLimit: document.getElementById("topUsersLimit").value,
        num_batches: document.getElementById("num_batches").value,
        page: document.getElementById("page").value,
        page_size: document.getElementById("page_size").value,
      };

      console.log(form_data);

      const response =
        await window.pywebview.api.get_registered_users(form_data);
      if (response.status === "success") {
        console.log(response.data);
      } else console.log("error occured");
    });
  }

  layout() {
    return /*html*/ `
    <app-navbar></app-navbar>
    <main>
        <h2>Dashboard</h2>
        <!-- Test -->
         <button id="testBtn">Go to settings</button>

          <!-- Filters -->
           <label for="start-date">Choose start date</label>
           <input type="date" id="start-date" name="start-date">
           <label for="end-date">Choose end date</label>
           <input type="date" name="end-date" id="end-date">
           <label for="search-name">Search Name</label>
           <input type="text" name="search-name" id="search-name">
           <label for="batch">Batch</label>
           <input type="text" name="batch" id="batch">
           <label for="sex">Sex</label>
           <input type="text" name="sex" id="sex">

           <label for="topUsersLimit">Top Users Count/Limit</label>
           <input type="number" name="topUsersLimit" id="topUsersLimit" value="5">

           <label for="num_batches">Number of Batches Limit</label>
           <input type="number" name="num_batches" id="num_batches" value="6">

            <label for="page">Current Page</label>
            <input type="number" name="page" id="page" value="1">

            <label for="page_size">Number of items in a page</label>
            <input type="number" name="page_size" id="page_size" value="100">

         <button id="dashboardDataBtn">Dashboard Data</button>
         <button id="attendanceHistoryBtn">Attendance History </button>
         <button id="registeredUsersBtn">Regisrered Users</button>

    </main>
    `;
  }
}

customElements.define("app-dashboard", DashboardViewComponent);

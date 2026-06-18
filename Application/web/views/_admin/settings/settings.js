import "../../../components/navbar/navbar.js";

class SettingsViewComponent extends HTMLElement {
  constructor() {
    super();
    this.faculties = [];
    this.activeTabId = "content-general";
  }

  async connectedCallback() {
    this.innerHTML = this.layout();
    this.initTabNavigation();
    this.initEventListeners();

    // Automatically fetch and load faculty database on render
    await this.loadFacultyTable();
  }

  // --- TAB NAVIGATION ---
  initTabNavigation() {
    const tabs = this.querySelectorAll(".sidebar .tab");
    tabs.forEach((tab) => {
      tab.addEventListener("click", () => {
        const targetTab = tab.getAttribute("data-tab");
        this.switchTab(targetTab);
      });
    });
    this.switchTab(this.activeTabId);
  }

  switchTab(tabId) {
    this.activeTabId = tabId;
    const contents = this.querySelectorAll(".tab-content");
    contents.forEach((content) => {
      content.style.display = content.id === tabId ? "flex" : "none";
    });

    const tabs = this.querySelectorAll(".sidebar .tab");
    tabs.forEach((tab) => {
      if (tab.getAttribute("data-tab") === tabId) {
        tab.classList.add("active");
      } else {
        tab.classList.remove("active");
      }
    });
  }

  // --- MODAL SYSTEM CONTROLS ---
  openModal(modalId) {
    const modal = this.querySelector(`#${modalId}`);
    if (modal) modal.style.display = "block";
  }

  closeModal(modalId) {
    const modal = this.querySelector(`#${modalId}`);
    if (modal) modal.style.display = "none";
  }

  clearInputs(ids) {
    ids.forEach((id) => {
      const el = this.querySelector(`#${id}`);
      if (el) el.value = "";
    });
  }

  // --- EVENT ATTACHMENTS ---
  initEventListeners() {
    // Router Return Button
    this.querySelector("#returnToDashboardButton").addEventListener(
      "click",
      async () => {
        await window.router("dashboard");
      },
    );

    // Outer click triggers modal dismissal
    this.addEventListener("click", (e) => {
      if (e.target.classList.contains("modal")) {
        e.target.style.display = "none";
      }
    });

    // Modal Close Triggers
    this.querySelectorAll(".close-button, .cancel-btn").forEach((btn) => {
      btn.addEventListener("click", (e) => {
        const modal = e.target.closest(".modal");
        if (modal) modal.style.display = "none";
      });
    });

    // Action Trigger: Admin Password Submission
    this.querySelector("#submitAdminPassBtn").addEventListener("click", () =>
      this.handleAdminPasswordChange(),
    );

    // Action Trigger: Direct Student Update Execution
    this.querySelector("#save-student-details-changes-btn").addEventListener(
      "click",
      () => this.handleSaveStudentInfo(),
    );

    // Action Trigger: Target Save Faculty Updates
    this.querySelector("#saveFacultyChangesBtn").addEventListener("click", () =>
      this.handleSaveFacultyInfo(),
    );
  }

  // --- BACKEND WRAPPER INTERFACES ---

  // Admin Change Password API Implementation
  async handleAdminPasswordChange() {
    const oldPassword = this.querySelector("#old-password").value;
    const newPassword = this.querySelector("#new-password").value;
    const confirmPassword = this.querySelector(
      "#new-password-confirmation",
    ).value;

    if (newPassword !== confirmPassword) {
      alert("The Confirmation Password does not match.");
      return;
    }

    if (confirm("Are you sure you want to change the password?")) {
      try {
        const response = await window.pywebview.api.auth.change_password(
          oldPassword,
          newPassword,
          confirmPassword,
        );
        if (response && response.status === "success") {
          alert("Password updated successfully");
          this.closeModal("modal-change-admin-pass");
          this.clearInputs([
            "old-password",
            "new-password",
            "new-password-confirmation",
          ]);
        } else {
          alert(`Failed: ${response?.message || "Unknown error occurred"}`);
        }
      } catch (error) {
        console.error("Error setting password changes:", error);
        alert(
          "Unexpected communication breakdown via python bridge runtime ecosystem.",
        );
      }
    }
  }

  // Data Aggregator: Get & Display Faculty Table Content
  async loadFacultyTable() {
    try {
      const response = await window.pywebview.api.faculty.get_all_faculty();
      const tbody = this.querySelector(".facultyTable tbody");

      if (response && response.status === "success") {
        this.faculties = response.data.faculties || [];
        tbody.innerHTML = this.faculties
          .map(
            (fac, idx) => `
          <tr data-id="${fac.id}">
            <td>${idx + 1}</td>
            <td class="cell-id">${fac.id}</td>
            <td class="cell-first-name">${fac.first_name}</td>
            <td class="cell-last-name">${fac.last_name}</td>
            <td class="cell-sex">${fac.sex}</td>
            <td>
              <button class="edit-btn">Edit</button>
            </td>
          </tr>
        `,
          )
          .join("");

        tbody.querySelectorAll(".edit-btn").forEach((btn) => {
          btn.addEventListener("click", (e) =>
            this.popFacultyEditModal(e.target.closest("tr")),
          );
        });
      }
    } catch (err) {
      console.error("Unable to load faculty structure: ", err);
    }
  }

  // Faculty Update Entry Routing Initialization
  popFacultyEditModal(row) {
    this.querySelector("#faculty-id").value =
      row.querySelector(".cell-id").innerText;
    this.querySelector("#faculty-firstName").value =
      row.querySelector(".cell-first-name").innerText;
    this.querySelector("#faculty-lastName").value =
      row.querySelector(".cell-last-name").innerText;
    this.querySelector("#faculty-sex").value =
      row.querySelector(".cell-sex").innerText;

    this.openModal("editForm");
  }

  // Row Processing: Submit Faculty Mutation Operations
  async handleSaveFacultyInfo() {
    const targetId = this.querySelector("#faculty-id").value;
    const firstName = this.querySelector("#faculty-firstName").value.trim();
    const lastName = this.querySelector("#faculty-lastName").value.trim();
    let sex = this.querySelector("#faculty-sex").value.trim();

    sex = sex.toLowerCase();
    sex = sex.charAt(0).toUpperCase() + sex.slice(1);

    if (sex.toUpperCase() !== "M" && sex.toUpperCase() !== "F") {
      alert("Incorrect Sex Input: Please Enter Either M or F");
      return;
    }

    const dataPayload = {
      id: targetId,
      first_name: firstName,
      last_name: lastName,
      sex: sex,
    };

    try {
      const response =
        await window.pywebview.api.faculty.update_faculty(dataPayload);
      if (response && response.status === "success") {
        alert("Faculty modifications processed successfully.");
        this.closeModal("editForm");
        await this.loadFacultyTable();
      } else {
        alert(`Failed to save changes: ${response.message}`);
      }
    } catch (err) {
      console.error(err);
      alert(
        "Error occurred updating context changes across environment execution framework.",
      );
    }
  }

  // Direct Student Mutation Dispatch (Without initial lookup requirement)
  async handleSaveStudentInfo() {
    const studentID = this.querySelector("#student-id-input").value.trim();
    const firstName = this.querySelector("#student-firstName").value.trim();
    const lastName = this.querySelector("#student-lastName").value.trim();

    // KEEP AS STRING: Do not use parseInt(), leave it as the raw input string value
    const batch = this.querySelector("#student-batch").value.trim();

    // Map full names to single character codes ('M' or 'F') expected by SexEnum
    const sexInput = this.querySelector("#student-sex").value;
    const sex = sexInput === "Male" ? "M" : "F";

    if (!studentID || !firstName || !lastName || !batch) {
      alert("Please fill out all fields (including Student ID) before saving.");
      return;
    }

    if (
      confirm(
        "Are you sure about the changes? This will update the student matching this ID, overriding registration fields.",
      )
    ) {
      const dataPayload = {
        id: studentID,
        first_name: firstName,
        last_name: lastName,
        sex: sex, // Sends 'M' or 'F'
        batch: batch, // Sends as String (e.g. "2026")
      };

      try {
        const response =
          await window.pywebview.api.student.update_student(dataPayload);
        if (response && response.status === "success") {
          alert("Student profile updated successfully.");
          this.closeModal("modal-change-student-details");
          this.clearInputs([
            "student-id-input",
            "student-firstName",
            "student-lastName",
            "student-batch",
          ]);
        } else {
          alert(`Error saving configuration changes: ${response.message}`);
        }
      } catch (error) {
        console.error(
          "Error executing backend update routing wrapper stack:",
          error,
        );
        alert(
          "Failed to submit student changes via pywebview interface layer.",
        );
      }
    }
  }

  // --- LAYOUT STRUCTURAL MARKUP COMPONENT SCHEMA ---
  layout() {
    return /*html*/ `
    <div class="container">
        <div class="sidebar">
            <div class="sidebar-nav-group">
                <button class="tab active" data-tab="content-general">General</button>
                <button class="tab" data-tab="content-faculties">Manage Faculty Accounts</button>
            </div>
            <button id="returnToDashboardButton">Return to Dashboard</button>
        </div>

        <div class="content">
            
            <div id="content-general" class="tab-content">
                <h2 class="tab-header">General Settings</h2>
                
                <button class="category-button" id="triggerChangeAdminPassBtn" onclick="document.querySelector('app-settings').openModal('modal-change-admin-pass')">
                    <div class="category-text-container">
                        <h5 class="category-header">Change Admin Password</h5>
                        <label class="category-subheader">Update the password required to access the Data Dashboard</label>
                    </div>
                    <div class="button-sign">&#9654</div>
                </button>

                <button class="category-button" id="triggerChangeStudentDetailsBtn" onclick="document.querySelector('app-settings').openModal('modal-change-student-details')">
                    <div class="category-text-container">
                        <h5 class="category-header">Change Student Details</h5>
                        <label class="category-subheader">Modify Student Profile matching an ID (First/Last Name, Batch, and Sex)</label>
                    </div>
                    <div class="button-sign">&#9654</div>
                </button>

                <div class="modal" id="modal-change-admin-pass">
                    <div class="modal-content">
                        <button class="close-button">&#128937</button>
                        <h3 class="modal-header">Change Admin Password</h3>
                        <label class="modal-subheader">Update the password required to access the Data Dashboard</label>
                        <div class="password-inputs">
                            <label>Enter Current Password</label>
                            <input id="old-password" type="password">
                        </div>
                        <div class="password-inputs">
                            <label>Enter New Password</label>
                            <input id="new-password" type="password">
                        </div>
                        <div class="password-inputs">
                            <label>Confirm New Password</label>
                            <input id="new-password-confirmation" type="password">
                        </div>
                        <button class="saveButton" id="submitAdminPassBtn">Submit</button>
                    </div>
                </div>

                <div class="modal" id="modal-change-student-details">
                    <div class="modal-content">
                        <button class="close-button">&#128937</button>
                        <h3 class="modal-header">Update Student Profile</h3>
                        <label class="modal-subheader">Enter target Student ID along with new record updates.</label>
                        <div class="student-info">
                            <label>Target Student ID</label>
                            <input id="student-id-input" placeholder="e.g., STU-12345">
                            
                            <label>First Name</label>
                            <input id="student-firstName">
                            
                            <label>Last Name</label>
                            <input id="student-lastName">
                            
                            <label>Batch</label>
                            <input id="student-batch" type="number">
                            
                            <label>Sex</label>
                            <select id="student-sex">
                                <option value="Male">Male</option>
                                <option value="Female">Female</option>        
                            </select>
                            <button class="saveButton" id="save-student-details-changes-btn">Save Changes</button>
                        </div>
                    </div>
                </div>
            </div>

            <div id="content-faculties" class="tab-content">
                <h2>Manage Faculty Accounts</h2>
                <label class="category-subheader">Edit or remove faculty accounts for the program</label>
                <div class="table-container">
                    <table class="facultyTable">
                        <thead>
                            <tr>
                                <th>No.</th>
                                <th>Faculty ID</th>
                                <th>First Name</th>
                                <th>Last Name</th>
                                <th>Sex</th>
                                <th>Action</th>
                            </tr>
                        </thead>
                        <tbody>
                           </tbody>
                    </table>
                </div>
            </div>

        </div>
    </div>

    <div class="edit-form modal" id="editForm">
        <div class="modal-content">
            <button class="close-button">&#128937</button>
            <h2>Edit Faculty Details</h2>
            <div id="editFormContent">
                <label for="faculty-id">ID:</label>
                <input type="text" id="faculty-id">
                
                <label for="faculty-firstName">First Name:</label>
                <input type="text" id="faculty-firstName">
                
                <label for="faculty-lastName">Last Name:</label>
                <input type="text" id="faculty-lastName">
                
                <label for="faculty-sex">Sex:</label>
                <input type="text" id="faculty-sex">
                
                <div style="margin-top: 15px; display:flex; gap: 10px;">
                     <button type="button" class="saveButton" id="saveFacultyChangesBtn" style="margin: 0;">Save Changes</button>
                     <button type="button" class="cancel-btn saveButton" style="background-color: #888; margin: 0;">Cancel</button>
                </div>
            </div>
        </div>
    </div>
    `;
  }
}

customElements.define("app-settings", SettingsViewComponent);

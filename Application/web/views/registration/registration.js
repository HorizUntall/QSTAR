import "../../components/navbar/navbar.js";

class RegistrationViewComponent extends HTMLElement {
  connectedCallback() {
    // Retrieve data passed by router
    this.viewData = window.routerState || {};
    window.routerState = undefined; // Cleanup

    // This page needs qr code and user type.
    // if viewData lacks any of them, return to homepage
    if (
      !(
        Object.hasOwn(this.viewData, "id") &&
        Object.hasOwn(this.viewData, "user_type")
      )
    ) {
      alert("An error occurred. Please try again"); // <-- IMPROVE
      (async () => {
        await window.router("homepage");
      })();
      return;
    }
    this.innerHTML = this.layout();

    // If user is a faculty, then remove the input for batch
    if (this.viewData.user_type === "faculty") {
      document.getElementById("sex").remove();
    }

    // Button to return to homepage
    const returnBtn = document.getElementById("returnBtn");
    returnBtn.addEventListener("click", async () => {
      await window.router("homepage");
    });

    // Form Submission
    const registrationForm = document.getElementById("registrationForm");
    registrationForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      let form = document.forms["registrationForm"];

      const form_data = {
        id: this.viewData.id,
        user_type: this.viewData.user_type,
        first_name: form["firstName"].value,
        last_name: form["lastName"].value,
        sex: form["sex"].value,
      };
      if (this.viewData.user_type === "student") {
        form_data.batch = form["batch"].value;
      }

      // Call API
      const response = await window.pywebview.api.register_new_user(form_data);
      if (response === "success") {
        alert("Success"); // <-- IMPROVE
        window.router("homepage");
      } else {
        alert(response.message);
      }
    });
  }

  layout() {
    return /*html*/ `
    <main>
        <form action="submit" id="registrationForm">
            <label for="firstName">First Name</label>
            <input type="text" id="firstName" name="firstName" required>
            <label for="lastName">Last Name</label>
            <input type="text" id="lastName" name="lastName" required>
            <label for="batch">Batch Year</label>
            <input type="number" id="batch" name="batch" required>
            <select id="sex" name="sex" required>
                <option value="">Select an option...</option>
                <option value="M">Male</option>
                <option value="F">Female</option>
            </select>

            <button id="returnBtn">Back to Homepage</button>
            <button type="submit">Register</button>
        </form>
    </main>
    `;
  }
}

customElements.define("app-registration", RegistrationViewComponent);

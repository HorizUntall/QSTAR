import "../../components/navbar/navbar.js";

class RegistrationViewComponent extends HTMLElement {
  constructor() {
    super();
    this.extractedUserData = {};
    this.viewData = {};
    this.isTermsAccepted = false;
  }

  async connectedCallback() {
    // Globally hide the navbar while on this full-screen gate page
    this.globalNavbar = document.querySelector("app-navbar");
    if (this.globalNavbar) this.globalNavbar.style.display = "none";

    // Retrieve data passed by router
    this.viewData = window.routerState || {};
    window.routerState = undefined; // Cleanup
    console.log(this.viewData);

    // Extract nested data from meta.data if it exists
    const userData = this.viewData.meta?.data || {};

    // This page needs qr code and user type.
    // if userData lacks any of them, return to homepage safely without using native alert loops
    if (
      !(Object.hasOwn(userData, "id") && Object.hasOwn(userData, "user_type"))
    ) {
      this.showToast("An error occurred. Please try again.", "error");
      const fallbackRouter = window.router;
      setTimeout(async () => {
        if (typeof fallbackRouter === "function") {
          await fallbackRouter("homepage");
        } else {
          window.location.reload();
        }
      }, 2500);
      return;
    }

    // Store the extracted data for easier access throughout the component
    this.extractedUserData = userData;

    // Render original layout structures
    this.innerHTML = this.layout();

    // Adjust structural form elements based on User Type (Faculty vs Student)
    this.adjustFormFieldsBasedOnRole();

    // Setup Interactive Event Listeners
    this.attachEventListeners();
  }

  disconnectedCallback() {
    // Restore the navbar layout when navigating away from registration
    if (this.globalNavbar) {
      this.globalNavbar.style.display = "";
    }
  }

  adjustFormFieldsBasedOnRole() {
    const batchGroup = this.querySelector(".batch-group");
    if (this.extractedUserData.user_type === "faculty" && batchGroup) {
      // Completely remove the batch layout option container
      batchGroup.remove();

      // Remove validation constraint requirements since it's hidden for faculty
      const batchInput = this.querySelector("#batch");
      if (batchInput) {
        batchInput.removeAttribute("required");
      }
    }
  }

  attachEventListeners() {
    // Exit & Return Actions
    const exitBtn = this.querySelector("#exitBtn");
    const returnBtn = this.querySelector("#returnBtn");
    const handleExit = async (e) => {
      e.preventDefault();
      if (typeof window.router === "function") {
        await window.router("homepage");
      }
    };
    if (exitBtn) exitBtn.addEventListener("click", handleExit);
    if (returnBtn) returnBtn.addEventListener("click", handleExit);

    // Data Privacy Overlay Controls
    const termsCheckbox = this.querySelector("#terms");
    const privacyPopup = this.querySelector("#privacyPopup");
    const acceptPrivacyBtn = this.querySelector("#accept_button");
    const closePrivacyBtn = this.querySelector("#closePrivacyBtn");

    if (termsCheckbox) {
      termsCheckbox.addEventListener("click", (e) => {
        // Prevent manual toggling directly without accepting modal text
        e.preventDefault();
        if (!this.isTermsAccepted) {
          this.togglePopup(privacyPopup, true);
        } else {
          this.isTermsAccepted = false;
          termsCheckbox.checked = false;
        }
      });
    }

    if (acceptPrivacyBtn) {
      acceptPrivacyBtn.addEventListener("click", () => {
        this.isTermsAccepted = true;
        if (termsCheckbox) termsCheckbox.checked = true;
        this.togglePopup(privacyPopup, false);
      });
    }

    if (closePrivacyBtn) {
      closePrivacyBtn.addEventListener("click", () => {
        this.isTermsAccepted = false;
        if (termsCheckbox) termsCheckbox.checked = false;
        this.togglePopup(privacyPopup, false);
      });
    }

    // Master Form Registration Triggers
    const registrationForm = this.querySelector("#registrationForm");
    if (registrationForm) {
      registrationForm.addEventListener("submit", (e) => {
        e.preventDefault();

        if (!this.isTermsAccepted) {
          this.showToast("You must agree to the Data Privacy Policy.", "error");
          return;
        }

        this.openReviewConfirmation();
      });
    }

    // Review Modal Submissions
    const closeReviewBtn = this.querySelector("#closeReviewBtn");
    const closeReviewModalX = this.querySelector("#closeReviewModalX");
    const confirmRegisterBtn = this.querySelector("#confirmRegisterBtn");
    const reviewPopup = this.querySelector("#reviewPopup");

    if (closeReviewBtn) {
      closeReviewBtn.addEventListener("click", () => {
        this.togglePopup(reviewPopup, false);
      });
    }

    if (closeReviewModalX) {
      closeReviewModalX.addEventListener("click", () => {
        this.togglePopup(reviewPopup, false);
      });
    }

    if (confirmRegisterBtn) {
      confirmRegisterBtn.addEventListener("click", () => {
        this.togglePopup(reviewPopup, false);
        this.executeRegistrationPayload();
      });
    }
  }

  togglePopup(popupElement, show) {
    const mainWidget = this.querySelector(".main_widget");
    if (!popupElement) return;

    if (show) {
      popupElement.style.display = "block";
      if (mainWidget) mainWidget.style.display = "none";
    } else {
      popupElement.style.display = "none";
      if (mainWidget) mainWidget.style.display = "flex";
    }
  }

  openReviewConfirmation() {
    let form = this.querySelector("#registrationForm");

    this.querySelector("#firstname_review").textContent =
      form["firstName"].value;
    this.querySelector("#lastname_review").textContent = form["lastName"].value;
    this.querySelector("#sex_review").textContent =
      form["sex"].value === "M" ? "Male" : "Female";
    this.querySelector("#id_review").textContent = this.extractedUserData.id;

    const batchReviewWrapper = this.querySelector("#batch_review_wrapper");
    if (this.extractedUserData.user_type === "student") {
      if (batchReviewWrapper) batchReviewWrapper.style.display = "block";
      this.querySelector("#batch_review").textContent = form["batch"].value;
    } else {
      if (batchReviewWrapper) batchReviewWrapper.style.display = "none";
    }

    this.togglePopup(this.querySelector("#reviewPopup"), true);
  }

  async executeRegistrationPayload() {
    let form = this.querySelector("#registrationForm");

    const form_data = {
      id: this.extractedUserData.id,
      user_type: this.extractedUserData.user_type,
      first_name: form["firstName"].value,
      last_name: form["lastName"].value,
      sex: form["sex"].value,
    };

    if (this.extractedUserData.user_type === "student") {
      form_data.batch = form["batch"].value;
    }

    try {
      // Call Modern pywebview API
      const response =
        await window.pywebview.api.user.register_new_user(form_data);

      // FIXED: Adjusted check to handle the python dictionary structure object return payload
      if (response && response.status === "success") {
        const fullName = `${form_data.first_name} ${form_data.last_name}`;

        // Hide the input forms entirely so the success message is isolated beautifully
        const mainWidget = this.querySelector(".main_widget");
        if (mainWidget) mainWidget.style.display = "none";

        this.showToast(
          `${fullName} successfully added to the database!`,
          "success",
        );

        // Store reference to global router helper scope safely
        const targetRouter = window.router;

        // Form Cleanup
        form.reset();
        this.isTermsAccepted = false;

        // Trigger safe auto routing back to homepage
        setTimeout(async () => {
          if (typeof targetRouter === "function") {
            await targetRouter("homepage");
          } else if (typeof window.router === "function") {
            await window.router("homepage");
          }
        }, 3000);
      } else {
        // Use the explicit dynamic backend message from dictionary response if available
        const errorMsg =
          response?.message ||
          "User entry already exists or registration failed.";
        this.showToast(errorMsg, "error");
      }
    } catch (err) {
      console.error("API Communication error:", err);
      this.showToast("Database connection error encountered.", "error");
    }
  }

  showToast(message, type) {
    const toast =
      type === "success"
        ? this.querySelector(".success_msg")
        : this.querySelector(".error_msg");
    if (!toast) return;

    toast.querySelector(".toast-text").textContent = message;
    toast.classList.add("animated");

    toast.addEventListener(
      "animationend",
      () => {
        toast.classList.remove("animated");
      },
      { once: true },
    );
  }

  layout() {
    return /*html*/ `
    <main class="main">

      <div id="privacyPopup" class="pop-up">
        <div class="exit1">
          <button id="closePrivacyBtn">x</button>
        </div>
        <div class="pop-up_info">
          <span id="pop-up_headers">Data Privacy Policy</span><br><br>
          <span>
            In accordance with the Republic Act No. 10173, otherwise known as the Data Privacy Act of 2012, all personal
            information gathered from this form shall be kept CONFIDENTIAL where only the authorized researchers and administrators 
            of this study shall have access to the said information.
          </span>
        </div>
        <div class="accept_button">
          <button id="accept_button">I accept the Data Privacy Policy</button>
        </div>
      </div>

      <div id="reviewPopup" class="pop-up2">
        <div class="exit2">
          <button id="closeReviewModalX">x</button>
        </div>
        <div class="review_content">
          <h1>Review Details</h1>
          <h3>ID No.:</h3>
          <p id="id_review"></p>
          <h3>First Name:</h3>
          <p id="firstname_review"></p>
          <h3>Last Name:</h3>
          <p id="lastname_review"></p>
          <div id="batch_review_wrapper">
            <h3>Batch:</h3>
            <p id="batch_review"></p>
          </div>
          <h3>Sex:</h3>
          <p id="sex_review"></p>
          <br>
          <div class="review-buttons">
            <button id="closeReviewBtn">Go Back</button>
            <button id="confirmRegisterBtn">Confirm</button>
          </div>
        </div>
      </div>

      <div class="main_widget">

        <div class="info">
          <div class="title_container">
            <img src="../../assets/images/PSHS-ZRC\ LOGO-modified.png" class="logo_title" alt="Q-Star Logo">
            <span class="info-title">Q-STAR</span>
            <span class="info-subtitle">QR-Based Student and Teacher Attendance Tracker</span>
          </div>
          <div class="general_info">
            In the pursuit of Digital Inclusion and sustainable technology, this project’s main objective is to develop and 
            integrate a QR-based digital attendance system in the PSHS-ZRC Library, called Q-STAR (QR-based Student-Tracking
            Attendance Recorder). Its purpose is to automate the attendance tracking system of the library. Doing so would 
            speed up the check-in process, decrease the chance of human error, aid in report-making and performance analysis, 
            and lessen paper usage.
          </div>
        </div>
        
        <div class="inputfields">
          <div class="exit">
            <button id="exitBtn">x</button>
          </div>

          <div class="input_title_text">
            <span class="input-title">Q-STAR</span>
            <span class="input-subtitle">Registration Form</span>
          </div>

          <form id="registrationForm" class="inputs">
            <div class="group1">
              <label for="firstName" class="form__label">First Name</label>
              <input type="text" class="form__field" name="firstName" id="firstName" required />
            </div>
            
            <div class="group2">
              <label for="lastName" class="form__label">Last Name</label>
              <input type="text" class="form__field" name="lastName" id="lastName" required />
            </div>

            <div class="group3">
              <div class="batch-group" style="margin-right: 1vw;">
                <label for="batch" class="form__label">Batch Year</label>
                <input type="number" class="form__field" name="batch" id="batch" min="1900" max="2100" required />
              </div>
              
              <div>
                <label for="sex" class="gender">Sex</label>
                <select name="sex" id="sex" required>
                  <option value=""></option>
                  <option value="M">Male</option>
                  <option value="F">Female</option>
                </select>
              </div>
            </div>

            <div class="terms">
              <input type="checkbox" id="terms" name="terms"> I agree to the <u>Data Privacy Policy</u>.
            </div>
            
            <div class="main-buttons">
              <button type="button" id="returnBtn">Back to Homepage</button>
              <button type="submit" id="register_button">Register</button>
            </div>
          </form>
        </div>
      </div>

      <div class="success_msg">
        <img src="../../assets/images/check.png" alt="Success">
        <span class="toast-text">Successfully added to the database!</span>
      </div>

      <div class="error_msg">
        <img src="../../assets/images/error_sign2.png" alt="Error">
        <span class="toast-text">Error processing records.</span>
      </div>

    </main>
    `;
  }
}

customElements.define("app-registration", RegistrationViewComponent);

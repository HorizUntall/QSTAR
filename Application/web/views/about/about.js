import "../../components/navbar/navbar.js";

class AboutViewComponent extends HTMLElement {
  connectedCallback() {
    this.innerHTML = this.layout();

    const testBtn = document.getElementById("testBtn");
    if (testBtn) {
      testBtn.addEventListener("click", async () => {
        await window.router("registration");
      });
    }
  }

  layout() {
    return /*html*/ `

        <main class="about-container">
            <h1>ABOUT</h1>
            <hr class="about-divider">
            
            <h2>What is Q-STAR?</h2>
            <p>
                The QR-Based Student Tracking Attendance Recorder (Q-STAR) is a collaborative project for the Filipino 6 
                and Social Science 6 subjects. The initiative is both a research endeavor and a community project designed
                to primarily benefit the school library’s attendance system.
                The goal is to automate the attendance tracking system of the library using a program that streamlines the 
                library’s attendance system through the implementation of a QR-based scanner. This program will scan a 
                user’s unique QR code displayed on their ID, and utilize that information to efficiently encode their 
                time-in and time-out in the system, together with information such as name, grade level, section, and 
                biological sex. This information can be compiled externally into a CSV file for an organized review 
                of student and library performance.                
            </p>

            <h2>Meet the incredible people behind the scenes</h2>
            <p>
                <b>Gabrielle Pauleen Tan</b>, the Project Manager, is responsible for planning, executing, and communicating with external 
                stakeholders for the project. Her duties include defining the project scope, setting objectives, creating a detailed 
                project plan, managing the team, monitoring the progress, mitigating risks, and ensuring that the project is delivered 
                on time and within budget while meeting its intended goals. She serves as the central point of coordination, 
                communication, and accountability for the success of the project.
            </p>
            <p>
                <b>Ray Emanuele Untal</b>, the Back-end Developer, is responsible for coding, testing, and maintaining software applications. 
                His duties involve translating project requirements into functional code for the back-end, debugging and resolving issues within 
                the back-end system, collaborating with other team members, and staying up-to-date with relevant back-end programming languages 
                and technologies; ensuring the application's back-end meets the quality and functionality standards.
            </p>
            <p>
                <b>Raphael Khandie Bihag</b>, the Front-End Developer, breathes life into the visual and interactive elements of 
                software applications. He transforms project requirements into user interfaces (UIs) that are both aesthetically 
                pleasing and user-friendly. Raphael's expertise lies in crafting user journeys, implementing responsive design for 
                various screen sizes, and ensuring seamless user interaction. He collaborates closely with designers and back-end 
                developers to bridge the gap between vision and functionality, while staying on top of the latest front-end technologies 
                to deliver exceptional user experiences.
            </p>
            <p>
                <b>Matt Angelo Sareno</b>, the Technical Writer, is responsible for producing clear, concise, and informative documentation
                for technical and non-technical audiences. His duties involve researching and understanding complex technical subjects and 
                translating this knowledge into user manuals, guides, and online documentation. He also collaborates with subject matter
                experts and ensures that documentation complies with industry standards while maintaining accuracy and clarity in conveying 
                technical information to end-users or other stakeholders.
            </p>
            <p>
                <b>Caryl Jan Pauline Agawin</b>, the Quality Assurance (QA) Tester, is responsible for evaluating the project output (software application)
                to identify defects and ensure they meet quality and performance standards. Her duties involve creating test plans, test cases, 
                and test scenarios, conducting manual or automated testing, reporting and documenting defects, and collaborating with the development
                team to resolve issues. She ensures the reliability and functionality of the project output, contributing to the delivery of a
                high-quality product to the end-users.
            </p>
            <p>
                <b>Mrs. Kathlyn G. Tangcay</b> is the main Stakeholder in this project. Her duties and responsibilities include providing 
                input, feedback, and requirements to ensure that the project aligns with her needs and expectations. She may also 
                participate in decision-making processes, support project activities, and communicate with the project team to ensure 
                that the project's goals and objectives are met successfully.
            </p>

            <div class="test-actions">
               <button id="testBtn">Switch page</button>
            </div>
        </main>
        `;
  }
}

customElements.define("app-about", AboutViewComponent);

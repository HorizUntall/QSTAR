var ticked = false;


function display_popup(classname) {
    const main = document.querySelector('.main_widget');

    if (classname == 'pop-up1') {
        const pop_up = document.querySelector('.pop-up');
        pop_up.style.display = 'block';
        main.style.display='none';
    } else {
        const pop_up = document.querySelector('.pop-up2');
        pop_up.style.display = 'block';
        main.style.display='none';
    }
}

function close_popup(classname) {
    const main = document.querySelector('.main_widget');
    if (classname == 'pop-up1') {
        const pop_up = document.querySelector('.pop-up');
        pop_up.style.display = 'none';
        main.style.display='flex';
    } else {
        const pop_up = document.querySelector('.pop-up2');
        pop_up.style.display = 'none';
        main.style.display='flex';
    }
}

function check_if_checked() {
    if (ticked == false) {
        display_popup('pop-up1');
    } else {
        document.getElementById('terms').checked = false;
        ticked = false;
    }
}

function update_terms(value) {
    if (value == true) {
        document.getElementById('terms').checked = true;
        ticked = true;
    } else {
        document.getElementById('terms').checked = false;
        ticked = false;
    }
}

function submit_verification() {
    var firstname = document.getElementById("firstname").value;
    var lastname = document.getElementById("lastname").value;
    var batch = document.getElementById("batchyear").value;
    var sex = document.getElementById("gender").value;
    var terms = document.getElementById("terms").checked;

    if (firstname != "" && lastname != "" && batch != null && batch.length == 4 && sex != "" && terms == true){
        display_popup('pop-up2');
        review_details();

    } else {
        alert("Fill up all the needed details.")
    }
}

function review_details() {
    const firstname = document.getElementById("firstname").value;
    const lastname = document.getElementById("lastname").value;
    const batch = document.getElementById("batchyear").value;
    const sex = document.getElementById("gender").value;

    document.getElementById("firstname_review").innerHTML = firstname;
    document.getElementById("lastname_review").innerHTML = lastname;
    document.getElementById("batch_review").innerHTML = batch;
    document.getElementById("sex_review").innerHTML = sex;

    eel.get_last_code()(function(output) {
        document.getElementById("id_review").innerHTML = output;
    });
}

function animate_success() {
    const firstname = document.getElementById("firstname");
    const lastname = document.getElementById("lastname");
    const batch = document.getElementById("batchyear");
    const sex = document.getElementById("gender");
    const registered_name = document.getElementById('registered_name');
    const terms = document.getElementById("terms");

    registered_name.innerHTML = firstname.value + " " + lastname.value;
    firstname.value = '';
    lastname.value = '';
    batch.value = '';
    sex.value = '';
    terms.checked = false;
    
    const success_msg = document.querySelector(".success_msg");

    success_msg.classList.add("animated");

    success_msg.addEventListener('animationend', () => {
        success_msg.classList.remove("animated");
    });
}



function animate_error() {
    const registered_name = document.getElementById('registered_name');
    registered_name.innerHTML = firstname.value + " " + lastname.value;
    const error_msg = document.querySelector(".error_msg");
    error_msg.classList.add("animated");

    error_msg.addEventListener('animationend', () => {
        error_msg.classList.remove("animated");
    });
}

function randomize_studentID() {
    let firstSection = Math.floor(Math.random() * 100).toString().padStart(2, '0');
    let secondSection = Math.floor(Math.random() * 10000).toString().padStart(4, '0');
    let thirdSection = Math.floor(Math.random() * 1000).toString().padStart(3, '0');

    // Combine the sections with hyphens
    let randomizedString = firstSection + '-' + secondSection + '-' + thirdSection;

    return randomizedString;
}

function register_student() {
    let studentID = document.getElementById('id_review').innerHTML;
    let firstName = document.getElementById('firstname_review').innerHTML;
    let lastName = document.getElementById('lastname_review').innerHTML;
    let batch = document.getElementById('batch_review').innerHTML;
    let sex = document.getElementById('sex_review').innerHTML;

    eel.verifier(studentID)(function(position){

        console.log(position);

        eel.register(studentID, firstName, lastName, batch, sex, position[0])(function(response){
            console.log(response);
                if (response == "NONE") {
                    animate_error();
                    close_popup('pop-up2');
                } else {
                    close_popup('pop-up2');
                    animate_success();
                    setTimeout(window.location.href = "../homepage.html", 5000);
                }
        })
    });

    
}

window.onload = function() {
    let dashboardlink = document.getElementById('DashboardLink');
    dashboardlink.style.fontFamily = 'FuturaHeavy';
    load_graphs();
    Chart.defaults.font.family = "Lato";
    display_table('Data');
};

function linechart(data_input) {
    let canvasElement = document.getElementById("visitsVStime");

    if (canvasElement) {
        canvasElement.remove();
    }

    // Create a new canvas element
    let newCanvas = document.createElement("canvas");
    newCanvas.id = "visitsVStime";

    // Add the new canvas to the container (assuming the container has class "graph1")
    let container = document.querySelector(".graph1");
    container.appendChild(newCanvas);

    var ctxLine = document.getElementById('visitsVStime').getContext('2d');
    var myLineChart = new Chart(ctxLine, {
    type: 'line', // Set chart type to 'bar' for a bar chart
    data: [],
    options: {
        plugins: {legend: {display: false}, title:{display: true, color: 'black', text: "  Library Visits vs Time", align: 'start', padding: {left: 5, bottom: 5},font: {size: 20, weight: 'bold'}}},
        responsive: true,
        maintainAspectRatio: false,
        scales : {
            y:{title: {display: true, text: 'Frequence'}},
            x:{title: {display: true, text: 'Date'}, ticks: {
                autoSkip: true,
                maxTicksLimit: 10,
            }},
        },
    },
    });
    myLineChart.data = data_input;
    myLineChart.update();
};

function barchart(data_input) {
    
    let canvasElement = document.getElementById("batchVisits");

    if (canvasElement) {
        canvasElement.remove();
    }

    // Create a new canvas element
    let newCanvas = document.createElement("canvas");
    newCanvas.id = "batchVisits";

    // Add the new canvas to the container (assuming the container has class "graph1")
    let container = document.querySelector(".graph3");
    container.appendChild(newCanvas);

    Chart.defaults.font.family = "Lato";
    var ctxBar = document.getElementById('batchVisits').getContext('2d');
    var myBarChart = new Chart(ctxBar, {
    type: 'bar', // Set chart type to 'bar' for a bar chart
    data: data_input,
    options: {
        plugins: {legend: {display: false}, title:{display: true, color: 'black', text: "   Library Visits per Batch", align: 'start', padding: {left: 5, bottom: 5},font: {size: 15, weight: 'bold'}}},
        responsive: true,
        maintainAspectRatio: false,
        scales : {
            y:{title: {display: true, text: 'Frequency'}},
            x:{title: {display: true, text: 'Batch'}, ticks: {
                autoSkip: true,
                maxTicksLimit: 10,
            }},
        },
    },
    });
    myBarChart.update();
};

function barchart2(data_input) {
    
    let canvasElement = document.getElementById("top_students");

    if (canvasElement) {
        canvasElement.remove();
    }

    // Create a new canvas element
    let newCanvas = document.createElement("canvas");
    newCanvas.id = "top_students";

    // Add the new canvas to the container (assuming the container has class "graph1")
    let container = document.querySelector(".graph2");
    container.appendChild(newCanvas);

    Chart.defaults.font.family = "Lato";
    var ctxBar = document.getElementById('top_students').getContext('2d');
    var myBarChart = new Chart(ctxBar, {
    type: 'bar', // Set chart type to 'bar' for a bar chart
    data: data_input,
    options: {
        plugins: {legend: {display: false}, title:{display: true, color: 'black', text: "Top Library Goers", align: 'start', padding: {left: 5, bottom: 5},font: {size: 15, weight: 'bold'}}},
        responsive: true,
        maintainAspectRatio: false,
        scales : {
            y:{title: {display: true, text: 'Frequency'}},
            x:{title: {display: true, text: 'Library User'}, ticks: {
                autoSkip: true,
                maxTicksLimit: 5,
            }},
        },
    },
    });
    myBarChart.update();
};

const customDateInput = document.getElementById('customDate');
const todayInput = document.getElementById('today');
const customLabel = document.getElementById('customLabel');
const customDates = document.querySelector('.custom-dates');
var visibility_tick = false;
var admin_password = 'admin';


customDateInput.addEventListener('change', function() {
    if (this.checked) {
        customDates.style.display = 'inline-block';
    } else {
        customDates.style.display = 'none';
    }
});

todayInput.addEventListener('change', function() {
    if (this.checked) {
        customDates.style.display = 'none';
    }
});


function display_table(tab) {
    let dashboardDiv = document.querySelector('.dashboard');
    let dataSummary = document.getElementById('DataSummary');
    let attendanceHistory = document.getElementById('AttendanceHistory');
    let attendancetableDiv = document.querySelector('.attandance_table');
    let registered = document.getElementById('RegisteredPeople');
    let registeredtableDiv = document.querySelector('.registered_table');
    
    if (tab == 'Attendance') {
        attendancetableDiv.style.display = 'block';
        attendanceHistory.style.fontFamily = 'FuturaHeavy';
        dashboardDiv.style.display = 'none';
        dataSummary.style.fontFamily = 'FuturaBook';
        registeredtableDiv.style.display = 'none';
        registered.style.fontFamily = 'FuturaBook';
    } else if (tab == 'Registered') {
        attendancetableDiv.style.display = 'none';
        attendanceHistory.style.fontFamily = 'FuturaBook';
        dashboardDiv.style.display = 'none';
        dataSummary.style.fontFamily = 'FuturaBook';
        registeredtableDiv.style.display = 'block';
        registered.style.fontFamily = 'FuturaHeavy';
    } else if (tab == 'Data') {
        attendancetableDiv.style.display = 'none';
        attendanceHistory.style.fontFamily = 'FuturaBook';
        dashboardDiv.style.display = 'block';
        dataSummary.style.fontFamily = 'FuturaHeavy';
        registeredtableDiv.style.display = 'none';
        registered.style.fontFamily = 'FuturaBook';
    }

}

function load_tableAttendance(lista) {
    let theTable = document.querySelector('.theTable_attendance');
    eel.convert_htmlTable_filters(lista)(function(table_contents) {
        theTable.innerHTML = table_contents;
    })
}

function load_tableRegistered(lista) {
    let theTable = document.querySelector('.theTable_registered');
    eel.convert_htmlTable_filters_registered(lista)(function(table_contents) {
        theTable.innerHTML = table_contents;
    })
}

function togglevisibility() {
    let icon = document.getElementById('visibility');
    let inputpass = document.getElementById('password');
    if (visibility_tick == true) {
        visibility_tick = false;
        icon.src='images/view.png';
        inputpass.type="password";
    } else {
        visibility_tick = true;
        icon.src='images/blind.png';
        inputpass.type="input";
    }
}

function handleEnter(event) {
    if (event.code === "Enter") {
      // Your function to be called on ENTER press
      verify_password();
    }
}

function verify_password() {
    let inputpass = document.getElementById('password').value;
    let everything = document.querySelector('.everything_dashboard');
    let verification = document.querySelector('.verification');
    let body = document.body;

    if (inputpass == admin_password) {
        everything.style.display = 'block';
        verification.style.display = 'none';
        body.style = "background-color: white; overflow: auto;"
    } else {
        alert('Incorrect Password');
    }
}

function getTodayFormatted() {
    let today = new Date();
    let dd = String(today.getDate()).padStart(2, '0'); // Day with leading zero
    let mm = String(today.getMonth() + 1).padStart(2, '0'); // Month with leading zero (January is 0!)
    let yyyy = today.getFullYear();
    return `${yyyy}-${mm}-${dd}`;
}

function getTomorrowFormatted(){
    let tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1); // Add 1 day to get tomorrow's date
    let dd = String(tomorrow.getDate()).padStart(2, '0'); // Day with leading zero
    let mm = String(tomorrow.getMonth() + 1).padStart(2, '0'); // Month with leading zero (January is 0!)
    let yyyy = tomorrow.getFullYear();
    return `${yyyy}-${mm}-${dd}`;
}

function get_filters() {
    let today = document.getElementById('today');
    let name = document.getElementById('Name').value;
    let sex = document.getElementById('Sex').value;
    let batch = document.getElementById('Batch').value;
    let start_date = document.getElementById('startDate').value;
    let end_date = document.getElementById('endDate').value;

    if (name.length == 0) {
        name = 'NONE';
    }
    if (batch.length == 0) {
        batch = 'NONE';
    }

    if (sex.length == 0) {
        sex = 'NONE';
    }

    if (today.checked != true) {
        if (start_date.length == 0) {
            start_date = 'NONE';
        }

        if (end_date.length == 0) {
            end_date = 'NONE';
        }
        
        var start_end = [start_date, end_date];

        let filter_list = [name, sex, batch, start_end, "NOT"];
        return filter_list
    } else {
        let dateString_today = getTodayFormatted();
        let filter_list = [name, sex, batch, [dateString_today, dateString_today], "TODAY"];
        return filter_list
    };
}

function formatDate(dateString, when) {
    if (dateString != 'NONE') {
        // Split the date and time components (adjust separator based on your format)
        const [datePart, timePart] = dateString.split(" ");
    
        // Parse the date part
        const dateParts = datePart.split("/");
        const year = parseInt(dateParts[2], 10); // Parse year as integer
        const month = parseInt(dateParts[1], 10) - 1; // Adjust month index for zero-based months
        const day = parseInt(dateParts[0], 10);
    
        // Create a Date object
        const date = new Date(year, month, day);
    
        // Get month name (adjust indexing for zero-based months)
        const monthName = date.toLocaleString("default", { month: "short" });
    
        // Get day, ensuring two digits with leading zero if needed
        const formattedDay = day.toString().padStart(2, "0");
    
        // Format the output string
        return `${monthName}. ${formattedDay}, ${year}`;
    } else  {
        if (when == 'start') {
            return "start";
        } else {
            return "end";
        }
         // Or return an alternative value if parsing fails
    }
}

function export_toEmail() {
    let filters = get_filters();
    eel.clean_data2(filters[3][0], filters[3][1], filters[0], filters[2], filters[1])(function(outputList) {
        eel.create_csv(outputList, filters)(function(){
        })
    
    })
}

function load_graphs() {
    let filters = get_filters();
    eel.clean_data_registered(filters[0], filters[2], filters[1])(function(outputList) {
        load_tableRegistered(outputList);
    });
    eel.clean_data2(filters[3][0], filters[3][1], filters[0], filters[2], filters[1])(function(outputList) {
        load_tableAttendance(outputList);

        eel.visitsVStime(outputList)(function(lineOutput) { // outputs a two-element list
            data = {
                labels: lineOutput[0], 
                datasets: [{
                    label: false, 
                    data: lineOutput[1],
                    backgroundColor: 'rgba(255, 99, 132)',
                    borderColor: 'rgba(255, 99, 132)', 
                }],
            }
            linechart(data); // creates the line chart with the data specified
            document.getElementById('avg_visits').innerHTML = lineOutput[3];
            document.getElementById('total_visits').innerHTML = lineOutput[4];
            
        });
        eel.visitsVSbatch(outputList)(function(barOutput) { // outputs a two-element list
            data = {
                labels: barOutput[0], 
                datasets: [{
                    label: false, 
                    data: barOutput[1],
                    backgroundColor: 'rgba(255, 99, 132)', 
                    borderColor: 'rgba(255, 99, 132)', 
                }],
            }
            barchart(data); // creates the bar chart with the data specified
        });
        eel.rank_students(outputList)(function(barOutput) { // outputs a two-element list
            data = {
                labels: barOutput[0], 
                datasets: [{
                    label: false, 
                    data: barOutput[1],
                    backgroundColor: 'rgba(255, 99, 132)', 
                    borderColor: 'rgba(255, 99, 132)', 
                }],
            }
            barchart2(data); // creates the bar chart with the data specified
        });
        eel.average_time(outputList)(function(averageOutput) {
            let avg_time_container = document.getElementById('avg_hrs');
            avg_time_container.innerHTML = averageOutput + "hrs"
        });

        eel.gad_stats2(outputList)(function(gadOutput) {
            let female_stat = document.getElementById('FemalePercentage');
            let not_female_stat = document.getElementById('MalePercentage');
            let total_num = document.getElementById('total_num');
            let date = document.getElementById('date');
            female_stat.innerHTML = gadOutput[0];
            not_female_stat.innerHTML = gadOutput[1];
            total_num.innerHTML = gadOutput[2];
            
            if (filters[4] == 'TODAY') {
                date.innerHTML = "Today";
            } else {
                date.innerHTML = `from ${filters[3][0]} to ${filters[3][1]}`
            }
            
        });
    });
    
}

function display_popup() {
    let pop_up = document.querySelector('.export_container');
    let everything = document.querySelector('.everything_dashboard');
    pop_up.style.display = 'block';
    everything.style['pointer-events']= 'none';
}

function close_popup() {
    let pop_up = document.querySelector('.export_container');
    let everything = document.querySelector('.everything_dashboard');
    pop_up.style.display = 'none';
    everything.style['pointer-events']= 'auto';
}

function export_report(receiver) {
    eel.create_report(receiver);
}

function start_export() {
    var receiver = document.querySelector('#export_email').value;
    var list = [receiver];
    export_report(list);
    close_popup();
}
function start_load_table() {
    const theTable = document.querySelector('.theToday_table');
    eel.convert_htmlTable_today()(function(table_contents) {
        theTable.innerHTML = table_contents;
        scroll_bottom();
    })
}

function updateClockAndDate() {
    var now = new Date();
    var hours = now.getHours();
    var minutes = now.getMinutes();
    var ampm = hours >= 12 ? 'PM' : 'AM';
    var dayOfWeek = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'][now.getDay()];
    var month = ['Jan.', 'Feb.', 'Mar.', 'Apr.', 'May', 'Jun.', 'Jul.', 'Aug.', 'Sep.', 'Oct.', 'Nov.', 'Dec.'][now.getMonth()];

    // Convert hours to 12-hour format
    hours = hours % 12;
    hours = hours ? hours : 12; // Handle midnight (0 hours)

    // Add leading zeros if needed
    hours = hours < 10 ? '0' + hours : hours;
    minutes = minutes < 10 ? '0' + minutes : minutes;

    // Format the time as HH:MM AM/PM
    var timeString = hours + ':' + minutes + ' ' + ampm;

    // Format the date as Month Day, Year DayOfWeek
    var dateString = month + ' ' + now.getDate() + ', ' + now.getFullYear() + ' ' + dayOfWeek;

    // Display the time in the clock div
    document.getElementById('Time').textContent = timeString;

    // Display the date in the Date span
    document.getElementById('Date').textContent = dateString;
}


// Call updateClock function every second to update the time
setInterval(updateClockAndDate, 1000);

// Initial call to update the clock immediately
updateClockAndDate();

function hide_table() {
    const tableDiv = document.querySelector('.table');
    const dashboardDiv = document.querySelector('.dashboard');
    const filters = document.querySelector('.filters');
    const theTable = document.querySelector('.theToday_table');
    const attendanceHistory = document.getElementById('AttendanceHistory');
    const dataSummary = document.getElementById('DataSummary');
    tableDiv.style.display = 'none';
    dashboardDiv.style.display = 'block';
    filters.style.display = 'block';
    theTable.innerHTML = '';
    attendanceHistory.style.fontFamily = 'FuturaBook';
    dataSummary.style.fontFamily = 'FuturaHeavy';
}

function scroll_bottom() {
    var rowCount = document.getElementById('lamesa').rows.length;
    var rows = document.querySelectorAll('#lamesa tr');
    rows[rowCount-1].scrollIntoView({
        behavior: 'smooth',
        block: 'nearest'
    });
}


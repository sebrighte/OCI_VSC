
var tidalStationEventData = [];
var tidalStationHeights = [];

var offset = 0;
var base_offset = 0;
var daylightdelta = 0;
var timeView;

function GetDayLightData() {
    /* $.ajax({
        url: "Home/GetOffsetMinutes",
        async: false,
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: success,
        error: error
    }); */
	
	 //var data ="{"baseOffset":0,"currentOffset":60,"dstOffset":60}";

    function success(data) {
        base_offset = 0;
        offset = 60;
        daylightdelta = 60;

        if (offset == daylightdelta) {
            $("#bstTimeView").prop("checked", true);
            timeChange("BST");
            timeView = "BST";
        }
        else {
            $("#gmtTimeView").prop("checked", true);
            timeChange("GMT");
            timeView = "GMT";
        }
    }

    function error(xhr) {
        alert('Incorrect TimeZone');
    }
}

$('#tidetimes').click(function (e) {
    e.preventDefault(); // restricts scrolling to top of the page when clicked
});

$('#tidalcurve').click(function (e) {
    e.preventDefault();// restricts scrolling to top of the page when clicked
});

$('#moreOption').click(function (e) {
    e.preventDefault();// restricts scrolling to top of the page when clicked

    showHideMoreOptions();

    changeTimeView(timeView);
    return false;
});

$('#backButton').click(function (e) {
    e.preventDefault();
    $('#predictionDasboard').show();
    $('#moreOptionDashboard').addClass('hide');
    resetWarningMessage();
});

$("#bstTimeView").click(function myfunction() {
    $("#spnTimeTxt").text("! This will update all times to BST");
});

$("#gmtTimeView").click(function myfunction() {
    $("#spnTimeTxt").text("! This will update all times to GMT");
});

$('#applyChanges').click(function (e) {
    resetWarningMessage();

    toggleTimeView();

    localStorage.setItem("offset", offset);
    adjustEventData();
    generateTidalTableforDashboard();
    generateTidalCurve();

    // The window width above 991 is considered as desktop and value below it is non-desktops (devices)
    if ($(window).width() >= 992) { $('#backButton').click(); }
});

/*$("#applyChangesCnt").click(function myfunction() {
    //$("#spnTimeTxt").text("! This will update all times to GMT");
    setCookie("country", "england", 30);
    alert("NewList");
});*/

function timeChange(tme) {
    $("#paraTimeTxt").text("Times are shown with " + tme + " adjustments");
    $("#bsttitle").text("Times have been adjusted for " + tme);
    localStorage.setItem("bstitleprint", "Times have been adjusted for " + tme);
}

function resetWarningMessage() {
    $("#spnTimeTxt").text("");
}

function adjustEventData() {
    var tidalStationEventDatacopy = JSON.parse(JSON.stringify(tidalStationEventDataClone))
    tidalStationEventData = adjustTidalTable(tidalStationEventDatacopy);

    var tidalStationHeightscopy = JSON.parse(JSON.stringify(tidalStationHeightsClone))
    tidalStationHeights = adjustTidalChart(tidalStationHeightscopy);
}

function adjustDST(dt) {
    let temp_dt = dt;
    temp_dt = temp_dt.getTime() + offset * 60000; //transforms minutes in miliseconds.

    return new Date(temp_dt);
}

function adjustTidalTable(tsdata) {
    $.each(tsdata, function (i, t) {

        if (t.dateTime != null && t.dateTime != "") {

            var tidedatetime = adjustDST(toISODateFormat(t.dateTime));
            t.dateTime = toISOStringFormat(tidedatetime);

            if (new Date(t.dateTime).toDateString() != new Date(t.date).toDateString()) {
                t.date = toISOStringFormat(tidedatetime, true);
            }
        }
    });

    return tsdata;
}


function adjustTidalChart(tsdata) {
    $.each(tsdata, function (i, t) {

        if (t.dateTime != null && t.dateTime != "") {

            var tidedatetime = adjustDST(toISODateFormat(t.dateTime));
            t.dateTime = toISOStringFormat(tidedatetime);
        }
    });

    return tsdata;
}

function toISODateFormat(datetime, dateonly = false) {
    datetime = datetime.replace('T', ' ');
    var [date, time] = datetime.split(' ')
    var [year, month, day] = date.split('-')
    var [hour, minute] = time.split(':')



    if (dateonly) {
        return new Date(year, month - 1, day, 0, 0, 0);
    }
    else {
        return new Date(year, month - 1, day, hour, minute, 0);
    }
}

function toISOStringFormat(dt, dateonly = false) {
    var yr = dt.getFullYear();
    var mnth = dt.getMonth() + 1;
    var day = dt.getDate();
    var hrs = dt.getHours();
    var mins = dt.getMinutes();
    var secs = dt.getSeconds();

    if (mnth < 10) { mnth = "0" + mnth; }
    if (day < 10) { day = "0" + day; }

    if (hrs < 10) { hrs = "0" + hrs; }
    if (mins < 10) { mins = "0" + mins; }
    if (secs < 10) { secs = "0" + secs; }

    if (dateonly) {
        return yr + "-" + mnth + "-" + day + " 00:00:00";
    }
    else {
        return yr + "-" + mnth + "-" + day + " " + hrs + ":" + mins + ":" + secs;
    }
}

function showHideMoreOptions() {
    if ($(window).width() >= 992) {
        $('#predictionDasboard').hide();
        $('#moreOptionDashboard').removeClass('hide');
    }
    else {
        if ($('#moreOptionDashboard')[0].className.indexOf('hide') == -1) {
            $('#moreOptionDashboard').addClass('hide');
            $('#moreOption').find($(".fas"))
                .removeClass('fa-angle-up')
                .addClass('fa-angle-down');
        }
        else {
            $('#moreOptionDashboard').removeClass('hide');
            $('#moreOption').find($(".fas"))
                .removeClass('fa-angle-down')
                .addClass('fa-angle-up');
        }
    }
}

function toggleTimeView() {
    if ($("#bstTimeView").prop('checked')) {
        offset = daylightdelta;
        timeChange("BST");
        timeView = "BST";
    }
    else if ($("#gmtTimeView").prop('checked')) {
        offset = base_offset;
        timeChange("GMT");
        timeView = "GMT";
    }
}

function changeTimeView(tm) {
    if (tm === "BST") {
        $("#bstTimeView").prop("checked", true);
    }
    else {
        $("#gmtTimeView").prop("checked", true);
    }
}

$('#btnExport').click(function (e) {
    localStorage.setItem("locationName", document.getElementById('locationName').innerHTML);
});


$("input[name='exportTideTimes']").change(function () {
    if ($(this).val() == 'one') {
        localStorage.setItem("exportoption", "onedayoption");
    } else if ($(this).val() == 'seven') {
        localStorage.setItem("exportoption", "sevendayoption");
    }
});





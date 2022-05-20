
var LowWater = 1;  // The value of Low Water from dbase is "1".
var HighWater = 0; // The value of Low Water from dbase is "0".
var columnCount = 0;

var newMoon = 1; // The value of New Moon from dbase is "1".
var firstQuarter = 2; // The value of First Quarter from dbase is "2".
var fullMoon = 3; // The value of Low Full Moon dbase is "3".
var lastQuarter = 4; // The value of Last Quarter from dbase is "4".

var lunarPhases = {};
lunarPhases[newMoon] = { src: "/images/new-moon.svg", tooltip: "New moon on this day" };
lunarPhases[firstQuarter] = { src: "/images/first-quarter.svg", tooltip: "First quarter on this day" };
lunarPhases[fullMoon] = { src: "/images/full-moon.svg", tooltip: "Full moon on this day" };
lunarPhases[lastQuarter] = { src: "/images/last-quarter.svg", tooltip: "Last quarter on this day" };

function generateTidalTable(tid) {

    var url = 'https://api.weatherapi.com/v1/forecast.json?key=4ad45c22c74941e5ba4224518212409&days=3&aqi=no&alerts=no&q=';

    if(station != undefined)
    {
        var weatherData = (isLocal) ? fetchData('data/weather.json') : fetchData(url + station[0].geometry.coordinates[1] + ',' + station[0].geometry.coordinates[0]);

        var tid2 = ('#weather-table');
        $(tid2).empty();

        weatherData.forecast.forecastday.forEach(d => 
        {
            var weatherInfo = '<img src=' + d.day.condition.icon + '></img><br/>Wind: ' + d.hour[12].wind_dir + '<br/>' + d.hour[12].wind_mph  + ' (' + d.hour[12].gust_mph + ') mph';
            $(tid2).append('<div class=" col dashboard-container-light-grey">' + weatherInfo + '</div>');
        });

        weatherData.forecast.forecastday.forEach(d => 
            {
                var weatherInfo = '<img src=' + d.day.condition.icon + '></img><br/>Wind: ' + d.hour[12].wind_dir + '<br/>' + d.hour[12].wind_mph  + ' (' + d.hour[12].gust_mph + ') mph';
                $(tid2).append('<div class=" col dashboard-container-light-grey">' + weatherInfo + '</div>');
            });

        //for (let i = 7 - weatherData.forecast.forecastday.length; i < 8; i++) {
            $(tid2).append('<div class="col  dashboard-container-light-grey"><br/><a href="https://www.weatherapi.com/" target="_blank">To view please upgrade API plan</a><br/></div>');
        //}
    }
    
    var oneDayView = false;
    var addLastTide = false;
    var lastTide;

    var lunar_data = lunarPhaseData;
    var raw_data = tidalStationEventData;

    if (startDate == endDate) {
        oneDayView = true;
    }

    var tidal_sdate = Date.parse(startDate);
    var tidal_edate = Date.parse(endDate);

    var data = raw_data.filter(d => {
        var tdate = Date.parse(d.date.substr(0, 10));
        return (tidal_sdate <= tdate && tdate <= tidal_edate);
    });

    var firstTide = HighWater;

    if (data.length > 0) {
        firstTide = data[0].eventType;
        lastTide = data[data.length - 1].eventType;
    }

    var tideSeries = [];

    if (firstTide == LowWater) {
        tideSeries = [
            { key: LowWater, value: '<p> Low </p><p> Tide</p>' },
            { key: HighWater, value: '<p > High </p><p> Tide </p>' }
        ];
    }
    else {
        tideSeries = [
            { key: HighWater, value: '<p> High </p><p> Tide </p>' },
            { key: LowWater, value: '<p> Low </p><p> Tide</p>' }
        ];
    }

    if (oneDayView) {
        var nextDayTide;

        var next_sdate = new Date(tidal_sdate).setMinutes(new Date(tidal_sdate).getMinutes() + 1440) //adding one day in minutes

        var nextDayData = raw_data.filter(z => {
            var tdate = Date.parse(z.date.substr(0, 10));
            return (next_sdate <= tdate && tdate <= next_sdate);
        });

        if (nextDayData.length > 0) {
            nextDayTide = nextDayData[0].eventType;
        }

        if (nextDayTide == lastTide) {
            addLastTide = true;

            if (lastTide == LowWater) {
                lastTide = HighWater;
            }
            else {
                lastTide = LowWater;
            }
        }
    }

    let unique = [...new Set(data.map(item => toISODateFormat(item.date).toLocaleDateString("en-GB")))];

    var result = [];

    result = adjustAlternateTides(data, /*filtered data based on date*/
        firstTide /*to add extra count in the respective tide if the firsttide is different from the first tide of a tide in multiple day view*/);

    createTidalColumns(unique, /*distinct dates*/
        result, /*tides in each date*/
        tideSeries, /*series of tide depending on first tide*/
        addLastTide, /*flag to add last tide for adjusting with the first tide of the next day only for one day view*/
        lastTide, /*name of the last tide*/
        tid /*table name*/); 

    var d = 0;
    var delLastCol = true;

    for (let z in unique) {
        $(tid + ' tbody').append('<tr></tr>')

        for (var j = 0; j < columnCount; j++) {

            if (data[d] != undefined) {
                var date = toISODateFormat(data[d].date).toLocaleDateString("en-GB");
            }
            else {
                date = undefined;
            }

            if (j == 0) {
                var lunar;
                var sdate;

                lunar = createLunarIcon(lunar_data, date);

                sdate = createDateColumn(data[d].dateTime, date, tid);

                $(tid + ' tbody tr').last().append('<th class="headcol">' + sdate + '  ' + lunar + '</th>');

            }

            if (date != undefined && date == unique[z]) {
                var type = data[d]["eventType"];

                var hhmm = "-";
                if (data[d]["dateTime"] != null && data[d]["dateTime"] != "") {
                    var hh = toISODateFormat(data[d]["dateTime"]).getHours();
                    var mm = toISODateFormat(data[d]["dateTime"]).getMinutes();

                    if (hh < 10) { hh = "0" + hh; }
                    if (mm < 10) { mm = "0" + mm; }

                    hhmm = hh + ':' + mm;
                }

                var highLowTide;
                if (type === 0) {
                    highLowTide = "High";
                } else {
                    highLowTide = "Low";
                }
                if ((j % 2 == 0 && firstTide == type) ||
                    (j % 2 != 0 && firstTide != type)) {

                    var height = data[d].height == null || data[d].height == "" ? "-" : roundOffHeight(data[d].height) + "m";

                    if (height == '-' && hhmm == "-") {
                        $(tid + ' tbody tr').last().append('<td> - </td>');
                    }
                    else {
                        $(tid + ' tbody tr').last().append('<td> <span aria-hidden=true> <p class="data-time">' + hhmm + '</p>' +
                            ' <p class="data-height">' + height + '</p></span><span class="sr-only">' + highLowTide + ' Tide of ' + height.slice(0, -1) + ' meters, at ' + hhmm + '. </span></td >');
                    }
                    d++;

                    if (j == (columnCount - 1)) {
                        delLastCol = false;
                    }
                }
                else {

                    $(tid + ' tbody tr').last().append('<td> - </td>');
                }
            }
            else {
                $(tid + ' tbody tr').last().append('<td> - </td>');
            }

        }
    }

    var rowcnt = $(tid)[0].rows.length;

    if (rowcnt == 2) { /* header + 1 row */
        $(tid + " td:nth-child(even)").css("background-color", "#eef3f4");
    }

    $('.lunar').mouseover(function () {
        $('#lunar-title').text(this.alt);
    });

    $('.lunar').mouseout(function () {
        $('#lunar-title').text('');
    });
}

function adjustAlternateTides(data,ft) {
    var lcnt = 0, hcnt = 0;
    var rslt = [];

   data.forEach(function (a) {
        var dt = toISODateFormat(a.date).toLocaleDateString("en-GB");
        var key = dt;
        if (!this[key]) {
            this[key] = { HighWater: 0, LowWater: 0 };
            rslt[dt] = this[key];

            if (a.eventType != ft) { // If the tide of the first entry in any record is different from the firsttide then add it. 
                if (ft == LowWater) {
                    this[key].LowWater += 1;
                }
                else if (ft == HighWater) {
                    this[key].HighWater += 1;
                }
            }
        }

        if (a.eventType == HighWater) {
            this[key].HighWater += 1;
            hcnt += 1;
            lcnt = 0;

            if (hcnt > 1) {
                this[key].LowWater += 1; // adding the count of Low Water if there are subsequent High Water
            }
        }
        else if (a.eventType == LowWater) {
            this[key].LowWater += 1;
            lcnt += 1;
            hcnt = 0;

            if (lcnt > 1) {
                this[key].HighWater += 1; // adding the count of Low Water if there are subsequent High Water
            }
        }

    }, Object.create(null))

    return rslt;
}

function createTidalColumns(unique, rlt, ts, alt, lt, tid) {
    
    $(tid + ' thead tr').empty();
    $(tid + ' tbody').empty();
    $(tid + ' thead tr').append('<td class="headcol"></td>');

    var count = 0, hw, lw;
    columnCount = 0;

    for (let i in unique) {
        hw = rlt[unique[i]]['HighWater'];
        lw = rlt[unique[i]]['LowWater'];

        count = hw + lw;
        if (columnCount < count) {
            columnCount = count;
        }
    }

    for (var c = 0; c < columnCount; c++) {
        var columnName;

        if (c % 2 == 0) {
            columnName = ts[0].value;
        }
        else {
            columnName = ts[1].value;
        }

        $(tid + ' thead tr').append('<td aria-hidden=true class="col-header">' + columnName + '</td>');
    }

    if (alt) {
        columnCount += 1;
        var lastColumnName = ts.find(item => item.key == lt).value;
        $(tid + ' thead tr').append('<td aria-hidden=true  class="col-header">' + lastColumnName + '</td>');
    }

}

function createLunarIcon(ldata, dt) {
    var lunar_date;
    var lunar_phase;

    for (let l in ldata) {
        lunar_date = toISODateFormat(ldata[l].dateTime).toLocaleDateString("en-GB")

        if (lunar_date == dt) {
            lunar_phase = lunarPhases[ldata[l].lunarPhaseType];

            localStorage.setItem("lunarphasesrc", lunar_phase.src);
            return '<div class="lunar-icon"> <img class="lunar" src=' + lunar_phase.src + ' alt="' + lunar_phase.tooltip + '" ></div>';
        }
    }

    return "";
}

function createDateColumn(dtime, dt, tid) {
    var today = new Date().toLocaleDateString("en-GB")

    if (today == dt) {
        if (tid == "#tidal-table-print") {

            //[0] - Weekday
            //[1] - Date
            //[2] - Month
            return weekdays(toISODateFormat(dtime).toString().split(' ')[0]) + ' ' +
                toISODateFormat(dtime).toString().split(' ')[2] + ' ' +
                toISODateFormat(dtime).toString().split(' ')[1];
        } else {
            return 'Today';
        }
    }
    else {
            //[0] - Weekday
            //[1] - Date
            //[2] - Month
        return weekdays(toISODateFormat(dtime).toString().split(' ')[0]) + ' ' +
            toISODateFormat(dtime).toString().split(' ')[2] + ' ' +
            toISODateFormat(dtime).toString().split(' ')[1];
    }
}

function expandPanel() {
    // The window width above 991 is considered as desktop and value below it is non-desktops (devices)
    if ($(window).width() > 991) {
        expandFirstContent();
    }
    else {
        expandAllContent();
    }
}

function generateTidalTableforDashboard() {
    generateTidalTable('#tidal-table');
    expandPanel();
}

function generateTidalTableforPrint() {
    generateTidalTable('#tidal-table-print');
}

function roundOffHeight(height) {
    if (height != null && height != "") {
        var h = height.toFixed(2); // Converts to 2 decimals
        var l = h.toString().slice(-1); // removes the last digit

        if (l > 5) { // if the last digit after the decimal is greater than 5 
            h = height.toFixed(1).toString();
        }
        else {
            h = h.substring(0, h.length - 1);
        }
        return ("-0.0" ? Math.abs(h).toFixed(1) : h);
    }
}

function weekdays(wd) {
    if (wd === 'Tue') {
        return 'Tues'
    }
    else if (wd === 'Wed') {
        return 'Weds'
    }
    else if (wd === 'Thu') {
        return 'Thurs'
    }
    else {
        return wd;
    }
}

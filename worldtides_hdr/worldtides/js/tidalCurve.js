//Copyright © 2014-2021 Chart.js contributors

//Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
//documentation files(the "Software"), to deal in the Software without restriction, including without 
//limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and / or sell copies of 
//the Software, and to permit persons to whom the Software is furnished to do so, subject to the following 
//conditions:

//The above copyright notice and this permission notice shall be included in all copies or substantial portions 
//of the Software.

//THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED 
//TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.IN NO EVENT SHALL 
//THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF 
//CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS 
//IN THE SOFTWARE.

var lineChart = new Chart();

function generateTidalCurve(chartid = 'chart') {
    if (tidalStationHeights.length != 0) { /*Check for sufficient data*/

        $("#alertSection").addClass("hide");
        $("#tidalcurvegraph").removeClass("hide");
        $("#spnPredictionMessage").removeClass("hide");

        var tidalHeightHour = [];
        var tidalHeightHeight = [];

        var tidal_sdate = Date.parse(startDate);
        var tidal_edate = Date.parse(endDate);

        var filterobject = tidalStationHeights.filter(d => {

            var tdate = Date.parse(d.dateTime.substr(0, 10));  /*To get only date part from DateTime*/
            return (tidal_sdate <= tdate && tdate <= tidal_edate);
        });

        jQuery(filterobject).each(function (i, item) {
            tidalHeightHeight.push(item.height);
        });

        function checkTime(i) {
            if (i < 10) {  /*To format time in 12 hour*/
                i = "0" + i;
            }
            return i;
        }

        tidalHeightHour = $.map(filterobject, function (value, index) {
            return checkTime(toISODateFormat(value.dateTime).getHours()) + ":" + checkTime(toISODateFormat(value.dateTime).getMinutes());
        });

        var curveData = {
            labels: tidalHeightHour,
            datasets: [{
                backgroundColor: "rgba(151,187,205,0.5)",
                pointHoverRadius: 5, /*To adjust Size of points plot on graph when hover */
                pointHoverBackgroundColor: 'red',
                data: tidalHeightHeight,
                fill: {
                    target: 'origin',
                    above: 'rgba(173,216,230,.3)'
                },
                borderColor: 'rgba(135,206,235,1)'
            }]
        }
        var curveplugins = {
            legend: {
                display: false, /*Title of graph*/

            },
            tooltip: {
                callbacks: {
                    title: function () {
                        return;
                    },
                    label: function (tooltipItem) {
                        return "Time : " + tooltipItem.label + " Height : " + roundOffHeight(tooltipItem.raw) + "m";
                    }
                }
            }
        }

        if (startDate === endDate) {
            let chart = document.getElementById(chartid).getContext('2d');

            lineChart.destroy();
            lineChart = new Chart(chart, {
                type: 'line', /*type of chart*/
                data: curveData,
                options: {
                    plugins: curveplugins,

                    elements: { line: { tension: 0.4 }, point: { radius: 3 } }, /*Tension- Shape of line, radius - Size of points plot on graph*/
                    scales: {
                        y: {
                            ticks: {
                                stepSize: 1, /* Interval on x axis */
                                beginAtZero: true
                            }
                        }
                    }
                }
            });
            generateTidalCurveTable(tidalHeightHour, tidalHeightHeight);
        } else {
            $("#tidalcurvetablewrapper").hide();
            var xAxislabelIndex = 0;
            let chart = document.getElementById(chartid).getContext('2d');

            lineChart.destroy(); 

            lineChart = new Chart(chart, {
                type: 'line', /*type of chart*/
                data: curveData,
                options: {
                    plugins: curveplugins,

                    elements: { line: { tension: 0.4 }, point: { radius: 2.5 } }, /*Tension- Shape of line, radius - Size of points plot on graph*/
                    scales: {
                        xAxes: [
                            {
                                id: 'xAxis1',
                                type: "category",
                                ticks: {
                                    callback: function (label) {
                                        return label;
                                    }
                                }
                            },
                        ],
                        y: {
                            ticks: {
                                stepSize: 1, /* Interval on Y axis */
                                beginAtZero: true
                            }
                        },
                        x: {
                            ticks: {
                                color: "#09315B",
                                font: {
                                    size: 16,
                                    family: "Johnston ITC W01 Light",
                                    weight: "bold"
                                },
                                stepSize: 2, /* Interval on x axis */
                                callback: function (value, index, values) {
                                    var labelValue = this.getLabelForValue(index);
                                    if (labelValue == "12:00") {  /*To Disply Date on x axis in 7 day view at 12 PM interval */
                                        xAxislabelIndex += 1;
                                        return xAxislabelsForSevenDayView[xAxislabelIndex - 1];
                                    }
                                }
                            }
                        }
                    }
                }
            });
            xAxislabelIndex = 0;  /*code logic */
        }

    }
    else {
        $("#alertSection").removeClass("hide");
        $("#tidalcurvegraph").addClass("hide");
        $("#spnPredictionMessage").addClass("hide");
    }
}

function SevenDayView() {
    SevenDayOneDayView(true);
    generateTidalTableforDashboard();
    generateTidalCurve();
    gtag('event', 'gtm.click', {  /*GTM event Data*/
        'event_category': '7_day_view',
        'event_label': document.getElementById('locationName').innerHTML
    });
}

function SevenDayOneDayView(sevenDayView) {
    if (sevenDayView) {
        $("#tidetimes").text("Tide times for the next 7 days");
        $("#tidalcurve").text("Tidal curve for the next 7 days");
        $("#sevenday").hide();
        SetSevenDayViewDates();
        ResetDateControl();
        SevenDayTidalCurveView();

    }
    else {
        $("#tidetimes").text("Tide times");
        $("#tidalcurve").text("Tidal curve");
        $("#sevenday").show();
        OneDayTidalCurveView();
    }
}

function SevenDayTidalCurveView() {
    $("#chartWrapper").addClass("chartWrapper");
    $("#chartAreaWrapper").addClass("chartAreaWrapper");
    $("#myChartAxis").show();
}

function OneDayTidalCurveView() {
    $("#chartWrapper").removeClass("chartWrapper");
    $("#chartAreaWrapper").removeClass("chartAreaWrapper");
    $("#myChartAxis").hide();
}

function TidalCurveXAxislabelsForSevenDayView(printPage = false) {
    var i = 0;
    if (!printPage) {
        i = 1;
        xAxislabelsForSevenDayView.push("Today");
    }
    for (i; i < numberOfPredicationDays; i++) {
        const d = new Date();
        d.setDate(d.getUTCDate() + i);
        var week = d.toString().split(' ')[0];
        var month = d.toString().split(' ')[1];
        var dd = d.toString().split(' ')[2];
        xAxislabelsForSevenDayView.push(weekdays(week) + " " + dd + " " + month);
    }
}

function generateTidalCurveTable(hour, height, tid = '#tidalcurvetable') {
    $("#tidalcurvetablewrapper").show();
    $(tid + ' thead tr').empty();
    $(tid + ' tbody').empty();

    $(tid + ' thead tr').append('<th aria-hidden=true class="headcol"> Time </th>');

    for (let i in hour) {
        $(tid + ' thead tr').append('<td> <span aria-hidden=true>' + hour[i] + '</span><span class="sr-only">Tide Time is ' + hour[i] + ' and Height is ' + roundOffHeight(height[i]) + ' metres.</span></td >');
    }

    $(tid + ' tbody').append('<tr aria-hidden=true></tr>')
    $(tid + ' tbody tr').last().append('<th  class="headcol">' + 'Height (m)' + '</th>');

    for (let j in height) {
        $(tid + ' tbody tr').last().append('<td>' + roundOffHeight(height[j]) + 'm' + '</td>');
    }
    $(tid + " td:nth-child(even)").css("background-color", "#eef3f4");
}
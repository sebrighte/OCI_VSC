
$(document).ready(init);

var tidalStationEventDataClone = [];
var tidalStationHeightsClone = [];
var lunarPhaseDataClone = [];
var lunarPhaseData = [];
var tidalStationFooterNote;
var srcStations;
var station;
var portLat;
var portLng;

var startDate;
var endDate;

var highlightMarkers = ["urlMarker", "clickedLocationMarker", "currentLocationMarker", "searchedMarker"];
var placeHolderMsg = "Search by coastal location or port";
var results;
var minZoomLevel = 0;
var intmZoomLevel = 8;
var maxZoomLevel = 14;
var xAxislabelsForSevenDayView = [];
var numberOfPredicationDays = parseInt(document.getElementById('numberOfPredicationDays').value);

var searchStationHeaderMessage = "You have entered a location with no tidal station";
var searchStationMessage = "Please use the map to search and find a tidal station nearest to your specified location";
var currentLocationHeaderMessage = "Unable to identify your current location";
var currentLocationMessage = "Your current location cannot be found. Please try using the map or check your location settings.";

var isLocal = false;

function setCountries() {
    var cookie = getCookie("selectedCountriesTides");
    //alert(cookie);
    setCookie("selectedCountriesTides",prompt("Select countries to display (comma sepeated)",cookie),30);
    var cookie2 = getCookie("selectedCountriesTides");
    if(cookie != cookie2) location.reload();
}

window.onload = function () {
    
    localStorage.setItem("exportoption", "onedayoption");
    $("#map").attr("tabindex", 0);
    $("button.ol-zoom-in:contains('+')").attr("tabindex", 0);
    $("button.ol-zoom-out:contains('−')").attr("tabindex", 0);
    TidalCurveXAxislabelsForSevenDayView();
    OneDayTidalCurveView();
    $('#accessibilitylink').keydown(function (e) {
        if (e.keyCode == 9) { // Key code for Tab.
            $('#admiralitylogo').focus();
            e.preventDefault();
        }
    });
}

  function setCookie(cname, cvalue, exdays) {
    document.cookie = cname + " + =; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    const d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    let expires = "expires="+d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
  }
  
  function getCookie(cname) {
    let name = cname + "=";
    let ca = document.cookie.split(';');
    for(let i = 0; i < ca.length; i++) {
      let c = ca[i];
      while (c.charAt(0) == ' ') {
        c = c.substring(1);
      }
      if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
      }
    }
    return "";
  }

  function fetchData(url, geoJSON = false) {

    strReturn = "";
  
    jQuery.ajax({
      url: url,
      crossDomain: true,
      success: function(data) {
        strReturn = geoJSON? JSON.parse(data): data;
      },
      error: function(err) {
        //strReturn = err.responseText;
      },
      async:false
    });
  
    return strReturn;
  }

  function GetPredictionData(Id) {
	
    //data = JSON.parse(fetchData('/Home/GetTidalPrediction?stationId=' + Id));

    var r = 4;

    try {
        data = JSON.parse(fetchData('/Home/GetTidalPrediction?stationId=' + Id));
    }
    catch(err) {
        data = (fetchData('data/pred.json'));
    }
	
	    tidalStationEventDataClone = data.tidalEventList;
        tidalStationHeightsClone = data.tidalHeightOccurrenceList;
        lunarPhaseData = data.lunarPhaseList;
        tidalStationFooterNote = data.footerNote;

        setFooterNote(tidalStationFooterNote);
        adjustEventData();
		
		function setFooterNote(note) {
        $("#spnFooterNoteMessage").text(note);
    }
}

function GenerateDashboard(stationId, portName) {
    updateURL(stationId, portName);

    GetDayLightData();
    localStorage.setItem("offset", offset);

    GetPredictionData(stationId);

    generateTidalTableforDashboard();
    generateTidalCurve();
}

function init() {

    //setCookie("country", "scotland", 1000);

    var keydown = function (evt) {
        var charCode = (evt.which) ? evt.which : evt.keyCode;
        if (charCode === 187 || charCode === 61) { // Keycode 61 is for key "+" specific to Firefox browser and 187 for other browsers
            map.getView().setZoom(map.getView().getZoom() + 1);
        }
        else if (charCode === 189 || charCode === 173) { // Keycode 173 is for key "-" specific to Firefox browser and 189 for other browsers
            map.getView().setZoom(map.getView().getZoom() - 1);
        }
    };

    $('#map').on('keydown', keydown);

    function setActivePin(markerName, latlong) {
        var iconLayer = new ol.layer.Vector({
            source: new ol.source.Vector(),
            style: activeMarker
        });

        iconLayer.set('name', markerName);
        map.addLayer(iconLayer);

        var marker = new ol.Feature(new ol.geom.Point(latlong));

        iconLayer.getSource().addFeature(marker);
    }

    function showHideDashboard(show) {

        if (show) {

            $(".dashboard").removeClass('hide');


            Array.from(document.querySelectorAll('.map-container')).forEach(function (el) {
                if (el.className.includes("dashboard")) {
                    el.classList.add('col-xl-5');
                    el.classList.add('col-lg-7');
                }
                else {
                    el.classList.add('col-xl-7');
                    el.classList.add('col-lg-5');
                }

                el.classList.remove('col-lg-12');
            });

            // The window width above 991 is considered as desktop and value below it is non-desktops (devices)
            if ($(window).width() < 992) {
                scrollToDashBoard();
            }
           
        }
        else {

            $(".dashboard").addClass(' hide');

            $('.map-container').each(function () {
                if (this.className.includes("dashboard")) {
                    this.classList.remove('col-xl-5');
                    this.classList.remove('col-lg-7');
                }
                else {
                    this.classList.remove('col-xl-7');
                    this.classList.remove('col-lg-5');
                }

                this.classList.add('col-lg-12');
            });


            $("#locationName").text('');
            $("#smlocationName").text('');
        }

        clearBlueMarker();
        map.updateSize();
    }

    function changePlaceholder() {

        // The window width above 991 is considered as desktop and value below it is non-desktops (devices)
        if ($(window).width() < 992) {

            Array.from(document.querySelectorAll('.overlap')).forEach(function (el) {
                el.classList.remove('ol-control');
            });
            $("#currentlocation").removeAttr("title");
            $("#locationName").addClass("hide");

            showHideSMLocation();

            // The window width below is for mobile devices
            if ($(window).width() <= 767) {

                Array.from(document.querySelectorAll('.footer-break')).forEach(function (el) {
                    el.classList.remove('input-group');
                });

                map.getView().animate({
                    //center: [-501251.5726032632, 6954237.505335568],
                    center: [-470588.309823008, 7135445.458637395],
                    zoom: minZoomLevel
                });
            }
            else { // for devices like Tablet and iPad

                map.getView().animate({
                    center: [-552127.8794805913, 7216691.931052772],
                    zoom: minZoomLevel
                });

                Array.from(document.querySelectorAll('.footer-break')).forEach(function (el) {
                    el.classList.add('input-group');
                });
            }
        }
        else {
            $("#currentlocation").attr("title", "Search by Current location");
            $(".sm-locationName").addClass("hide");
            $("#locationName").removeClass("hide");
            $("#map-header").removeClass('hide');

            Array.from(document.querySelectorAll('.overlap')).forEach(function (el) {
                el.classList.add('ol-control');
            });

            Array.from(document.querySelectorAll('.footer-break')).forEach(function (el) {
                el.classList.add('input-group');
            });

            map.getView().animate({
                center: [-751741.674200139, 7508203.515755335],
                zoom: minZoomLevel
            });
        }

        map.updateSize();
    }

    function showHideSMLocation() {

        // The window width above 991 is considered as desktop and value below it is non-desktops (devices)
        if ($(window).width() < 992) {
            if ($("#smlocationName").text() != "") {
                $(".sm-locationName").removeClass("hide");
                $("#map-header").addClass(' hide');
            }
            else {
                $(".sm-locationName").addClass("hide");
                $("#map-header").removeClass('hide');
            }
        }

        map.updateSize();
    }

    function clearBlueMarker() {

        var layersToRemove = [];
        map.getLayers().forEach(function (layer) {

            if (layer.get('name') != undefined && $.inArray(layer.get('name'), highlightMarkers) > -1) {
                layersToRemove.push(layer);
            }
        });

        var len = layersToRemove.length;

        for (var i = 0; i < len; i++) {
            map.removeLayer(layersToRemove[i]);
        }
    }

    var activeMarker = new ol.style.Style({
        image: new ol.style.Icon({
            anchor: [0.13, 137],
            scale: [0.35, 0.35],
            anchorXUnits: 'fraction',
            anchorYUnits: 'pixels',
            src: 'images/active-pin.svg',
        }),
    });

    var inactiveMarker = new ol.style.Style({
        image: new ol.style.Icon({
            anchor: [0, 138],
            scale: [0.23, 0.23],
            anchorXUnits: 'fraction',
            anchorYUnits: 'pixels',
            src: 'images/active-pin.svg',
        }),
    });

    ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    
    var cookie  = getCookie("selectedCountriesTides") == "null"? "" : getCookie("selectedCountriesTides");
    portURL = '/Home/GetTidalPorts?countries=' + cookie;

    srcStations = (isLocal) ? fetchData("data/ports.json") : fetchData(portURL, true);

    var source = new ol.source.Vector({
        //url: (isLocal) ? 'data/ukports.json' : portURL,
        url: (isLocal) ? 'data/ports.json' : portURL,
        format: new ol.format.GeoJSON()
    });

    var clusterSource = new ol.source.Cluster({
        distance: 60,
        source: source
    });

    var styleCache = {};
    var styleSizeCache = {};

    var clusters = new ol.layer.Vector({
        source: clusterSource,
        style: function (feature, resolution) {
            var size = feature.get('features').length;
            if (size > 1) {
                var style = styleCache[size];
                if (!style) {
                    style = new ol.style.Style({
                        image: new ol.style.Icon({
                            anchor: [0, 70],
                            scale: [0.23, 0.23],
                            anchorXUnits: 'fraction',
                            anchorYUnits: 'pixels',
                            src: 'images/cluster-pin.svg',
                        }),

                    });

                    styleCache[size] = style;
                }
            } else {
                style = inactiveMarker;
            }

            return style;
        }
    });

    var clusterssize = new ol.layer.Vector({
        source: clusterSource,
        zindex: 100,
        style: function (feature, resolution) {
            var size = feature.get('features').length;
            if (size > 1) {
                var style = styleSizeCache[size];
                if (!style) {
                    style = [new ol.style.Style({
                        text: new ol.style.Text({
                            text: size.toString(),
                            fill: new ol.style.Fill({
                                color: 'white'
                            }),
                            font: '10px Johnston ITC W01 Medium',
                            offsetY: -3,
                            offsetX: 11
                        })
                    })];
                    styleSizeCache[size] = style;
                }
            }
            return style;
        }
    });

    var raster = new ol.layer.Tile({
        source: new ol.source.XYZ({
            url: 'https://{a-d}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}.png',
            attributions: [
                '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
                'contributors © <a href="https://carto.com/attributions">CARTO</a>'
            ],
            opaque: true,
        }),
    });

    var attribution = new ol.control.Attribution({
        collapsible: false,
    });

    var interactions = ol.interaction.defaults({ altShiftDragRotate: false, pinchRotate: false, mouseWheelZoom: false });
	var controls = ol.control.defaults({rotate: false});
    var map = new ol.Map({
        layers: [raster, clusters, clusterssize],
        controls: ol.control.defaults({ attribution: false }).extend([attribution]),
        target: 'map',
        view: new ol.View({
    //center: [-178945.31282410398, 7447457.708208833],
            center: [-88660.93080121744, 7430854.828128697],
            zoom: minZoomLevel,
            maxZoom: maxZoomLevel,
            minZoom: minZoomLevel,
            interactions: interactions,
			controls: controls,
        }),
        logo: false
    });

    changePlaceholder();

    var extent = ol.proj.transformExtent(new ol.source.Vector({
        features: new ol.format.GeoJSON().readFeatures(srcStations)
      }).getExtent(), 'EPSG:4326', 'EPSG:3857');

      map.getView().fit(extent, map.getSize()); 

      map.getView().setZoom(map.getView().getZoom() - 1);

    var locationId = getParameterByName(qstringPORT);

    if (locationId != null) {

        //var urldata;

        //$.getJSON('Home/GetStations', function (data) {
            //urldata = data.features.filter(d => d.properties.Id == locationId.toUpperCase());
			
			var urldata = srcStations.features.filter(d => d.properties.Id == locationId.toUpperCase());

            if (urldata.length > 0) {

                station = urldata;

                var navigate = ol.proj.fromLonLat([urldata[0].geometry.coordinates[0], urldata[0].geometry.coordinates[1]])

                showHideDashboard(true);

				//var locationName = feat.get('features')[0].values_.Name + " (" + feat.get('features')[0].values_.Id + "), " +
                        //feat.get('features')[0].values_.Country;
                //var locationName = urldata[0].properties.Name + ", " + urldata[0].properties.Country
				var locationName = urldata[0].properties.Name + " (" + urldata[0].properties.Id + "), " + urldata[0].properties.Country

                $("#locationName").text(locationName);
                $("#smlocationName").text(locationName);

                setActivePin('urlMarker', navigate);

                showHideSMLocation();
                GenerateDashboard(urldata[0].properties.Id, urldata[0].properties.Name);
                localStorage.setItem("stationid", urldata[0].properties.Id);
                map.getView().animate({
                    center: navigate,
                    zoom: maxZoomLevel
                });
            }
        //});
    }

    map.on('pointermove', function (evt) {
        map.getViewport().style.cursor = '';
        map.forEachFeatureAtPixel(evt.pixel,
            function (feat, layer) {

                if (feat.get('features') == undefined) {
                    return false;
                }

                var clusterSize = feat.get('features').length;
                if (clusterSize >= 1) {
                    map.getViewport().style.cursor = 'pointer';
                }
				//if (clusterSize == 1) {
				//	var lonlat = ol.proj.transform(evt.coordinate, 'EPSG:3857', 'EPSG:4326');
			     //   var lon = lonlat[0];
				 //   var lat = lonlat[1];
				//	var locationName = feat.get('features')[0].values_.Name + " (" + feat.get('features')[0].values_.Id + "), " +
                 //       feat.get('features')[0].values_.Country + " " + lonlat;
						
					
					//var weatherInfo = getSyncData("https://api.weatherapi.com/v1/current.json?key=4ad45c22c74941e5ba4224518212409&q=" + lat + "," + lon + "&aqi=no");
					//var condition = weatherInfo.get('condition');
					
					//var status = weatherInfo.location.name;
					/* weatherInfo.current.gust_mph
					weatherInfo.current.temp_c
					weatherInfo.current.wind_dir
					weatherInfo.current.wind_mph */
					
					//features.forEach( clusterFeature => {
                     //   valuesToShow.push(clusterFeature.get('VALUE_TO_SHOW'));
                    //});
                    //container.style.display="block"; 
					//var coordinate = evt.coordinate; content.innerHTML = name; 
					//overlay.setPosition(coordinate);
					
					//console.log(weatherInfo);
                //}
            });
    });

    map.on('click', function (evt) {
        HideValidationPopUp();
        ResetSearchBox();

        var feature = map.forEachFeatureAtPixel(evt.pixel,
            function (feat, layer) {

                if (feat.get('features') == undefined) {
                    return false;
                }

                var clusterSize = feat.get('features').length;
                var zoomLevel;
                var centerCoords;

                //Cluster size with value 1 is a pin and value greater than 1 are clusters
                if (clusterSize == 1) {

                    showHideDashboard(true);
                    $('#predictionDasboard').show();
                    $('#moreOptionDashboard').addClass('hide');

                    var longlat = feat.get('features')[0].values_.geometry.flatCoordinates;

                    station = srcStations.features.filter(d => d.properties.Id == feat.get('features')[0].values_.Id);

                    var locationName = feat.get('features')[0].values_.Name + " (" + feat.get('features')[0].values_.Id + "), " +
                        feat.get('features')[0].values_.Country;
					//$("#portLat").text(portLat);
					//$("#portLng").text(portLng);
                    $("#locationName").text(locationName);
                    $("#smlocationName").text(locationName);
                    setActivePin('clickedLocationMarker', longlat);

                    //zoomLevel = maxZoomLevel;
                    centerCoords = longlat;
                    GenerateDashboard(feat.get('features')[0].values_.Id, feat.get('features')[0].values_.Name);
                    localStorage.setItem("stationid", feat.get('features')[0].values_.Id);
                }
                else {

                    var currentZoomLevel = map.getView().getZoom();

                    //if (currentZoomLevel >= intmZoomLevel && currentZoomLevel < maxZoomLevel) {
                    //    zoomLevel = maxZoomLevel;
                    //}
                    //else {
                    //    zoomLevel = intmZoomLevel;
                    //}
                    zoomLevel= currentZoomLevel + 2;

                    centerCoords = evt.coordinate;
                }

                map.getView().animate({
                    center: centerCoords,
                    zoom: zoomLevel
                });

                showHideSMLocation();

                return true;
            });

        if (feature == undefined) {

            showHideSMLocation();
        }
    });

    /*---------Autocomplete JS----------------*/
    $("#location").autocomplete({
        minLength: 0,
        delay: 0,
        source: function (request, response) {
            if (request.term.trim().length >= 2) {
				
                results = $.map(srcStations.features, function (item, index) {
					
					request.term = request.term.trim();

					if (item.properties.Name.substr(0, request.term.length).toLowerCase() === request.term.toLowerCase() ||
						item.properties.Name.toLowerCase().includes(" " + request.term.toLowerCase()) ||
						item.properties.Name.toLowerCase().includes("(" + request.term.toLowerCase())) {

						HideValidationPopUp();

						return {
							label: item.properties.Name,
							value: item.properties.Name,
							stationId: item.properties.Id,

							location: item.properties.Name,
							country: item.properties.Country,
							xaxis: item.geometry.coordinates[0],
							yaxis: item.geometry.coordinates[1],
						};
					}
				});

				results = results.sort(SortTidalStation).slice(0, 10);
				response(results);
            }
            else {
                HideValidationPopUp();
                $(".ui-menu-item").hide();
            }
        },
        response: function (event, ui) {
            if (ui.content.length === 0) {

                showHideDashboard(false);

                ShowValidationPopUp(searchStationHeaderMessage, searchStationMessage);

                showHideSMLocation();

                gtag('event', 'gtm.click', {
                    'event_category': 'station_search',
                    'event_label': 'Invalid search'
                });
            }
        },
        messages: {
            noResults: '',
            results: function () { '' }
        },
        select: function (event, ui) {
            document.activeElement.blur();
            event.preventDefault();
            this.value = ui.item.location;
            $(this).next().val(ui.item.location);
            var coords = [ui.item.xaxis, ui.item.yaxis];
            var navigate = ol.proj.fromLonLat([coords[0], coords[1]])

            showHideDashboard(true);
            $('#predictionDasboard').show();
            $('#moreOptionDashboard').addClass('hide');

            station = srcStations.features.filter(d => d.properties.Id == ui.item.stationId);

            var locationName = ui.item.location + " (" + ui.item.stationId + "), " + ui.item.country
			//var locationName = feat.get('features')[0].values_.Name + " (" + feat.get('features')[0].values_.Id + "), " +
                        //feat.get('features')[0].values_.Country;

            $("#locationName").text(locationName);
            $("#smlocationName").text(locationName);
            setActivePin('searchedMarker', navigate);

            map.getView().animate({
                center: navigate,
                zoom: maxZoomLevel
            });

            showHideSMLocation();
            GenerateDashboard(ui.item.stationId, ui.item.location);
            localStorage.setItem("stationid", ui.item.stationId);
            gtag('event', 'gtm.click', {
                'event_category': 'station_search',
                'event_label': locationName
            });
        }
    })
    /*---------Autocomplete JS----------------*/

    $("#searchstation").keyup(function (event) {
        if (event.keyCode === 13) { //Key code for Enter
            $("#searchstation").click();
        }
    });

    $("#searchstation").click(function () {

        var searchTidalStationName = $("#location").val().trim();
        var tempResult = results;

        var found_names = $.grep(tempResult, function (v) {
            return v.location.toLowerCase() === searchTidalStationName.toLowerCase();
        });

        if (found_names.length == 0) {

            showHideDashboard(false);

            ShowValidationPopUp(searchStationHeaderMessage, searchStationMessage);
            gtag('event', 'gtm.click', {
                'event_category': 'station_search',
                'event_label': 'Invalid search'
            });
        }
        else {

            var navigate = ol.proj.fromLonLat([found_names[0].xaxis, found_names[0].yaxis])

            showHideDashboard(true);

            station = srcStations.features.filter(d => d.properties.Id == found_names[0].stationId);

            var locationName = found_names[0].location + ", " + found_names[0].country
            $("#locationName").text(locationName);
            $("#smlocationName").text(locationName);
            setActivePin('searchedMarker', navigate);

            map.getView().animate({
                center: navigate,
                zoom: maxZoomLevel
            });

            showHideSMLocation();
            GenerateDashboard(found_names[0].stationId, found_names[0].location);
            localStorage.setItem("stationid", found_names[0].stationId);
            gtag('event', 'gtm.click', {
                'event_category': 'station_search',
                'event_label': locationName
            });
        }
    });


    $("#currentlocation").keyup(function (event) {
        if (event.keyCode === 13) { // Keycode for Enter
            $("#currentlocation").click();
        }
    });
    

    $('.find-current-location').click(function () {

        navigator.geolocation.getCurrentPosition(onSuccess, onError)

        function onSuccess(position) {
            HideValidationPopUp();

            var navigate = ol.proj.fromLonLat([position.coords.longitude, position.coords.latitude])

            map.getView().animate({
                center: navigate,
                zoom: maxZoomLevel
            });

            showHideDashboard(false);
        }
        function onError(error) {
            showHideDashboard(false);

            ShowValidationPopUp(currentLocationHeaderMessage, currentLocationMessage);
        }
    });
}

$("#location").focus(function () {
    $(this).attr('placeholder', '');

});

$("#location").focusout(function () {
    $(this).attr('placeholder', placeHolderMsg)
});

function SortTidalStation(a, b) {
    if (a.label < b.label) {
        return -1;
    }
    if (a.label > b.label) {
        return 1;
    }
    return 0;
}

function ResetSearchBox() {
    $("#location").val('');
}

var selectedDashboardDate = new Date();

SetOneDayViewDates();

$(".date-control-row div").click(function (e) {
    getOneDayData(e);
});

$(".date-control-row div").keydown(function (e) {
    var keycode = (e.keyCode ? e.keyCode : e.which);

    if (keycode === 13 || keycode === 32) { // Keycode "13" is for Enter and "32" is for Space bar
        getOneDayData(e);
    }
});

function getOneDayData(e) {
    SevenDayOneDayView(false);

    var dateID = e.target.id;

    var AddDays = parseInt(dateID.substring(3));

    var today = new Date();
    var tomorrow = new Date(today);
    tomorrow.setDate(tomorrow.getDate() + AddDays);
    
    startDate = tomorrow.toISOString().slice(0, 10);//e.currentTarget.id;
    endDate = tomorrow.toISOString().slice(0, 10);//e.currentTarget.id;

    generateTidalTableforDashboard();
    generateTidalCurve();

    ResetDateControl();
    $(e.currentTarget).addClass("dashboard-container-dark-grey");
    $(e.currentTarget).addClass("date-control-highlighted");
}

function ResetDateControl() {
    $('.col').each(function (i, obj) {
        $(this).removeClass('dashboard-container-dark-grey');
        $(this).addClass('dashboard-container-light-grey');
        $(this).removeClass('date-control-highlighted');
    });
}

function SetOneDayViewDates() {
    startDate = FormatStartEndDate(new Date());
    endDate = startDate;
}

function SetSevenDayViewDates() {
    startDate = FormatStartEndDate(new Date());
    const d = new Date();
    d.setDate(d.getDate() + (numberOfPredicationDays - 1));
    endDate = FormatStartEndDate(d);
}

function FormatStartEndDate(date) {
    var dd = String(date.getUTCDate()).padStart(2, '0');
    var mm = String(date.getUTCMonth() + 1).padStart(2, '0');
    var yyyy = date.getUTCFullYear();
    return yyyy + "-" + mm + "-" + dd;
}

function scrollToDashBoard() {
    window.scroll({
        top: 500, // scrolls up to value 500
        behavior: 'smooth'  
    });
}


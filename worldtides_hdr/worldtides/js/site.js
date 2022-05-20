
var qstringPORT = 'PortID'; // Name of Query string

function expandFirstContent() {
    var firstcont = false;
    var inActivecnt = 0;
    const colls = document.getElementsByClassName('collapsible');
    for (const coll of colls) {
        if (coll.className.indexOf('active') == -1) {
            inActivecnt += 1
        }
    }

    if (colls.length == inActivecnt) {
        firstcont = true;
    }

    if (firstcont) {
        if (colls[0].className.indexOf('active') == -1) {
            colls[0].click();
        }
    }
}

function toggleContent(content, coll) {

    if (content.style.display === "block") {
        content.style.display = "none";
        coll.setAttribute('aria-expanded', 'false'); // for accessibility, will read as "Expanded" in screen reader.
    } else {
        content.style.display = "block";
        coll.setAttribute('aria-expanded', 'true'); // for accessibility, will read as "Collapsed" in screen reader.
    }
}

//expand all closed content
function expandAllContent() {
    const colls = document.getElementsByClassName('collapsible');
    for (const coll of colls) {
        if (!coll.classList.contains('active')) {
            coll.classList.add('active');
            toggleContent(coll.nextElementSibling, coll);
        }
    }

    $('#predictionDasboard').show();
    $('#moreOptionDashboard').removeClass('hide');
    $('#backButton').addClass('hide');
    $('#moreOption').find($(".fas")).removeClass('fa-angle-right').addClass('fa-angle-up');
}

const colls = document.getElementsByClassName('collapsible');
for (const coll of colls) {
    coll.addEventListener('click', function () {
        this.classList.toggle('active');
        toggleContent(this.nextElementSibling, coll);
    });
}


function updateURL(portid,portName) {

    if (getParameterByName(qstringPORT)) {
        const params = new URLSearchParams(location.search);

        for (const key of params.keys()) {
            if (qstringPORT.toLowerCase() == key.toLowerCase()) {
                params.set(key, portid);
            }
            break;
        }

        window.history.replaceState({}, '', `${location.pathname}?${params}`);
    }
    else {
        window.history.pushState("", "", window.location.href + "?" + qstringPORT + "=" + portid);
    }
    document.title = "Tide Times " + portName + " | ADMIRALTY EasyTide";
}

function getParameterByName(name, url = new URL(window.location.href)) {
    const params = new URLSearchParams(
        url.search
    );

    const newParams = new URLSearchParams();
    for (const [key, value] of params) {
        newParams.append(key.toLowerCase(), value);
    }

    return newParams.get(name.toLowerCase());
}

const processUrl = "/process";
let mapDiv = document.getElementById("map");
let addressDiv = document.getElementById("address");
let descriptionDiv = document.getElementById("description");

function myMap(lat, long) {
    let center = new google.maps.LatLng(lat, long);
    var mapOptions = {
        center: center,
        zoom: 17,
    };
    var map = new google.maps.Map(mapDiv, mapOptions);
    var marker = new google.maps.Marker({position: center, map: map})
}


let submitForm = (url, data, callback) => {
    addressDiv.textContent = "";
    descriptionDiv.textContent = "";
    let req = new XMLHttpRequest();
    req.open("POST", url);
    req.addEventListener("load", () => {
        if (req.status >= 200 && req.status < 400) {
            callback(req.responseText);
        } else {
            console.error(req.status + " " + req.statusText + " " + url)
        }
    });
    req.addEventListener("error", () => {
        console.error("Network error with url : " + url)
    });
    req.send(data);
};


let searchForm = document.querySelector("form");
searchForm.addEventListener("submit", (e) => {
    mapDiv.style.height = '0';
    let data = new FormData(searchForm);
    console.log(searchForm);
    submitForm(processUrl, data, (response) => {
        let receivedData = JSON.parse(response);
        let googleData = receivedData.results.google_maps_api_results;
        let wikiData = receivedData.results.wikipedia_api_results;
        myMap(googleData.location.lat, googleData.location.lng);
        mapDiv.style.height = '400px';
        addressDiv.textContent = googleData.formatted_address;
        descriptionDiv.innerHTML = wikiData.description;
    });
    e.preventDefault();
});


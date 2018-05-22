const processUrl = "/process";
let searchBtn = document.getElementById("search-btn");
let mapDiv = document.getElementById("map");
let dialogDiv = document.getElementById("dialog");
let addressDiv = document.getElementById("address");
let descriptionDiv = document.getElementById("description");
let moreInfoLink = document.getElementById("more-info");
let loaderDiv = document.getElementsByClassName("loader")[0];
let loaderText = loaderDiv.getElementsByClassName("loader-text")[0];
let initialLoaderText = loaderText.innerHTML;

let colors = ['#c62e1a', '#13b5db', 'yellow'];
let loadInterval = null;
let loader = (loading) => {
        let i = 0;
        if (loading === true) {
            loaderDiv.classList.remove("hide-me");
            loadInterval = setInterval(() => {
                dialogDiv.style.backgroundColor = colors[i];
                if (i < colors.length) {
                    i++;
                    loaderText.innerHTML += "...";
                } else {
                    i = 0;
                }
            }, 1000)
        } else {
            clearInterval(loadInterval);
            loaderDiv.classList.add("hide-me");
            dialogDiv.style.backgroundColor = 'rgba(19, 181, 219, .5)';
            loaderText.innerHTML = initialLoaderText;
        }
    }
;


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
    searchBtn.disabled = true;
    addressDiv.textContent = "";
    descriptionDiv.textContent = "";
    moreInfoLink.textContent = "";
    let req = new XMLHttpRequest();
    req.open("POST", url);
    req.addEventListener("load", () => {
        if (req.status >= 200 && req.status < 400) {
            callback(req.responseText);
            loader(false);
            searchBtn.disabled = false;
        } else {
            console.error(req.status + " " + req.statusText + " " + url)
            loader(false);
            searchBtn.disabled = false;
        }
    });
    req.addEventListener("error", () => {
        console.error("Network error with url : " + url)
    });
    req.send(data);
};


let searchForm = document.querySelector("form");
searchForm.addEventListener("submit", (e) => {
    loader(true);
    mapDiv.style.height = '0';
    let data = new FormData(searchForm);
    submitForm(processUrl, data, (response) => {
        let receivedData = JSON.parse(response);
        let googleData = receivedData.results.google_maps_api_results;
        let wikiData = receivedData.results.wikipedia_api_results;
        myMap(googleData.location.lat, googleData.location.lng);
        mapDiv.style.height = '400px';
        addressDiv.textContent = googleData.formatted_address;
        descriptionDiv.innerHTML = wikiData.description;
        moreInfoLink.href = wikiData.url;
        moreInfoLink.innerText = "En savoir plus."
    });
    e.preventDefault();
});


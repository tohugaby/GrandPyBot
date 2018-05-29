const sentenceUrl = "/sentences";
const processUrl = "/process";
let searchForm = document.querySelector("form");
let searchBtn = document.getElementById("search-btn");
let eraseBtn = document.getElementById("erase-btn");
let dialogDiv = document.getElementById("dialog");
let colors = ['#c62e1a', '#13b5db', 'yellow'];
let loadInterval = null;


let loaderTemplate = `<div class="loader-image">
                        <img src="/static/images/thinker.jpg" alt="réflexion...">
                    </div>
                    <div class="loader-text">
                        Recherche en cours
                    </div>`;

let answerTemplate = `<div class="map" style="width:75%;margin: auto;"></div>
                <h2 class="address"></h2>
                <div class="description"></div>
                <a class="more-info" href="#" target="_blank"></a>`;


let loader = (loading) => {
    let i = 0;
    if (loading === true) {
        let loaderBlock = document.createElement("div");
        loaderBlock.classList.add("loader", "answer", "answer-grandpy");
        loaderBlock.innerHTML = loaderTemplate;
        dialogDiv.appendChild(loaderBlock);
        let loaderText = loaderBlock.getElementsByClassName("loader-text")[0];
        loadInterval = setInterval(() => {
            dialogDiv.style.borderColor = colors[i];
            if (i < colors.length) {
                i++;
                loaderText.innerHTML += "...";
            } else {
                i = 0;
            }
        }, 1000)
    } else {
        clearInterval(loadInterval);
        dialogDiv.style.borderColor = 'rgba(19, 181, 219, .5)';
        let activeLoaders = document.querySelectorAll(".loader");
        let i;
        for (i = 0; i < activeLoaders.length; i++) {
            activeLoaders[i].parentNode.removeChild(activeLoaders[i]);
        }
    }
};


function myMap(mapDiv, lat, long) {
    let center = new google.maps.LatLng(lat, long);
    let mapOptions = {
        center: center,
        zoom: 17,
    };
    let map = new google.maps.Map(mapDiv, mapOptions);
    let marker = new google.maps.Marker({position: center, map: map})
}

let ajaxGet = (url, callback) => {
    let req = new XMLHttpRequest();
    req.open("GET", url, true);
    req.addEventListener("load", () => {
        if (req.status >= 200 && req.status < 400) {
            callback(req.responseText);
        } else {
            console.error(req.status + " " + req.statusText + " " + url)
        }
    });
    req.addEventListener("error", () => {
        console.error("Network error with url : " + url)
    })
    req.send();
};

let ajaxPost = (url, data, callback) => {
    let req = new XMLHttpRequest();
    req.open("POST", url, true);
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


let addUserQuestion = (question) => {
    let questionBlock = document.createElement("div");
    questionBlock.classList.add("answer", "answer-user");
    questionBlock.textContent = question;
    dialogDiv.append(questionBlock);
};

let addGrandPyBaseAnswer = (answer) => {
    let answerBlock = document.createElement("div");
    answerBlock.classList.add("answer", "answer-grandpy");
    answerBlock.textContent = answer;
    dialogDiv.append(answerBlock);
};

let addFullAnswer = (data) => {
    let googleData = data.results.google_maps_api_results;
    let wikiData = data.results.wikipedia_api_results;

    let fullAnswerBlock = document.createElement("div");
    fullAnswerBlock.classList.add("answer", "answer-grandpy");
    fullAnswerBlock.innerHTML = answerTemplate;
    let mapDiv = fullAnswerBlock.getElementsByClassName("map")[0];
    let addressDiv = fullAnswerBlock.getElementsByClassName("address")[0];
    let descriptionDiv = fullAnswerBlock.getElementsByClassName("description")[0];
    let moreInfoLink = fullAnswerBlock.getElementsByClassName("more-info")[0];
    mapDiv.style.height = '400px';
    myMap(mapDiv, googleData.location.lat, googleData.location.lng);
    addressDiv.textContent = googleData.formatted_address;
    descriptionDiv.innerHTML = wikiData.description;
    moreInfoLink.href = wikiData.url;
    moreInfoLink.innerText = "En savoir plus."
    dialogDiv.append(fullAnswerBlock);
};

searchForm.addEventListener("submit", (e) => {
    addUserQuestion(searchForm.search.value);
    setTimeout(() => {
        ajaxGet(sentenceUrl, (response) => {
            addGrandPyBaseAnswer(JSON.parse(response)['sentence']);
            loader(true);
            let data = new FormData(searchForm);
            searchBtn.disabled = true;
            eraseBtn.disabled = true;
            ajaxPost(processUrl, data, (response) => {
                loader(false);
                searchBtn.disabled = false;
                eraseBtn.disabled = false;
                let receivedData = JSON.parse(response);
                addFullAnswer(receivedData);
            });
        });
    }, 500);


    e.preventDefault();
});

eraseBtn.addEventListener("click", (e) => {
    e.preventDefault();
    while (dialogDiv.firstChild) {
        dialogDiv.removeChild(dialogDiv.firstChild);
    }
})
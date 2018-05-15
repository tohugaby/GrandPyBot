const processUrl = "/process";
let dialog = document.querySelector("#dialog")


let submitForm = (url, data, callback) => {
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
    let data = new FormData(searchForm);
    submitForm(processUrl, data, (response) => {

        let response_div = document.createElement("div");
        response_div.innerHTML = JSON.stringify(response);
        while (dialog.firstChild){
            dialog.removeChild(dialog.firstChild)
        }
        dialog.appendChild(response_div);
        console.log(response);
    });
    e.preventDefault();
});


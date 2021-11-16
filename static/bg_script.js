// PaQwiOxGotLM41moiw_Atm76ji3T0EG3wDmb7mX6pOk

let client_id = "C0OdHfEEUqieghnJf62aDhdykSkQWQITvr_ek8Bvj2s";
let endpoint = ("https://api.unsplash.com/photos/random/?client_id="+client_id);

fetch(endpoint)
    .then(function(response) {
        return response.json();
    })
    .then(function(imgData) {
        document.body.style.backgroundImage = "url('"+imgData.urls.regular+"')";
    })
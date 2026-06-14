const cityInput = document.getElementById("city");
const options = document.getElementById("options");

const mapBtn = document.getElementById("mapBtn");
const mapModal = document.getElementById("mapModal");
const closeBtn = document.getElementById("closeBtn");

const currentLocationBtn =
document.getElementById("currentLocationBtn");

const checkWeatherBtn =
document.getElementById("checkWeatherBtn");

const selectedLocation =
document.getElementById("selectedLocation");



/* Show Options On Input Focus */

cityInput.addEventListener("focus", () => {

    options.style.display = "block";

});


/* Hide Options When Clicking Outside */

document.addEventListener("click", (e) => {

    if(!e.target.closest(".search-container")){

        options.style.display = "none";

    }

});

/* Close Map Modal */

closeBtn.addEventListener("click", () => {

    mapModal.style.display = "none";

});

/* Current Location Button */

currentLocationBtn.addEventListener(
"click",
async () => {

    navigator.geolocation.getCurrentPosition(

        async function(position){

            document.getElementById("lat").value =
            position.coords.latitude;

            document.getElementById("lon").value =
            position.coords.longitude;

            document.querySelector("form").submit();

        }

    );

});


/* Check Weather Button */

checkWeatherBtn.addEventListener("click", () => {
   
    document.querySelector("form").submit();

});
let map;
let marker;

mapBtn.addEventListener("click", () => {

    mapModal.style.display = "flex";

    if(map){
        setTimeout(() => map.invalidateSize(), 200);
        return;
    }

    navigator.geolocation.getCurrentPosition(

        function(position){

            const lat = position.coords.latitude;
            const lon = position.coords.longitude;

            map = L.map("map")
            .setView([lat, lon], 12);

            L.tileLayer(
                "https://tile.openstreetmap.org/{z}/{x}/{y}.png",
                {
                    attribution:
                    "&copy; OpenStreetMap"
                }
            ).addTo(map);

            marker = L.marker([lat, lon])
            .addTo(map);

            map.on("click",
            async function(e){

                const newLat =
                e.latlng.lat;

                const newLon =
                e.latlng.lng;

                marker.setLatLng(
                    [newLat, newLon]
                );

                const response =
                await fetch(
                `https://nominatim.openstreetmap.org/reverse?format=json&lat=${newLat}&lon=${newLon}`
                );

                const data =
                await response.json();

                const city =
                data.address.city ||
                data.address.town ||
                data.address.village ||
                data.address.state ||
                "Unknown Location";

                document.getElementById("lat").value =newLat;

                document.getElementById("lon").value =newLon;

                selectedLocation.textContent =
                city;

                checkWeatherBtn.disabled =
                false;

            });

        },

        function(){

            alert(
            "Location access denied"
            );

        }

    );

});
document.querySelector("form")
.addEventListener("submit", async function(e){

    if(
        document.getElementById("lat").value &&
        document.getElementById("lon").value
    ){
        return;
    }

    e.preventDefault();

    const city =
    cityInput.value.trim();

    const response =
    await fetch(
    `https://nominatim.openstreetmap.org/search?format=json&q=${city}`
    );

    const data =
    await response.json();

    if(data.length > 0){

        document.getElementById("lat").value =
        data[0].lat;

        document.getElementById("lon").value =
        data[0].lon;

        this.submit();
    }

});
console.log("script.js loaded");

// api key for geoapify
const geoapifyKey = JSON.parse(
    document.getElementById("geoapify-key").textContent
);

//geoapify widget
const birthplaceAutocomplete = new autocomplete.GeocoderAutocomplete(
    document.getElementById("birthplace-autocomplete"),
    geoapifyKey,
    {
        type: "city",
        placeholder: "Enter your birth city or town",
        lang: "en",
        limit: 5
    }
);

function clearBirthplace() {
    console.log("Clearing location");
    document.getElementById("birthplace").value = "";
    document.getElementById("location-id").value = "";
    document.getElementById("latitude").value = "";
    document.getElementById("longitude").value = "";
    document.getElementById("birth-timezone").value = "";
}

birthplaceAutocomplete.on("select", function (location) {
    console.log("Select event received:", location);
    clearBirthplace();

    if (!location) {
        return;
    }

    const details = location.properties;

    console.log("Selected location time zone:", details.timezone);

    document.getElementById("birthplace").value = details.formatted;
    document.getElementById("location-id").value = details.place_id;
    document.getElementById("latitude").value = details.lat;
    document.getElementById("longitude").value = details.lon;
    document.getElementById("birth-timezone").value = details.timezone?.name ?? "";
    console.log("Location selected:", {
        birthplace: document.getElementById("birthplace").value,
        latitude: document.getElementById("latitude").value,
        longitude: document.getElementById("longitude").value
    });
    
});

// clear the old selection if the user starts changing the location.
document.getElementById("birthplace-autocomplete")
    .addEventListener("input", clearBirthplace);

console.log("Location listeners ready");
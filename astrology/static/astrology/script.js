const geoapifyKey = JSON.parse(
    document.getElementById("geoapify-key").textContent
);

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
    document.getElementById("birthplace").value = "";
    document.getElementById("location-id").value = "";
    document.getElementById("latitude").value = "";
    document.getElementById("longitude").value = "";
}

birthplaceAutocomplete.on("select", function (location) {
    clearBirthplace();

    if (!location) {
        return;
    }

    const details = location.properties;

    document.getElementById("birthplace").value = details.formatted;
    document.getElementById("location-id").value = details.place_id;
    document.getElementById("latitude").value = details.lat;
    document.getElementById("longitude").value = details.lon;
});

// clear the old selection if the user starts changing the location.
document.getElementById("birthplace-autocomplete")
    .addEventListener("input", clearBirthplace);
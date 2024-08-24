function initMap() {
    // Koordinat Terminal Manggar, Belitung Timur
    const terminalManggar = { lat: -2.884405, lng: 108.270798 };
    
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 15,
        center: terminalManggar,
    });
    
    const marker = new google.maps.Marker({
        position: terminalManggar,
        map: map,
        title: "Terminal Manggar, Belitung Timur"
    });
}
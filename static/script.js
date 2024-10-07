function performSearch() {
    var city = document.querySelector('.city-input').value;
    fetch('/submit_city', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: 'city=' + encodeURIComponent(city)
    })
    .then(response => response.json())
    .then(data => {
        // Update DOM elements with fetched data
        document.querySelector('.details h2').textContent = data.full_location;
        document.querySelector('.details h6:nth-child(2)').textContent = "Date: " + data.time;
        document.querySelector('.details h6:nth-child(3)').textContent = "Temperature: " + data.temperature + "°F";
        document.querySelector('.details h6:nth-child(4)').textContent = "Wind Speed: " + data.wind_speed + " MPH";
        document.querySelector('.details h6:nth-child(5)').textContent = "Humidity: " + data.humidity + "%";
        document.querySelector('.details h6:nth-child(6)').textContent = "Rain Intensity: " + data.rain_intensity + " inches per hour";
        document.querySelector('.details h6:nth-child(7)').textContent = "Visibility: " + data.visibility + " miles";
        document.querySelector('.details h6:nth-child(8)').textContent = "Snow Intensity: " + data.snow_intensity + " inches per hour";

        const tempImage1 = data.temperature >= 80 ? 'hot.png' : 'cold.png';
        document.querySelector('.forecast-grid-item img:nth-child(1)').src = `/static/${tempImage1}`;
        document.querySelector('.forecast-grid-item img:nth-child(1)').alt = data.temperature >= 80 ? 'Hot weather' : 'Cold weather';

        const tempImage2 = 
        data.visibility >= 9 && data.rain_intensity == 0 && data.humidity < 70 ? 'sun.png' :
        data.visibility >= 6 && data.visibility < 9 && data.rain_intensity == 0 && data.humidity < 80 ? 'partly-cloudy.png' :
        data.visibility >= 3 && data.visibility < 6 && data.rain_intensity == 0 && data.humidity >= 80 ? 'cloudy.png' :
        data.visibility >= 1 && data.visibility < 3 && data.rain_intensity > 0 && data.rain_intensity <= 0.1 && data.humidity >= 85 ? 'drizzle.png' :
        data.visibility <= 0.5 && data.rain_intensity > 0.1 && data.rain_intensity < 0.3 && data.humidity >= 90 ? 'heavy-rain.png' :
        data.rain_intensity >= 0.3 ? 'lightning-bolt.png' :
        'drizzle.png';
    
        document.querySelector('.forecast-grid-item img:nth-child(2)').src = `/static/${tempImage2}`;
        document.querySelector('.forecast-grid-item img:nth-child(2)').alt = 
            data.visibility >= 9 && data.rain_intensity == 0 && data.humidity < 70 ? 'Clear sky, High visibility, Low humidity' :
            data.visibility >= 6 && data.visibility < 9 && data.rain_intensity == 0 && data.humidity < 80 ? 'Partly cloudy, Medium visibility, Moderate humidity' :
            data.visibility >= 3 && data.visibility < 6 && data.rain_intensity == 0 && data.humidity >= 80 ? 'Cloudy, Low visibility, High humidity' :
            data.visibility >= 1 && data.visibility < 3 && data.rain_intensity > 0 && data.rain_intensity <= 0.1 && data.humidity >= 85 ? 'Drizzle, Low visibility, High humidity' :
            data.visibility <= 0.5 && data.rain_intensity > 0.1 && data.rain_intensity < 0.3 && data.humidity >= 90 ? 'Heavy rain, Very low visibility, Very high humidity' :
            data.rain_intensity >= 0.3 ? 'Heavy rain with lightning' :
            'Drizzle, Moderate rain intensity';
    
        console.log(data);
    })
    .catch(error => console.error('Error fetching data:', error));
}

// Add event listener for the search button
document.querySelector('.search-btn').addEventListener('click', performSearch);

// Add event listener for the Enter key on the input field
document.querySelector('.city-input').addEventListener('keyup', function(event) {
    if (event.key === 'Enter') {
        performSearch();
    }
});
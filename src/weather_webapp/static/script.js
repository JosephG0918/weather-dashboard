/**
 * Performs a search for weather data of the selected city.
 * Sends a POST request to the server with the city name and updates the DOM with the current weather and 5-day forecast.
 * @param {string} city - The name of the city to search for.
 */
function performSearch(city) {
    fetch('/submit_city', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: 'city=' + encodeURIComponent(city)
    })
    .then(response => response.json())
    .then(data => {
        // Update Current Weather
        const locationElement = document.querySelector('.details h2');
        if (locationElement) locationElement.textContent = data.full_location;

        const dateElement = document.querySelector('.details h6:nth-child(2)');
        if (dateElement) dateElement.textContent = "Date: " + data.current.time;

        const tempElement = document.querySelector('.details h6:nth-child(3)');
        if (tempElement) {
            tempElement.innerHTML = `Temperature: ${data.current.temperature}°F
                <img class="temp-icon" src="${data.current.temperature >= 75 ? "/static/img/hot.png" : "/static/img/cold.png"}" alt="Temperature Icon">`;
        }

        const windSpeedElement = document.querySelector('.details h6:nth-child(4)');
        if (windSpeedElement) windSpeedElement.textContent = "Wind Speed: " + data.current.wind_speed + " MPH";

        const humidityElement = document.querySelector('.details h6:nth-child(5)');
        if (humidityElement) humidityElement.textContent = "Humidity: " + data.current.humidity + "%";

        const visibilityElement = document.querySelector('.details h6:nth-child(6)');
        if (visibilityElement) visibilityElement.textContent = "Visibility: " + data.current.visibility + " miles";

        const rainIntensityElement = document.querySelector('.details h6:nth-child(7)');
        if (rainIntensityElement) {
            rainIntensityElement.innerHTML = `Weather:
                <img class="weather-icon" src="${data.current.rain_intensity > 0.1 ? "/static/img/rain.png" : data.current.cloud_cover > 50 ? "/static/img/cloud.png" : "/static/img/sun.png"}" alt="Weather Icon">`;
        }

        // Update 5-Day Forecast
        let forecastContainer = document.querySelector('.weather-cards');
        if (forecastContainer) {
            forecastContainer.innerHTML = ""; // Clear previous forecast
            data.forecast.forEach(day => {
                let iconSrc_temp = day.temperature >= 75 ? "/static/img/hot.png" : "/static/img/cold.png";
                let iconSrc_weather = day.rain_intensity > 0.1 ? "/static/img/rain.png" : day.cloud_cover > 50 ? "/static/img/cloud.png" : "/static/img/sun.png";

                // Generate forecast card for each day
                let forecastCard = `
                    <li class="card">
                        <h3>${day.time}</h3>
                        <h6>Temp: ${day.temperature}°F
                          <img class="temp-icon" src="${iconSrc_temp}" alt="Temperature Icon">
                        </h6>
                        <h6>Wind: ${day.wind_speed} MPH</h6>
                        <h6>Humidity: ${day.humidity}%</h6>
                        <h6>Weather:
                          <img class="weather-icon" src="${iconSrc_weather}" alt="Weather Icon">
                        </h6>
                    </li>
                `;
                forecastContainer.innerHTML += forecastCard;
            });
        }
    })
    .catch(error => console.error('Error fetching data:', error));
}

/**
 * Handles dropdown selection for city.
 * Updates the button text with the selected city and performs the weather search.
 */
document.querySelectorAll(".dropdown-content a").forEach(item => {
    item.addEventListener("click", function() {
        let city = this.dataset.city;
        document.querySelector(".dropbtn").textContent = city; // Update button text
        performSearch(city); // Perform search with selected city
    });
});

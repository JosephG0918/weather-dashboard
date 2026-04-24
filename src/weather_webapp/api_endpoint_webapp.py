from flask import Flask, jsonify, render_template, request, session
import requests
import re
from deep_translator import GoogleTranslator
import secrets
from dotenv import load_dotenv
import os
from convert_to_12hour import convert_to_12hour
import logging

# Configure logging
logging.basicConfig(
    filename='logs/weather_app.log',
    level=logging.WARNING,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class WeatherApp:
    """
    A Flask-based weather application that fetches weather data from Tomorrow.io API,
    translates locations, and provides a dashboard with real-time and forecasted weather.
    """
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('WEATHER_API_KEY')
        self.translator = GoogleTranslator()
        self.app = Flask(__name__, template_folder="templates", static_folder="static")
        self.app.secret_key = secrets.token_hex(16)
        self.setup_routes()

    def setup_routes(self):
        """Defines the application routes."""
        self.app.route("/weather")(self.index)
        self.app.route("/submit_city", methods=["POST"])(self.handle_city)
        self.app.route("/realtime_weather", methods=["GET"])(self.get_realtime_weather)

    def index(self):
        """Renders the main weather dashboard."""
        if 'location' not in session:
            session['location'] = "Los Angeles"
        data = self.get_weather_data(session['location'])
        return render_template("index.html", data=data)

    def handle_city(self):
        """Handles city selection and fetches translated weather data."""
        city = request.form["city"]
        translated = self.translator.translate(city, dest='en')
        session['location'] = translated
        data = self.get_weather_data(session['location'])
        return jsonify(data)

    def get_realtime_weather(self):
        """Returns real-time weather data for the selected location."""
        if 'location' not in session:
            session['location'] = "Los Angeles"
        data = self.get_weather_data(session['location'])
        return jsonify(data)

    def get_weather_data(self, location):
        """Fetches weather data from Tomorrow.io API for a given location."""
        url = f"https://api.tomorrow.io/v4/weather/forecast?location={location}&timesteps=1d&units=imperial&apikey={self.api_key}"
        headers = {"accept": "application/json", "accept-encoding": "deflate, gzip, br"}
        response = requests.get(url, headers=headers).json()

        try:
            weather_data = self.extract_weather_data(response)
            logging.debug(f"Received response: {response}")
            return weather_data
        except Exception as e:
            error_message = f"Error fetching weather data for {location}: {response.get('type', 'Error')} : {response.get('message', str(e))}"
            logging.error(error_message)
            return {"error": error_message}

    def extract_weather_data(self, response_dict):
        """Extracts relevant weather data from API response."""
        full_location = self.translator.translate(str(response_dict["location"]["name"]), dest='en')
        weather_data = {"full_location": full_location, "current": {}, "forecast": []}

        if "timelines" in response_dict:
            daily_forecast = response_dict["timelines"].get("daily", [])

            for i, day in enumerate(daily_forecast):
                values = day["values"]
                formatted_12hour_time = convert_to_12hour(re.sub("T", " ", day["time"]).split(":00Z")[0])

                # Extract relevant weather details
                day_data = {
                    "time": formatted_12hour_time,
                    "temperature": values.get("temperatureAvg", 0),
                    "humidity": values.get("humidityAvg", 0),
                    "wind_speed": values.get("windSpeedAvg", 0),
                    "visibility": values.get("visibilityAvg", 0),
                    "rain_intensity": values.get("rainIntensityAvg", 0),
                    "cloud_cover": values.get("cloudCoverAvg", 0)
                }

                if i == 0:
                    weather_data["current"] = day_data
                else:
                    weather_data["forecast"].append(day_data)
                    if i == 5:  # Limit forecast to 5 days
                        break

        return weather_data

    def run(self):
        """Starts the Flask application."""
        self.app.run(host="0.0.0.0", port=5000, debug=True)  # Use port 5000 on Raspberry Pi/Linux unless running as root.

if __name__ == "__main__":
    weather_app = WeatherApp()
    weather_app.run()
# https://www.tomorrow.io/ - the API.
# https://www.flaticon.com/free-icons/weather-forecast/3 - weather icons.

from flask import Flask, jsonify, render_template, request, session
import requests
import re
from deep_translator import GoogleTranslator
import secrets
from dotenv import load_dotenv
import os

class WeatherApp:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('WEATHER_API_KEY')
        self.translator = GoogleTranslator()
        self.app = Flask(__name__, template_folder="templates", static_folder="static")
        self.app.secret_key = secrets.token_hex(16)
        self.setup_routes()

    def setup_routes(self):
        self.app.route("/")(self.index)
        self.app.route("/submit_city", methods=["POST"])(self.handle_city)
        self.app.route("/realtime_weather", methods=["GET"])(self.get_realtime_weather)

    def index(self):
        if 'location' not in session:
            session['location'] = "Los Angeles"
        data = self.get_weather_data(session['location'])
        return render_template("index.html", data=data)

    def handle_city(self):
        city = request.form["city"]
        translated = self.translator.translate(city, dest='en')
        session['location'] = translated
        data = self.get_weather_data(session['location'])
        return jsonify(data)

    def get_realtime_weather(self):
        if 'location' not in session:
            session['location'] = "Los Angeles"
        data = self.get_weather_data(session['location'])
        return jsonify(data)

    def get_weather_data(self, location):
        url = f"https://api.tomorrow.io/v4/weather/realtime?location={location}&units=imperial&apikey={self.api_key}"
        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers).json()

        try:
            weather_data = self.extract_weather_data(response)
            return weather_data
        except Exception as e:
            return {"error": f"{response.get('type', 'Error')} : {response.get('message', str(e))}"}

    def extract_weather_data(self, response_dict):
        values = response_dict["data"]["values"]
        full_location = self.translator.translate(str(response_dict["location"]["name"]), dest='en')
        time = str(response_dict["data"]["time"])
        
        return {
            "time": re.findall("(.+):...", re.sub("T", " ", time))[0],
            "location": session['location'],
            "full_location": full_location,
            "temperature": float(values["temperature"]),
            "humidity": float(values["humidity"]),
            "wind_speed": float(values["windSpeed"]),
            "rain_intensity": float(values["rainIntensity"]),
            "visibility": float(values["visibility"]),
            "snow_intensity": float(values["snowIntensity"]),
            "image_filename1": "hot.png" if float(values["temperature"]) >= 80 else "cold.png",
            "image_filename2": "sun.png" if float(values["visibility"]) >= 9 and float(values["rainIntensity"]) == 0 and float(values["humidity"]) < 70 else \
                "partly-cloudy.png" if float(values["visibility"]) >= 6 and float(values["visibility"]) < 9 and float(values["rainIntensity"]) == 0 and float(values["humidity"]) < 80 else \
                "cloudy.png" if float(values["visibility"]) >= 3 and float(values["visibility"]) < 6 and float(values["rainIntensity"]) == 0 and float(values["humidity"]) >= 80 else \
                "drizzle.png" if float(values["visibility"]) >= 1 and float(values["visibility"]) < 3 and float(values["rainIntensity"]) > 0 and float(values["rainIntensity"]) <= 0.1 and float(values["humidity"]) >= 85 else \
                "heavy-rain.png" if float(values["visibility"]) <= 0.5 and float(values["rainIntensity"]) > 0.1 and float(values["humidity"]) >= 90 and float(values["rainIntensity"]) < 0.3 else \
                "lightning-bolt.png" if float(values["rainIntensity"]) >= 0.3 else \
                "drizzle.png"
        }

    def run(self):
        self.app.run(host="0.0.0.0", port=80, debug=True)

if __name__ == "__main__":
    weather_app = WeatherApp()
    weather_app.run()
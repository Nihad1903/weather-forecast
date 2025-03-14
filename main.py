from flask import Flask, render_template, request
from utils import get_city_name, get_weather_data

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/weather", methods = ["POST", "GET"])
def weather():
    if request.method == "POST":
        location = request.form.get('location')
        if not location:
            return render_template("index.html", error="Please enter a valid location")

        latitude, longitute = get_city_name(location)

        if not latitude or not longitute:
            return render_template("index.html", error="Weather data not found for the given location")

        weather_data, month_name = get_weather_data(latitude=latitude, longitute=longitute)

        today_key = next(iter(weather_data))
        today_value = weather_data[today_key]

        del weather_data[today_key]

        context = {
            "data": weather_data,
            "month_abbr": month_name,
            "today": {
                today_key: today_value
            },
            "location": location
        }

        return render_template("index.html", context=context)

if __name__ == "__main__":
    app.run(debug=True)




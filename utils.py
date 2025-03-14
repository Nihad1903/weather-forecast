import requests
import calendar

location_url = "https://nominatim.openstreetmap.org/search"
weather_url = "https://api.open-meteo.com/v1/forecast"


def get_weather_data(latitude, longitute):
    parameters = {
    "latitude": float(latitude),
    "longitude": float(longitute),
    "hourly": "temperature_2m"
    }
    response = requests.get(url=weather_url, params=parameters).json()
    dates = {}
    for time, temp in zip(response["hourly"]["time"], response["hourly"]["temperature_2m"]):
        date, hour = time.split("T")[0].split("-")[-1], time.split("T")[1]

        if hour == "12:00" or hour == "00:00":
            if date in dates:
                dates[date].append([hour, temp])
            else:
                dates[date] = []
                dates[date].append([hour, temp])
        
    month_index = int(response["hourly"]["time"][0].split("-")[1])
    month_name = calendar.month_abbr[month_index]

    return dates, month_name


def get_city_name(location):
    parameters = {
        "q": location,
        "format": "json",
        "limit": 1
    }
    headers = {
        'User-Agent': 'Chrome/134.0.0.0 Safari/537.36'
    }
    response = requests.get(url=location_url, params=parameters, headers=headers).json()

    if not response:
        return None, None

    latitude = response[0]["lat"]
    longitude = response[0]["lon"]

    return latitude, longitude

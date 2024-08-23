#0.14.py
import requests
import tkinter as tk
from tkinter import messagebox

# API Keys
API_key = "3842348f97de0f2bc972353861cc8a9c"
accuweather_api_key = 'AxGvhpU9DZbkXAlCwJwoEUrU6Yiup2P4'

# Color format
BG_COLOR = "#d9eeff"
BUTTON_COLOR = "#b5c4ff"
BUTTON_HOVER_COLOR = "#3E8E41"
BUTTON_TEXT_COLOR = "#FFFFFF"
TEXT_COLOR = "#000000"
FONT_FAMILY = "Arial"
FONT_SIZE = 20

state_code = ""
country_code = ""
limit = 1

def update_text(data, color):
    text.tag_configure("green", foreground="green")
    text.tag_configure("red", foreground="red")
    text.insert(tk.END, data + "\n", color)
    text.yview_moveto(1.0)

def get_weather_data():
    city = city_entry.get()  # Get the city input from the entry widget

    try:
        if city:
            city_name = city
            # Step 1: Get latitude and longitude from manual city input
            geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name},{state_code},{country_code}&limit={limit}&appid={API_key}"
            geo_response = requests.get(geo_url)
            geo_data = geo_response.json()

            if geo_data:
                lat = geo_data[0]['lat']
                lon = geo_data[0]['lon']
            else:
                update_text("Error: City not found.", "red")
                return  # Exit the function if the city is not found

        else:  # If no manual input is provided, use IP-based location
            ip_data = requests.get("https://ipinfo.io").json()
            lat, lon = ip_data['loc'].split(',')
            city_name = ip_data['city']

        # Step 2: Get the location key from AccuWeather using latitude and longitude
        location_url = f"http://dataservice.accuweather.com/locations/v1/cities/geoposition/search"
        params = {
            'apikey': accuweather_api_key,
            'q': f"{lat},{lon}"
        }
        location_response = requests.get(location_url, params=params)

        if location_response.status_code == 200:
            location_data = location_response.json()
            location_key = location_data.get('Key')

            if location_key:
                # Step 3: Get weather data using the location key
                weather_url = f"http://dataservice.accuweather.com/currentconditions/v1/{location_key}"
                weather_params = {
                    'apikey': accuweather_api_key,
                }
                weather_response = requests.get(weather_url, params=weather_params)

                if weather_response.status_code == 200:
                    weather_data = weather_response.json()
                    if weather_data:
                        sky_look = weather_data[0]['WeatherText']
                        temperature = weather_data[0]['Temperature']['Metric']['Value']
                        rain = weather_data[0]['HasPrecipitation']

                        rain_status = "Likely to rain." if rain else "No rain."

                        # Update the output text widget
                        update_text(f"The weather in {city_name} is {temperature}°C with {rain_status}. The sky looks {sky_look}.", "green")
                    else:
                        update_text("Error: Weather data is empty.", "red")
                else:
                    update_text(f"Error fetching weather data: {weather_response.status_code}", "red")
            else:
                update_text("Error: Could not retrieve location key.", "red")
        else:
            update_text(f"Error fetching location key: {location_response.status_code}", "red")

    except Exception as e:
        update_text(f"An error occurred: {e}", "red")

root = tk.Tk()
root.title("Weather UI Tester")
root.configure(bg=BG_COLOR)

# Create an entry widget for user input
city_entry = tk.Entry(root, width=30)
city_entry.pack(pady=10)

get_weather_button = tk.Button(root, text="Get Weather", command=get_weather_data, padx=20, pady=10, bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR)
get_weather_button.pack()

text = tk.Text(root, wrap="word", width=80, height=10, bg=BG_COLOR, fg=TEXT_COLOR, font=(FONT_FAMILY, FONT_SIZE))
text.pack(side="top", padx=10, pady=10)

root.mainloop()
import streamlit as st
from pyowm.owm import OWM
from pyowm.utils.config import get_default_config
from pyowm.utils import timestamps
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import requests

# API details
API_key = '7a9d8997dd647d860585dc8e96bd84b2'
config_dict = get_default_config()
config_dict['language'] = 'en'
owm = OWM(API_key, config_dict)
mgr = owm.weather_manager()

# IPGeolocation API details
IP_API_KEY = 'c0dab82cf0d14895a398926861edc9a8'

# to get forecast
def get_forecaster(city):
    try:
        return mgr.forecast_at_place(city, '3h')
    except Exception as e:
        st.error(f"Error retrieving weather data: {e}")
        return None

#to plot bar chart
def plot_bar_chart(days, temp_min, temp_max):
    plt.figure(figsize=(10, 5))
    plt.bar(days, temp_min, label="Min Temp", color='blue', alpha=0.7)
    plt.bar(days, temp_max, label="Max Temp", color='red', alpha=0.7)
    plt.xlabel('Days')
    plt.ylabel('Temperature (°C)')
    plt.title('Temperature Forecast')
    plt.legend()
    st.pyplot(plt)

# to plot line chart
def plot_line_chart(days, temp_min, temp_max):
    plt.figure(figsize=(10, 5))
    plt.plot(days, temp_min, label="Min Temp", color='blue', marker='o')
    plt.plot(days, temp_max, label="Max Temp", color='red', marker='o')
    plt.xlabel('Days')
    plt.ylabel('Temperature (°C)')
    plt.title('Temperature Forecast')
    plt.legend()
    st.pyplot(plt)

#to extract additional weather information including sunrise and sunset times
def extract_additional_info(city):
    additional_info = {}
    
    #current weather for sunrise and sunset times
    observation = mgr.weather_at_place(city)
    weather = observation.weather

    #UTC timestamps for sunrise and sunset
    sunrise_utc = weather.sunrise_time('unix')
    sunset_utc = weather.sunset_time('unix')

    #UTC to IST (UTC + 5:30 hours)
    ist_offset = timedelta(hours=5, minutes=30)
    sunrise_ist = datetime.utcfromtimestamp(sunrise_utc) + ist_offset
    sunset_ist = datetime.utcfromtimestamp(sunset_utc) + ist_offset

    # Formatting times in ISO and IST
    additional_info['Sunrise (UTC)'] = weather.sunrise_time(timeformat='iso')
    additional_info['Sunrise (IST)'] = sunrise_ist.strftime('%Y-%m-%d %H:%M:%S')
    additional_info['Sunset (UTC)'] = weather.sunset_time(timeformat='iso')
    additional_info['Sunset (IST)'] = sunset_ist.strftime('%Y-%m-%d %H:%M:%S')

    additional_info['Humidity'] = weather.humidity
    wind_speed_mps = weather.wind().get('speed', 0)
    wind_speed_mph = wind_speed_mps * 2.23694  # Convert m/s to mph
    additional_info['Wind Speed'] = f"{wind_speed_mph:.2f} mph" 
    weather_percent = weather.clouds
    additional_info['Cloud Coverage'] = f"{weather_percent} %"

    return additional_info

#to get user's current location using IPGeolocation API
def get_user_location():
    url = f"https://api.ipgeolocation.io/ipgeo?apiKey={IP_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        city = data['city']
        latitude = data['latitude']
        longitude = data['longitude']
        country = data['country_name']
        return city, latitude, longitude, country
    else:
        st.error(f"Error retrieving location: {response.status_code}")
        return None, None, None, None

# Streamlit UI
st.title("Weather Forecast App")

# Add a button for user location
if st.button("Get Weather for My Location"):
    city, latitude, longitude, country = get_user_location()
    if city:
        st.session_state.city = city  # Store the city in session state for later use
        st.success(f"Detected location: {city}, {country} (Lat: {latitude}, Lon: {longitude})")
    else:
        st.error("Unable to detect location.")

#for manual city input
city = st.text_input("Enter a city", st.session_state.city if 'city' in st.session_state else "Los Angeles")
graph_type = st.selectbox("Select graph type", ["Bar Chart", "Line Chart"])

# Fetching and display weather data
if city:
    forecaster = get_forecaster(city)

    if forecaster:
     
        forecast_list = forecaster.forecast.weathers
        days = []
        temp_min = []
        temp_max = []

        for forecast in forecast_list:
            day = forecast.reference_time('iso').split(" ")[0]
            days.append(day)
            
            
            temp_data = forecast.temperature('celsius')
            min_temp = temp_data.get('min', temp_data.get('temp')) 
            max_temp = temp_data.get('max', temp_data.get('temp'))  
            
            temp_min.append(min_temp)
            temp_max.append(max_temp)

        # graph based on the user's choice
        if graph_type == "Bar Chart":
            plot_bar_chart(days, temp_min, temp_max)
        else:
            plot_line_chart(days, temp_min, temp_max)

        #additional weather info, including sunrise and sunset
        additional_info = extract_additional_info(city)
        st.subheader("Additional Weather Information")
        for key, value in additional_info.items():
            st.write(f"{key}: {value}")

        # forecast conditions
        st.subheader("Weather Conditions")
        st.write("Will it rain? ", forecaster.will_have_rain())
        st.write("Will it be clear? ", forecaster.will_have_clear())
        st.write("Will it be cloudy? ", forecaster.will_have_clouds())
        st.write("Will there be a storm? ", forecaster.will_have_storm())

else:
    st.write("Please enter a city name to see the forecast.")

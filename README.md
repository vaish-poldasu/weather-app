
# Weather Forecast App

This Weather Forecast App provides detailed weather forecasts for any city with real-time data from OpenWeatherMap. Built with Streamlit, it offers graphical and textual information, including temperature trends, weather details, and condition predictions. Ideal for daily and weekly planning, this app brings essential weather insights to your fingertips.

## Features

- **Location-based Weather**: Automatically detects user’s location to provide local weather forecasts.
- **Temperature Forecast**: Displays minimum and maximum temperatures in both bar and line chart formats for visual trend analysis.
- **Detailed Weather Information**:
  - Sunrise and Sunset Times (UTC and IST).
  - Humidity, Wind Speed, and Cloud Coverage.
- **Weather Conditions**: Checks for rain, clear skies, cloudiness, and storms.
- **Graph Selection**: Allows users to choose between bar and line charts for temperature visualization.
- **City-based Forecasting**: Enter any city for customized weather forecasts.

## Technologies Used

- **[Streamlit](https://streamlit.io/)** - For building an interactive web app.
- **[OpenWeatherMap API](https://openweathermap.org/api)** - Provides real-time weather data.
- **[Matplotlib](https://matplotlib.org/)** - Generates clear, visual charts for temperature trends.
- **[IPGeolocation API](https://ipgeolocation.io/)** - Detects user location based on IP address.

## Getting Started

### Prerequisites

- **Python 3.7+**
- Install required Python packages:
  ```bash
  pip install streamlit pyowm matplotlib requests

  ### Running the Application

Follow these steps to run the Weather Forecast App on your local machine:

1. **Configure API Keys**:
   - Obtain API keys from:
     - **OpenWeatherMap**: [Sign up here](https://home.openweathermap.org/users/sign_up).
     - **IPGeolocation**: [Sign up here](https://ipgeolocation.io/signup).
   - Open `weather_app.py` and replace `API_key` and `IP_API_KEY` variables with your own API keys.

2. **Run the Application**:
   - In the terminal, execute the following command:
     ```bash
     streamlit run weather_app.py
     ```

3. **Access the App**:
   - After running the command, a local URL (usually `http://localhost:8501`) will be displayed in the terminal.
   - Open this URL in your browser to start using the Weather Forecast App.


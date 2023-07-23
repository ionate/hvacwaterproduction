import requests

class WeatherModule:
    def __init__(self, api_key):
        self.weather_base_url = "http://api.openweathermap.org/data/2.5/weather"
        self.historical_base_url = "https://www.ncdc.noaa.gov/cdo-web/api/v2/data"
        self.geocode_base_url = "https://nominatim.openstreetmap.org/search"
        self.api_key = api_key

    def get_weather_data(self, location):
        params = {
            "q": location,
            "appid": self.api_key,
            "units": "metric"
        }

        response = requests.get(self.weather_base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            city_name = data["name"]
            temperature = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            pressure = data["main"]["pressure"]
            rain_amount = data.get("rain", {}).get("1h", 0)  # Rainfall in the last hour (if available)
            historical_rainfall = self.get_historical_rainfall(location)
            return {
                "city": city_name,
                "temperature": temperature,
                "humidity": humidity,
                "pressure": pressure,
                "rain_amount": rain_amount,
                "historical_rainfall": historical_rainfall
            }
        else:
            print(f"Failed to fetch weather data for {location}!")
            return None

    def get_historical_rainfall(self, location):
        # Replace 'YOUR_NCEI_TOKEN' with your NCEI API token
        ncei_api_token = 'YOUR_NCEI_TOKEN'
        headers = {"token": ncei_api_token}

        params = {
            "datasetid": "GHCND",  # Global Historical Climatology Network - Daily (GHCND) dataset
            "location": f"city={location}",
            "startdate": "2021-01-01",
            "enddate": "2021-12-31",
            "datatypeid": "PRCP",  # Precipitation data
            "limit": 365,  # Maximum number of data points (365 days in a year)
            "units": "metric"
        }

        response = requests.get(self.historical_base_url, params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            rainfall_data = [entry["value"] for entry in data["results"]]
            return rainfall_data
        else:
            print("Failed to fetch historical rainfall data!")
            return []
        
    def __init__(self, api_key):
        self.weather_base_url = "http://api.openweathermap.org/data/2.5/weather"
        self.geocode_base_url = "https://nominatim.openstreetmap.org/search"
        self.api_key = api_key

    def get_coordinates(self, location):
        params = {
            "q": location,
            "format": "json"
        }

        response = requests.get(self.geocode_base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            if data:
                latitude = data[0]["lat"]
                longitude = data[0]["lon"]
                return latitude, longitude
        print(f"Failed to fetch coordinates for '{location}'!")
        return None, None

    def get_weather_data(self, location):
        latitude, longitude = self.get_coordinates(location)
        if latitude is None or longitude is None:
            return None

        params = {
            "lat": latitude,
            "lon": longitude,
            "appid": self.api_key,
            "units": "metric"
        }

        #print(f'*DEBUG: URL={self.weather_base_url}')
        response = requests.get(self.weather_base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            city_name = data["name"]
            temperature = data["main"]["temp"]
            temp_f = self.convert_to_fahrenheit(temperature)
            humidity = data["main"]["humidity"]
            pressure = data["main"]["pressure"]
            return {
                "city": city_name,
                "temperature": temp_f,
                "humidity": humidity,
                "pressure": pressure
            }
        else:
            print(f"Failed to fetch weather data for {location}!")
            return None

    def calculate_relative_humidity(self, humidity):
        return 0.01 * humidity

    def calculate_absolute_humidity(self, temperature, humidity):
        # Formula to calculate absolute humidity (in grams per cubic meter)
        # For simplicity, we use a simplified version without considering variations with temperature
        return (humidity / 100) * 2.16679 * pow(10, (7.5904 * temperature) / (temperature + 240.5))

    def calculate_average_temperature(self, *temperatures):
        return sum(temperatures) / len(temperatures)

    def calculate_average_humidity(self, *humidities):
        return sum(humidities) / len(humidities)

    def display_weather(self, weather_data):
        if not weather_data:
            return
    def convert_to_fahrenheit(self, temperature_celsius):
        return (temperature_celsius * 9/5) + 32

        temperature = weather_data["temperature"]
        humidity = weather_data["humidity"]
        pressure = weather_data["pressure"]

        relative_humidity = self.calculate_relative_humidity(humidity)
        absolute_humidity = self.calculate_absolute_humidity(temperature, humidity)

        print(f"City: {weather_data['city']}")
        print(f"Temperature: {temperature:.2f}°C")
        print(f"Humidity: {humidity:.2f}%")
        print(f"Relative Humidity: {relative_humidity:.2f}")
        print(f"Absolute Humidity: {absolute_humidity:.2f} g/m³")
        print(f"Pressure: {pressure:.2f} hPa")
        print()

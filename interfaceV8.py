from weather_moduleV8 import WeatherModule


# Example cities in super cold areas (Russia)
cold_cities = ["Moscow, RU", "Saint Petersburg, RU"]

# Example cities in super hot areas (Saudi Arabia)
hot_cities = ["Riyadh, SA", "Jeddah, SA"]

# Example cities with high daily rainfall (India)
rainy_cities = ["Mumbai, IN", "Kolkata, IN"]

def main():
    # Replace 'YOUR_API_KEY' with your OpenWeatherMap API key
    api_key = '06cefde2fb9735b6a48aedd072a74dc7'
    weather_module = WeatherModule(api_key)

    locations = ["New York", "Los Angeles", "London", "Tokyo", "Sydney", "90210"]
    locs2 = ["77055", "78738"]

    for location in locs2:
        print(location)
        weather_data = weather_module.get_weather_data(location)
        weather_module.display_weather(weather_data)
    
    for location in cold_cities:
        print(location)
        weather_data = weather_module.get_weather_data(location)
        weather_module.display_weather(weather_data)

    for location in hot_cities:
        print(location)
        weather_data = weather_module.get_weather_data(location)
        weather_module.display_weather(weather_data)

    for location in rainy_cities:
        print(location)
        weather_data = weather_module.get_weather_data(location)
        weather_module.display_weather(weather_data)

if __name__ == "__main__":
    main()


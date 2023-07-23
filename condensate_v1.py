import random
import time
import requests
from weather_moduleV8 import WeatherModule
import time
import csv

# Simulated weather data
def get_simulated_weather():
    temperature = random.uniform(70, 90)  # Simulate temperature between 70°F and 90°F
    humidity = random.uniform(40, 80)     # Simulate humidity between 40% and 80%
    return temperature, humidity

# Function to estimate AC condensate production
def estimate_condensate_production(temperature, humidity, ac_size, room_square_footage):
    # Constants for the condensate production formula (simplified for the example)
    condensate_per_btuh = 0.005  # Gallons of water produced per BTU per hour
    efficiency_factor = 0.8     # Efficiency factor of the AC unit

    # Calculate the BTUs needed for the room based on square footage
    btus_needed = room_square_footage * 20  # 20 BTUs per square foot

    # Calculate the estimated condensate production
    condensate_production = (
        btus_needed
        * condensate_per_btuh
        * efficiency_factor
        * (1 + (humidity - 50) / 100)  # Adjust for humidity (humidity deviation from 50%)
    )

    return condensate_production

def main():
    conf = {}
    conf['ac_size_btu'] = 36000
    conf['room_sqft'] = 200
    conf['api_key'] = '06cefde2fb9735b6a48aedd072a74dc7'
    conf['houston'] = '77055'
    conf['austin'] = '78738'
    conf['interval_sec'] = 10
    
    # Replace 'YOUR_API_KEY' with your OpenWeatherMap API key
    api_key = '06cefde2fb9735b6a48aedd072a74dc7'
    weather_module = WeatherModule(api_key)
    location = ['austin', 'houston']

    # Room and AC configuration (you can change these values as needed)
    room_square_footage = conf['room_sqft'] #200 # Replace with your room's square footage
    # A “ton” of air conditioning represents approximately 12,000 BTU per hour. 
    # This means that a 3-ton air conditioning system will have 36,000 BTU per hour — 
    # a 4-ton air conditioning system will have 48,000 BTU per hour (and so so forth).
    ac_size_btuh = conf['ac_size_btu'] #36000 # Replace with your AC's cooling capacity in BTU/h

    # Start a CSV file setup
    csv_file = f"ac_data.csv"
    print(f'(writing to file: {csv_file})')
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Temperature (F)", "Humidity (%)", "Condensate Production (gallons/hour)"])
    
    while True:
        for loc in location:
            print('\n----------------')
            print(loc)
            weather_data = weather_module.get_weather_data(conf[loc])
            temperature = weather_data['temperature']
            humidity = weather_data['humidity'] 
            #temperature, humidity = get_simulated_weather()
            condensate_production = estimate_condensate_production(
                temperature, humidity, ac_size_btuh, room_square_footage
            )
            
            print(f"Current Temperature: {temperature:.1f}°F")
            print(f"Current Humidity: {humidity:.1f}%")
            print(f"Estimated Condensate Production: {condensate_production:.2f} gallons/hour")
            print("-" * 30)
            # Append data to CSV file
            with open(csv_file, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([temperature, humidity, condensate_production])

        interval = conf['interval_sec']
        print(f'(sleeping for {interval} secs)')
        time.sleep(interval)  # Simulate data refresh every 5 seconds

if __name__ == "__main__":
    main()

import os
from typing import Any
from dotenv import load_dotenv
import requests
from mcp.server.fastmcp import FastMCP

load_dotenv()

mcp = FastMCP(
    "demo"
)


def format_weather_data(data: dict[str, Any], location: str) -> str:
    """
    Parses a JSON string from a weather API and formats the key information 
    into a concise, human-readable string.
    
    The API data provides temperature in Kelvin (K), which is converted to 
    Celsius (°C) and Fahrenheit (°F).
    """

    # --- Extracting Key Data ---
    
    city = data.get("name", "N/A")
    country = data.get("sys", {}).get("country", "N/A")
    
    # Weather description and main condition
    weather_desc = data.get("weather", [{}])[0].get("description", "N/A").title()
    main_weather = data.get("weather", [{}])[0].get("main", "N/A")
    
    # Main measurements (temperature, humidity, pressure)
    main_data = data.get("main", {})
    temp_k = main_data.get("temp")
    humidity = main_data.get("humidity")
    pressure = main_data.get("pressure")
    
    # Wind speed and direction
    wind_speed = data.get("wind", {}).get("speed")
    wind_deg = data.get("wind", {}).get("deg")
    
    # --- Temperature Conversion ---
    
    temp_c = f"{(temp_k - 273.15):.2f}" if temp_k is not None else "N/A"
    temp_f = f"{((temp_k - 273.15) * 9/5 + 32):.2f}" if temp_k is not None else "N/A"
    
    # --- Formatting the Output String ---

    output_string = (
        f"Weather Report for {location}, {country} -"
        f"\n🌡️ Temperature: {temp_c}°C / {temp_f}°F ({temp_k}K)\n"
        f"☁️ Condition: {weather_desc} ({main_weather})\n"
        f"💧 Humidity: {humidity}%\n"
        f"💨 Wind: {wind_speed} m/s at {wind_deg}°\n"
        f"🧭 Pressure: {pressure} hPa"
    )
    
    return output_string

@mcp.tool(name = 'add_two_numbers', description = "Useful when adding two numbers")
def add(a: int, b: int) -> int:
    return a + b

@mcp.tool(name = "get_weather_data", description="Useful when getting weather data, given proper address")
def get_weather_data(address: str):
    geocoding_api_url = f"https://geocode.maps.co/search?q={address}&api_key={os.environ['GEOCODING_API_KEY']}"
    lat_and_long_res = requests.get(geocoding_api_url, verify=False)
    lat_and_long = lat_and_long_res.json()
    
    if not lat_and_long:
        return "Co-ordinates can't be found, please try different address"
    
    coordinates = lat_and_long[0]
    if 'lat' not in coordinates or 'lon' not in coordinates:
        return "Co-ordinates can't be found, please try different address"
    
    namedetails = coordinates.get('namedetails', {})

    location_name = (
        namedetails.get('name:en') 
        or namedetails.get('name') 
        or coordinates.get('display_name')
    )
    
    
    print(f'Fetching co-ordinates for: {location_name}')
    lat, lon = coordinates['lat'], coordinates['lon']
    
    weather_forecast_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={os.environ['OPEN_WEATHER_API_KEY']}"
    
    print(f'Fetching weather details for: {location_name}')
    weather_forecast_res = requests.get(weather_forecast_url, verify=False)
    weather_forecast_res = weather_forecast_res.json()
    
    if 'weather' not in weather_forecast_res:
        return 'No weather data can be found for the given co-ordinates!'

    return format_weather_data(data = weather_forecast_res, location=location_name)
    
    
if __name__ == '__main__':
    # print("Starting MCP server...")
    # mcp.run(transport='stdio')
    print(get_weather_data('China'))
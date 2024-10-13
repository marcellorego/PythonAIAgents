from json import dumps

import os
import requests
from langchain_core.tools import tool
from pydantic import BaseModel, Field

class WeatherInput(BaseModel):
    location: str = Field(description="Must be a valid location in city format.")

@tool("get_weather", args_schema=WeatherInput)
def get_weather(location: str) -> str:
    """Get the current weather for a specified location."""
    if not location:
        return (
            "Please provide a location and call the get_current_weather_function again."
        )
    api_params = {
        "key": os.environ.get("WEATHER_API_KEY"),
        "q": location,
        "aqi": "no",
        "alerts": "no",
    }
    response: requests.models.Response = requests.get(
        "http://api.weatherapi.com/v1/current.json", params=api_params
    )
    str_response: str = dumps(response.json())
    return str_response

# if __name__ == "__main__":
#     from dotenv import load_dotenv, find_dotenv
#     load_dotenv(find_dotenv())
#     print(get_weather("New York"))
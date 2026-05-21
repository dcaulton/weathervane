"""Weather tool for the Weathervane agent.

This is a clean, well-documented tool that the LLM can call.
"""

from typing import Any

import structlog
from langchain_core.tools import tool
from openmeteo_requests import Client

from weathervane.agent.config import settings

logger = structlog.get_logger(__name__)

# Initialize Open-Meteo client once
openmeteo = Client()


@tool
def get_weather(
    latitude: float | None = None,
    longitude: float | None = None,
    forecast_days: int = 7,
    past_days: int = 0,
) -> dict[str, Any]:
    """Get current weather, forecast, and historical data for a location.

    If latitude/longitude not provided, uses the default location from config.

    This is one of the core tools the agent will use heavily.
    """

    lat = latitude or settings.default_latitude
    lon = longitude or settings.default_longitude

    try:
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": [
                "temperature_2m",
                "relative_humidity_2m",
                "apparent_temperature",
                "precipitation",
                "weather_code",
                "wind_speed_10m",
            ],
            "hourly": [
                "temperature_2m",
                "precipitation_probability",
                "wind_speed_10m",
            ],
            "daily": [
                "temperature_2m_max",
                "temperature_2m_min",
                "precipitation_sum",
                "weather_code",
            ],
            "forecast_days": forecast_days,
            "past_days": past_days,
        }

        responses = openmeteo.weather_api(settings.openmeteo_url + "/forecast", params=params)

        # For simplicity, we'll return the first (and usually only) response
        response = responses[0]

        result = {
            "location": {"lat": latitude, "lon": longitude},
            "current": {
                "temperature": response.Current().Variables(0).Value(),
                "humidity": response.Current().Variables(1).Value(),
                "feels_like": response.Current().Variables(2).Value(),
                "precipitation": response.Current().Variables(3).Value(),
                "weather_code": int(response.Current().Variables(4).Value()),
                "wind_speed": response.Current().Variables(5).Value(),
            },
            "daily_forecast": [],  # We can expand this later
            "source": "Open-Meteo",
        }

        logger.info("Weather fetched successfully", lat=latitude, lon=longitude)
        return result

    except Exception as e:
        logger.error("Weather fetch failed", error=str(e))
        return {"error": str(e)}


# For easy testing / debugging
if __name__ == "__main__":
    print("=== Testing Weather Tool ===")
    result = get_weather.invoke({})
    print(result)

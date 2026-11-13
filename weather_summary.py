"""
Week 1 Lab — Calls a public REST API (OpenWeatherMap current weather),
parses the JSON response, stores the results in a small class, and prints
a formatted summary.

The API key is read from a .env file (never hard-coded).
"""

import argparse
import os
import sys
from dataclasses import dataclass

import requests
from dotenv import load_dotenv

API_URL = "https://api.openweathermap.org/data/2.5/weather"
REQUEST_TIMEOUT_SECONDS = 10


class WeatherAPIError(Exception):
    """Raised when the API call fails or returns an unexpected response."""


@dataclass
class WeatherReport:
    """Holds the parsed results for one city."""

    city: str
    country: str
    temperature_c: float
    feels_like_c: float
    humidity_pct: int
    wind_speed_ms: float
    description: str

    @classmethod
    def from_json(cls, data: dict) -> "WeatherReport":
        """Build a WeatherReport from the raw JSON returned by the API."""
        try:
            return cls(
                city=data["name"],
                country=data["sys"]["country"],
                temperature_c=float(data["main"]["temp"]),
                feels_like_c=float(data["main"]["feels_like"]),
                humidity_pct=int(data["main"]["humidity"]),
                wind_speed_ms=float(data["wind"]["speed"]),
                description=data["weather"][0]["description"].capitalize(),
            )
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            raise WeatherAPIError(f"Unexpected response format: {exc}") from exc


class WeatherClient:
    """Thin wrapper around the REST endpoint."""

    def __init__(self, api_key: str):
        if not api_key:
            raise WeatherAPIError("API key is empty. Check your .env file.")
        self.api_key = api_key

    def get_weather(self, city: str) -> WeatherReport:
        params = {"q": city, "appid": self.api_key, "units": "metric"}
        try:
            response = requests.get(API_URL, params=params, timeout=REQUEST_TIMEOUT_SECONDS)
        except requests.RequestException as exc:
            # Request exceptions may contain the full URL, including the API key.
            raise WeatherAPIError(
                f"Network error for '{city}'. Check your connection and try again."
            ) from exc

        if response.status_code == 401:
            raise WeatherAPIError("Invalid API key (HTTP 401).")
        if response.status_code == 404:
            raise WeatherAPIError(f"City not found: '{city}'.")
        if not response.ok:
            raise WeatherAPIError(f"HTTP {response.status_code}: {response.text[:200]}")

        try:
            data = response.json()
        except requests.exceptions.JSONDecodeError as exc:
            raise WeatherAPIError("The weather service returned invalid JSON.") from exc

        return WeatherReport.from_json(data)


def print_summary(reports: list[WeatherReport]) -> None:
    """Print a formatted table of the collected reports."""
    header = f"{'City':<16}{'Country':<9}{'Temp (°C)':>10}{'Feels (°C)':>12}{'Humidity':>10}{'Wind (m/s)':>12}  Conditions"
    print("=" * len(header))
    print("Weather Summary".center(len(header)))
    print("=" * len(header))
    print(header)
    print("-" * len(header))
    for r in reports:
        print(
            f"{r.city:<16}{r.country:<9}{r.temperature_c:>10.1f}{r.feels_like_c:>12.1f}"
            f"{r.humidity_pct:>9}%{r.wind_speed_ms:>12.1f}  {r.description}"
        )
    print("=" * len(header))
    if reports:
        hottest = max(reports, key=lambda r: r.temperature_c)
        print(f"Hottest city: {hottest.city} ({hottest.temperature_c:.1f} °C)")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Print a weather summary for one or more cities.")
    parser.add_argument("cities", nargs="+", help="City names, e.g. Cairo Matrouh London")
    args = parser.parse_args(argv)

    load_dotenv()  # reads .env in the current folder
    api_key = os.getenv("OPENWEATHER_API_KEY", "")

    try:
        client = WeatherClient(api_key)
    except WeatherAPIError as exc:
        print(f"[error] {exc}", file=sys.stderr)
        return 1

    reports, failures = [], []
    for city in args.cities:
        try:
            reports.append(client.get_weather(city))
        except WeatherAPIError as exc:
            failures.append(str(exc))

    if reports:
        print_summary(reports)
    for message in failures:
        print(f"[error] {message}", file=sys.stderr)
    return 0 if reports else 1


if __name__ == "__main__":
    sys.exit(main())

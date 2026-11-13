# Week 1 Lab — REST API + JSON + Class

Calls the OpenWeatherMap current-weather REST API, parses the JSON response into a small `WeatherReport` class, and prints a formatted summary. The API key is read from a `.env` file.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env               # then put your real key in .env
```

Get a free key at openweathermap.org (the key can take a short while to activate).

## Run

```bash
python weather_summary.py Cairo Matrouh London
```

## Tests (offline)

```bash
pip install pytest
pytest -q
```

## Files

- `weather_summary.py`: API client, `WeatherReport` class, and printing.
- `test_weather_summary.py`: offline tests for parsing and validation.
- `.env.example`: template for the key. `.env` is git-ignored.

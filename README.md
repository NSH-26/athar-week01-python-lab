# Week 1 Lab — REST API + JSON + Class

Calls the OpenWeatherMap current-weather REST API, parses the JSON response into a small `WeatherReport` class, and prints a formatted summary. The API key is read from a `.env` file.

## Setup

Requires Python 3.10 or later.

Windows (Command Prompt):

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

macOS / Linux:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Then put your own OpenWeatherMap API key in the new `.env` file:

```
OPENWEATHER_API_KEY=your_actual_key
```

A free key is available at openweathermap.org. A new key can take up to two hours to activate; until then the API answers with HTTP 401.

## Run

```
python weather_summary.py Cairo
```

Several cities can be passed at once, for example `python weather_summary.py Cairo London`. Temperatures are in Celsius and wind speeds in metres per second.

## Tests (offline)

```
pip install pytest
python -m pytest -q
```

The tests use sample responses and simulated errors. They do not call the live API.

## Files

- `weather_summary.py`: API client, `WeatherReport` class, and printing.
- `test_weather_summary.py`: offline tests for parsing and error handling.
- `.env.example`: template for the key. `.env` is git-ignored.

"""Offline tests: they check parsing and error handling without calling the network."""

import pytest

from weather_summary import WeatherAPIError, WeatherClient, WeatherReport

SAMPLE = {
    "name": "Matrouh",
    "sys": {"country": "EG"},
    "main": {"temp": 21.4, "feels_like": 20.9, "humidity": 60},
    "wind": {"speed": 5.2},
    "weather": [{"description": "clear sky"}],
}


def test_from_json_parses_fields():
    r = WeatherReport.from_json(SAMPLE)
    assert r.city == "Matrouh"
    assert r.country == "EG"
    assert r.temperature_c == 21.4
    assert r.humidity_pct == 60
    assert r.description == "Clear sky"


def test_from_json_rejects_bad_payload():
    with pytest.raises(WeatherAPIError):
        WeatherReport.from_json({"name": "X"})


def test_empty_key_is_rejected():
    with pytest.raises(WeatherAPIError):
        WeatherClient("")

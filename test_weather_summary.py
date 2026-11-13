"""Offline tests: they check parsing and error handling without calling the network."""

import pytest
import requests

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


def test_invalid_json_is_reported_as_api_error(monkeypatch):
    class InvalidJSONResponse:
        status_code = 200
        ok = True

        def json(self):
            raise requests.exceptions.JSONDecodeError("Invalid JSON", "not json", 0)

    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: InvalidJSONResponse())
    with pytest.raises(WeatherAPIError, match="invalid JSON"):
        WeatherClient("dummy-test-key").get_weather("Matrouh")


def test_network_error_does_not_expose_api_key(monkeypatch):
    dummy_key = "DUMMY_KEY_NOT_A_SECRET"

    def fail_request(*args, **kwargs):
        raise requests.ConnectionError(
            f"Failed URL https://api.openweathermap.org/data/2.5/weather?appid={dummy_key}"
        )

    monkeypatch.setattr(requests, "get", fail_request)
    with pytest.raises(WeatherAPIError, match="Network error") as error:
        WeatherClient(dummy_key).get_weather("Matrouh")
    assert dummy_key not in str(error.value)

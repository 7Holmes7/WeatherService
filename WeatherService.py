from typing import Optional
from pyowm import OWM
from pyowm.commons.enums import SubscriptionTypeEnum

# openweathermap.org token
RESOURCE_KEY = "439d4b804bc8187953eb36d2a8c26a02"


class WeatherService:

    def __init__(self, token: Optional[str] = None):
        # self._session = Session()
        self._token = token if token else RESOURCE_KEY
        self._manager = None

    def _initManagerByCity(self, city: str):
        config = {
            'subscription_type': SubscriptionTypeEnum.FREE,
            'language': 'ru',
            'connection': {
                'use_ssl': True,
                'verify_ssl_certs': True,
                'use_proxy': False,
                'timeout_secs': 5
            },
            'proxies': {
                'http': 'http://user:pass@host:port',
                'https': 'socks5://user:pass@host:port'
            }
        }
        self._manager = OWM(self._token, config=config).weather_manager().weather_at_place(city)

    def getCurrentWeatherByCity(self, city: str) -> dict:
        if self._manager is None:
            self._initManagerByCity(city)
        weather = self._manager.weather
        return dict(temperature=round(weather.temperature('celsius').get('temp')),
                    status=weather.detailed_status,
                    pressure=weather.pressure.get('press'),
                    humidity=weather.humidity,
                    icon=weather.weather_icon_name,
                    wind=weather.wind().get('speed'))

    def getLocationByCity(self, city: str) -> dict:
        if self._manager is None:
            self._initManagerByCity(city)
        location = self._manager.location
        return dict(name=location.name, country=location.country.lower())

    def analyzeWeather(self, weather: dict):
        pass

    def __repr__(self):
        return "This is service object"

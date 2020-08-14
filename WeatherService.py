from typing import Optional
from pyowm import OWM
from pyowm.weatherapi25.observation import Observation
from pyowm.commons.enums import SubscriptionTypeEnum

# openweathermap.org token
RESOURCE_KEY = "439d4b804bc8187953eb36d2a8c26a02"


class WeatherService:

    def __init__(self, token: Optional[str] = None):
        # self._session = Session()
        self._token: str = token if token else RESOURCE_KEY
        self._manager: Optional[Observation] = None

    def _initManagerByCity(self, city: str):

        if self._manager is None:
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
        self._initManagerByCity(city)
        weather = self._manager.weather
        return dict(temperature=round(weather.temperature('celsius').get('temp')),
                    status=weather.detailed_status,
                    pressure=weather.pressure.get('press'),
                    humidity=weather.humidity,
                    icon=weather.weather_icon_name,
                    wind=weather.wind().get('speed'))

    def getLocationByCity(self, city: str) -> dict:
        self._initManagerByCity(city)
        location = self._manager.location
        return dict(name=location.name, country=location.country.lower())

    @staticmethod
    def analyzeWeather(weather: dict) -> str:

        clothes = {'head': None,
                   'torso': None,
                   'hands': None,
                   'legs': None,
                   'accessory': None}

        temperature = weather.get('temperature')

        if temperature < -15:
            clothes['head'] = "Меховая шапка"
            clothes['torso'] = "Тулуп"
            clothes['hands'] = "Варежки"
            clothes['legs'] = "Валенки"
            clothes['accessory'] = "Портативный обогреватель"
        elif temperature in range(-15, 1):
            clothes['head'] = "Шапка"
            clothes['torso'] = "Куртка"
            clothes['hands'] = "Перчатки"
            clothes['legs'] = "Утепленные ботинки"
            clothes['accessory'] = "Шарф"
        elif temperature in range(1, 15):
            clothes['torso'] = "Пальто"
            clothes['legs'] = "Джинсы"
        elif temperature in range(15, 25):
            clothes['torso'] = "Толстовка"
            clothes['legs'] = "Джинсы"
            clothes['accessory'] = "Кроссовки"
        else:
            clothes['head'] = "Кепка"
            clothes['torso'] = "Майка"
            clothes['legs'] = "Шорты"

        if "дождь" in weather.get('status'):
            clothes['accessory'] = "Зонт"

        recommendation = "Рекомендуем взять следующие вещи: "
        for element in clothes.values():
            if element:
                recommendation += f"{element},"
        return recommendation[:-1]

    def __repr__(self):
        return "This is service object"


if __name__ == "__main__":
    # from app import API_KEY
    #
    # service = WeatherService(API_KEY)
    # weather = service.getCurrentWeatherByCity('Гренландия')
    # print(weather)
    # message = service.analyzeWeather(weather)
    # print(message)
    pass

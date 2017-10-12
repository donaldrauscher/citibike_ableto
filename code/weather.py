import requests as r
import typing
import datetime

"""
DEPREACTED
Weather is not used in model, anymore
"""


class WeatherConditions(typing.NamedTuple):
    fog: bool = False
    rain: bool = False
    snow: bool = False


class WeatherInfo(typing.NamedTuple):
    date: datetime.date
    hour: int
    temp: int
    prcp: float
    conditions: WeatherConditions


def __parse_weather(description):
    if 'Fog' in description or 'Haze' in description:
        return WeatherConditions(fog=True)
    elif 'Rain' in description or 'Thunderstorm' in description:
        return WeatherConditions(rain=True)
    elif 'Sleet' in description or 'Snow' in description:
        return WeatherConditions(snow=True)
    else:
        return WeatherConditions()


class WeatherService:
    def __init__(self, state='NY', city='New York', api_key='7aace0916fed8b21'):
        self.state = state
        self.city = city
        self.api_key = api_key
        self.cache: typing.Dict[typing.Tuple[datetime.date, int], WeatherInfo] = {}

    def __cache_key(self) -> typing.Tuple[datetime.date, int]:
        dt = datetime.datetime.now()
        cache_key = (dt.date(), dt.hour)
        return cache_key

    def __fetch_from_cache(self) -> typing.Optional[WeatherInfo]:
        cache_key = self.__cache_key()

        if cache_key in self.cache:
            return self.cache[cache_key]
        return None

    def get_weather(self) -> WeatherInfo:

        cached_res = self.__fetch_from_cache()

        if cached_res:
            return cached_res
        else:
            res = self.__query_api()
            if res:
                key = self.__cache_key()

                dt = datetime.datetime.now()
                weather_res = WeatherInfo(
                    conditions=res['weather']
                    , temp=res['temp']
                    , prcp=res['prcp']
                    , date=dt.date()
                    , hour=dt.hour
                )
                self.cache[key] = weather_res
                return weather_res
            else:
                return self.__default_weather()

    def __query_api(self):
        res = r.get(
            "http://api.wunderground.com/api/{}/conditions/q/{}/{}.json".format(self.api_key, self.state, self.city))

        if res.status_code == 200:
            w_p = res.json()['current_observation']

            d = {
                'temp': w_p['temp_f']
                , 'prcp': w_p['precip_today_in']

            }

            weather = w_p['weather']
            d['weather'] = self.__parse_weather(weather)
            return d
        else:
            return None

    def __parse_weather(self, description: str) -> WeatherConditions:
        if 'Fog' in description or 'Haze' in description:
            return WeatherConditions(fog=True)
        elif 'Rain' in description or 'Thunderstorm' in description:
            return WeatherConditions(rain=True)
        elif 'Sleet' in description or 'Snow' in description:
            return WeatherConditions(snow=True)
        else:
            return WeatherConditions()

    def __default_weather(self):
        dt = datetime.datetime.now()
        return WeatherInfo(
            date=dt.date(),
            hour=dt.hour,
            temp=70,
            prcp=70,
            conditions=WeatherConditions()
        )

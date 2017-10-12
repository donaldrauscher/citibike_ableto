import datetime
from typing import List

import pytz
from code.models import ModelOutput, ModelInput

from code.ml_model import MLModel
from code.station import StationService
from code.weather import WeatherService


class PredictionService:
    """
    Service that interacts with ml model
    """

    def __init__(self):
        self.ml_model = MLModel()
        self.station_service = StationService()
        self.weather_service = WeatherService()

    def predict(self, arriving: bool, hour: int) -> List[ModelOutput]:
        """
        Predict the best station to use

        :param arriving: true = arriving
        :param hour:
        :return: Sorted list where entry[0] is the best
        """

        # get the hour in est time zone (model expects hour is est)
        dt = datetime.datetime.now()
        eastern = pytz.timezone('US/Eastern')
        est_hour = eastern.localize(dt).hour

        current_hour = est_hour
        station_infos = self.station_service.get_capacity()

        # if predicted hour is the same as current, use the latest info from citibike
        if current_hour == hour:
            if arriving: # want more free docks
                best_station = sorted(station_infos.values(), key=lambda x: x.available_docks, reverse=True)
            else: # want more free bikes
                best_station = sorted(station_infos.values(), key=lambda x: x.available_bikes, reverse=True)

            model_outputs = [ModelOutput(station_name=s.station_name, station_docks=s.available_docks,
                                         station_bikes=s.available_bikes) for s in best_station]
        else:
            inputs = []
            # prepare inputs/features to the model
            for station in station_infos.values():
                mi = ModelInput(year=dt.year, month=dt.month, week=dt.isocalendar()[1], day_of_week=dt.weekday(),
                                hour=dt.hour, station_id=station.station_id)
                inputs.append(mi)

            # parse output (flow) from model
            predicted_flows = self.ml_model.predict(inputs)
            model_outputs = [ModelOutput(station_name=s.station_name, flow=float(flow)) for (s, flow) in
                             zip(station_infos.values(), predicted_flows)]

            # positive flow -> more bikes in station
            # negative flow -> less bikes in station
            if arriving: # want more free docks
                model_outputs = sorted(model_outputs, key=lambda x: x.flow, reverse=True)
            else:
                model_outputs = sorted(model_outputs, key=lambda x: x.flow, reverse=False)

        return model_outputs

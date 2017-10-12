import typing
import requests as r
import time


class StationCapacityInfo(typing.NamedTuple):
    station_id: str
    name: str
    capacity: int = 0


class StationInfo(typing.NamedTuple):
    station_id: str
    station_name: str
    capacity: int = None
    available_docks: int = None
    available_bikes: int = None


class StationService:
    """
    Citbike Api Client
    """

    def __init__(self):
        self.last_updated = None
        self.current_station_info = None
        self.ableto_stations = self.__stations_near_ableto()
        self.station_capacity_info = self.__station_capacity()
        self.current_station_info = None

    def get_capacity(self) -> typing.Dict[str, StationInfo]:
        current_time = time.time()
        min_seconds_ttl = 60
        # If info in cache is stale, update
        if self.last_updated is None or (current_time - self.last_updated) > min_seconds_ttl:
            self.current_station_info = self.__query_api()
        return self.current_station_info

    def __query_api(self) -> typing.Dict[str, StationInfo]:
        """
        Get current bike/dock status for stations near offic
        :return:
        """
        res = r.get("https://gbfs.citibikenyc.com/gbfs/en/station_status.json")
        station_infos = res.json()['data']['stations']
        station_infos = [s for s in station_infos if s['station_id'] in self.ableto_stations]

        full_station_info = {}
        for s in station_infos:
            station_id = s['station_id']
            capacity = self.station_capacity_info[station_id].capacity
            name = self.station_capacity_info[station_id].name

            si = StationInfo(station_id=s['station_id'], available_docks=s['num_docks_available'],
                             available_bikes=s['num_bikes_available'],
                             capacity=capacity, station_name=name)
            full_station_info[station_id] = si

        return full_station_info

    def __station_capacity(self) -> typing.Dict[str, StationCapacityInfo]:
        """
        Returns Station info and total capacity
        :return:
        """
        res = r.get("https://gbfs.citibikenyc.com/gbfs/en/station_information.json")
        station_infos = res.json()['data']["stations"]

        station_infos = [s for s in station_infos if s['station_id'] in self.ableto_stations]

        station_map = {
            s['station_id']: StationCapacityInfo(station_id=s['station_id'], capacity=s['capacity'], name=s['name']) for
            s
            in
            station_infos}

        return station_map

    def __stations_near_ableto(self):
        """
        Station ids of stations near office
        :return:
        """
        return ["3635", "523", "490", "477", "529"]

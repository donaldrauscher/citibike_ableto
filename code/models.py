import typing


class ModelInput(typing.NamedTuple):
    """
    Expected fields to machine learning model
    """
    year: int
    month: int
    week: int
    hour: int
    day_of_week: int
    station_id: str


class ModelOutput(typing.NamedTuple):
    """
    Expected Api Response model
    """
    station_name: str
    station_bikes: int = None
    station_docks: int = None
    flow: float = None

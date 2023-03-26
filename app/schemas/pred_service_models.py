from typing import List

from pydantic import BaseModel


class ObservationModel(BaseModel):
    flight_id: int
    OPERA: str
    TIPOVUELO: str
    MES: int
    hour: int


class ObservationsModelModelBody(BaseModel):
    flights: List[ObservationModel]

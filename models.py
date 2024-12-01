from pydantic import BaseModel
from typing import List

class SensorData(BaseModel):
    x: float
    y: float
    z: float
    timestamp: float

class SensorInput(BaseModel):
    gyroscope: List[SensorData]
    accelerometer: List[SensorData]


class Item(BaseModel):
    name: str
    description: str
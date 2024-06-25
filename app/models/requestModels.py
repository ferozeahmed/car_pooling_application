from pydantic import BaseModel
from typing import List


# Create model for vehicle request
class Vehicle(BaseModel):
    type: str
    seats_offered: str


# Create model for users request
class User(BaseModel):
    first_name: str
    last_name: str
    mail_id: str
    mobile: str
    address: str
    latitude: float
    longitude: float
    vehicle: List[Vehicle]


# Create model for ride request
class Ride(BaseModel):
    mail_id: str
    latitude: float
    longitude: float
    destination: str
    seats_offered: int
    riders: List[str]
    date: str
    status: str
    vehicle: str

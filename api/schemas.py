from pydantic import BaseModel, EmailStr
from datetime import datetime

# class Image(BaseModel):
#     url: HttpUrl
#     name: str

class UserBase(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    email: EmailStr

class CreateUser(UserBase):
    password: str

class GetUser(UserBase):
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class VehicleBase(BaseModel):
    name: str
    model: str
    # rating: float = mapped_column(server_default=0.0)
    price: float
    motor_power: str
    motor_type: str
    v_range: str
    charging_time: str
    battery_capacity: str
    top_speed: str
    kerb_weight: str
    tyre_type: str
    ground_clearance: str
    fast_charging: bool
    wheels_type: str
    trip_meter: str
    starting: str
    speedometer: str
    clock: bool

class CreateVehicle(VehicleBase):
    pass
    # image: Image | None = None

class GetVehicle(VehicleBase):
    vehicle_id: int
    created_at: datetime
    class Config:
        orm_mode = True

class CreateCompany(BaseModel):
    name: str
    # vehicles: list[CreateVehicle] | None = None

class GetCompanies(BaseModel):
    company_id: int
    name: str
    class Config:
        orm_mode = True

class GetCompanyVehicles(BaseModel):
    company_id: int
    name: str
    vehicles: list[GetVehicle] | None = None
    class Config:
        orm_mode = True

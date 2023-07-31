from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime
from sqlalchemy import ForeignKey, func, DateTime

class Base(DeclarativeBase):
    pass

class Users(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    phone_number: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    vehicles: Mapped[list["Vehicles"]] = relationship(back_populates="user")
    is_dealer: Mapped[bool] = mapped_column(server_default="FALSE")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

class Companies(Base):
    __tablename__ = "companies"
    
    company_id: Mapped[int] = mapped_column(primary_key=True)
    # company_img: Mapped[]
    name: Mapped[str]
    vehicles: Mapped[list["Vehicles"]] = relationship(back_populates="company")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

class Vehicles(Base):
    __tablename__ = "vehicles"

    vehicle_id: Mapped[int] = mapped_column(primary_key=True)
    # vehicle_image: Mapped[]
    name: Mapped[str]
    model: Mapped[str]
    # rating: Mapped[float] = mapped_column(server_default=0.0)
    price: Mapped[float]
    motor_power: Mapped[str]
    motor_type: Mapped[str]
    v_range: Mapped[str]
    charging_time: Mapped[str]
    battery_capacity: Mapped[str]
    top_speed: Mapped[str]
    kerb_weight: Mapped[str]
    tyre_type: Mapped[str]
    ground_clearance: Mapped[str]
    fast_charging: Mapped[bool] = mapped_column(server_default="FALSE")
    wheels_type: Mapped[str]
    trip_meter: Mapped[str]
    starting: Mapped[str]
    speedometer: Mapped[str]
    clock: Mapped[bool] = mapped_column(server_default="FALSE")

    additional_fields : Mapped[list["AdditionalFields"] | None] = relationship()
    user_id: Mapped[int | None] = mapped_column(ForeignKey('users.user_id'))
    user: Mapped[Users | None] = relationship(back_populates='vehicles')
    company_id: Mapped[int | None] = mapped_column(ForeignKey('companies.company_id'))
    company: Mapped[Companies | None] = relationship(back_populates='vehicles')
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

class AdditionalFields(Base):
    __tablename__ = "additional_fields"

    field_id: Mapped[int] = mapped_column(primary_key=True)
    field_name: Mapped[str]
    field_value: Mapped[str]
    vehicle_id: Mapped["Vehicles"] = mapped_column(ForeignKey('vehicles.vehicle_id'))

# class BusinessUsers(Base):
#     __tablename__ = "businessusers"
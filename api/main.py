import random
from fastapi import FastAPI, HTTPException, status, Depends
from .database import engine, get_db
from . import models, schemas
from sqlalchemy import select
from sqlalchemy.orm import Session, load_only
from .routers import auth, users

#Create non-existent tables in the database
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)

@app.get("/")
async def root():
    return {"message": "Okaya API"}

#Search
@app.get("/search/")
async def search_field(db: Session = Depends(get_db)):
    pass

#Get all companies
@app.get("/companies/", response_model=list[schemas.GetCompanies])
async def list_companies(db: Session = Depends(get_db)):
    query = select(models.Companies).options(load_only(models.Companies.company_id, models.Companies.name))
    c_list = db.scalars(query).all()

    return c_list

# Get all vehicles of a specific company
@app.get("/companies/{company_id}/vehicles/", response_model=schemas.GetCompanyVehicles)
async def get_company_electric_vehicles(company_id: int, db: Session = Depends(get_db)):
    company = db.get(models.Companies, company_id)

    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Company with id {company_id} was not found")
        
    return company

# Get a specific electric vehicle by ID
@app.get("/companies/{company_id}/vehicles/{vehicle_id}/", response_model=schemas.GetVehicle)
async def get_electric_vehicle(company_id: int, vehicle_id: int, db: Session = Depends(get_db)):
    get_vehicle = select(models.Vehicles).join(models.Companies).where(models.Vehicles.vehicle_id == vehicle_id, models.Companies.company_id == company_id).limit(1)
    vehicle = db.scalars(get_vehicle).first()

    if not vehicle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The Vehicle or Company does not exist")
    
    return vehicle

#Create new company
@app.post("/companies/", status_code=status.HTTP_201_CREATED)
async def create_company(data: schemas.CreateCompany, db: Session = Depends(get_db)):
    company = db.scalars(select(models.Companies).where(models.Companies.name == data.name).limit(1)).first()
    if company:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Company already exists")
    
    new_company = models.Companies(**data.dict())
    db.add(new_company)
    db.commit()

    return {"message": "Created Successfully"}

# Create a new electric vehicle
@app.post("/companies/{company_id}/vehicles/", status_code=status.HTTP_201_CREATED)
async def create_electric_vehicle(company_id:int, vehicle: schemas.CreateVehicle, db: Session = Depends(get_db)):
    company = db.get(models.Companies, company_id)
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Company with ID {company_id} does not exist")
    
    new_vehicle = models.Vehicles(**vehicle.dict())
    company.vehicles = new_vehicle
    db.commit()
    db.refresh(company)
    
    return new_vehicle

# Update an existing electric vehicle
@app.put("companies/{company_id}/vehicles/{vehicle_id}")
async def update_electric_vehicle(company_id:int, vehicle_id: int, vehicle: schemas.GetVehicle, db: Session = Depends(get_db)):
    company_vehicle = select(models.Vehicles).join(models.Companies).where(models.Vehicles.vehicle_id == vehicle_id, models.Companies.company_id == company_id).limit(1)

    if not company_vehicle:
        raise HTTPException(status_code=404, detail="Electric Vehicle not found")
    
    for field, value in vehicle.dict().items():
        setattr(company_vehicle, field, value)
    
    db.commit()
    db.refresh(company_vehicle)

    return company_vehicle

#Delete an existing company and all it's vehicles
# @app.delete("companies/{company_id}")
# async def delete_electric_vehicle(*vehicle_id: int):
#     for index, vehicle in enumerate(vehicles_company):
#         if vehicle.id == vehicle_id:
#             del vehicles_company[index]
#             return {"message": "Electric Vehicle deleted successfully"}
#     raise HTTPException(status_code=404, detail="Electric Vehicle not found")

# # Delete an existing electric vehicle
# @app.delete("companies/{company_id}/vehicles/{vehicle_id}")
# async def delete_electric_vehicle(company_id:int, vehicle_id: int):
#     for index, vehicle in enumerate(vehicles_company):
#         if vehicle.id == vehicle_id:
#             del vehicles_company[index]
#             return {"message": "Electric Vehicle deleted successfully"}
#     raise HTTPException(status_code=404, detail="Electric Vehicle not found")


# @app.post('/companies/{company_id}/vehicles/{vehicle_id}/rate')
# async def rate_vehicle(company_id: int, vehicle_id: int, rating: float):
#     pass

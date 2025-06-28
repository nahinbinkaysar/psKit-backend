from fastapi import FastAPI, HTTPException, Depends, Body
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from datetime import datetime, timedelta
import jwt
from typing import Optional, List
from fastapi.middleware.cors import CORSMiddleware
import time
app = FastAPI()
# Allow all origins for demonstration purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can specify your allowed origins here
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


# # Database setup hehe
# DATABASE_URL = "sqlite:///./todo.db"
# CUSTOMER_DATABASE_URL = "sqlite:///./customer.db"
# ADDRESS_DATABASE_URL = "sqlite:///./address.db"
# engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
# customer_engine = create_engine(CUSTOMER_DATABASE_URL, connect_args={"check_same_thread": False})
# address_engine = create_engine(ADDRESS_DATABASE_URL, connect_args={"check_same_thread": False})
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# CustomerSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=customer_engine)
# AddressSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=address_engine)
# Base = declarative_base()
# CustomerBase = declarative_base()
# AddressBase = declarative_base()

# SECRET_KEY = "mysecretkey"
# ALGORITHM = "HS256"

# # Models
# class User(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, nullable=False)
#     email = Column(String, unique=True, index=True, nullable=False)
#     phone = Column(String, unique=True, index=True)
#     username = Column(String, unique=True, index=True, nullable=False)
#     password = Column(String, nullable=False)
#     profile_picture = Column(String, nullable=True)

# class Customer(CustomerBase):
#     __tablename__ = "customers"
#     id = Column(Integer, primary_key=True, index=True)
#     facebook_id = Column(String, nullable=True)  # changed to nullable=True
#     email = Column(String, nullable=True)        # changed to nullable=True
#     license_key = Column(String, nullable=True)  # changed to nullable=True
#     name = Column(String, nullable=True)         # changed to nullable=True
#     phone = Column(String, nullable=True)        # changed to nullable=True
#     username = Column(String, nullable=True)     # changed to nullable=True
#     password = Column(String, nullable=True)     # changed to nullable=True
#     payment = Column(String, nullable=True)
#     transaction_id = Column(String, nullable=True)
#     date = Column(String, nullable=True)

# class Address(AddressBase):
#     __tablename__ = "addresses"
#     id = Column(Integer, primary_key=True, index=True)
#     street = Column(String, nullable=False)
#     city = Column(String, nullable=False)
#     province = Column(String, nullable=False)
#     zip = Column(String, nullable=False)
#     used = Column(Boolean, default=False)
#     used_at = Column(DateTime, nullable=True)  # Track when address was used
#     used_by = Column(String, nullable=True)    # Track who used the address

# Base.metadata.create_all(bind=engine)
# CustomerBase.metadata.create_all(bind=customer_engine)
# AddressBase.metadata.create_all(bind=address_engine)

# # Schemas
# class UserCreate(BaseModel):
#     name: str
#     email: str
#     phone: Optional[str]
#     username: str
#     password: str
#     profile_picture: Optional[str]

# class UserLogin(BaseModel):
#     username: str
#     password: str

# class UserUpdate(BaseModel):
#     name: Optional[str]
#     email: Optional[str]
#     phone: Optional[str]
#     profile_picture: Optional[str]

# class CustomerCreate(BaseModel):
#     facebook_id: Optional[str] = None
#     email: Optional[str] = None
#     license_key: Optional[str] = None
#     name: Optional[str] = None
#     phone: Optional[str] = None
#     username: Optional[str] = None
#     password: Optional[str] = None
#     payment: Optional[str] = None
#     transaction_id: Optional[str] = None
#     date: Optional[str] = None

# class UserUpdateCredentials(BaseModel):
#     username: Optional[str] = None
#     password: Optional[str] = None

# class CustomerUpdate(BaseModel):
#     facebook_id: Optional[str] = None
#     email: Optional[str] = None
#     license_key: Optional[str] = None
#     name: Optional[str] = None
#     phone: Optional[str] = None
#     username: Optional[str] = None
#     password: Optional[str] = None
#     payment: Optional[str] = None
#     transaction_id: Optional[str] = None
#     date: Optional[str] = None

# # Dependency
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# def get_customer_db():
#     db = CustomerSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# def get_address_db():
#     db = AddressSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# # API Endpoints

# @app.post("/register")
# def register(user: UserCreate, db: Session = Depends(get_db)):
#     db_user = User(
#         name=user.name,
#         email=user.email,
#         phone=user.phone,
#         username=user.username,
#         password=user.password,
#         profile_picture=user.profile_picture,
#     )
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return {"message": "User registered successfully"}

# def create_jwt_token(username: str):
#     payload = {"sub": username, "exp": datetime.utcnow() + timedelta(days=1)}
#     return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

# @app.post("/login")
# def login(user: UserLogin, db: Session = Depends(get_db)):
#     db_user = db.query(User).filter(User.username == user.username).first()
#     if not db_user or db_user.password != user.password:
#         raise HTTPException(status_code=400, detail="Invalid credentials")
#     token = create_jwt_token(db_user.username)
#     return {"access_token": token, "token_type": "bearer"}

# @app.post("/customer")
# def create_customer(customer: CustomerCreate, db: Session = Depends(get_customer_db)):
#     # If username is provided, check for uniqueness
#     if customer.username:
#         existing = db.query(Customer).filter(Customer.username == customer.username).first()
#         if existing:
#             raise HTTPException(status_code=400, detail="Username already exists")
#     db_customer = Customer(**customer.dict())
#     db.add(db_customer)
#     db.commit()
#     db.refresh(db_customer)
#     # Return only the new customer id
#     return {"id": db_customer.id}

@app.get("/message")
def message():
    time.sleep(2)
    return {
        "message": "Hello there!"
    }

# @app.get("/profile/{username}")
# def get_profile(username: str, db: Session = Depends(get_db)):
#     db_user = db.query(User).filter(User.username == username).first()
#     if not db_user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return {
#         "username": db_user.username,
#         "password": db_user.password,
#     }

# @app.put("/profile/{username}")
# def update_profile(username: str, creds: UserUpdateCredentials = Body(...), db: Session = Depends(get_db)):
#     db_user = db.query(User).filter(User.username == username).first()
#     if not db_user:
#         raise HTTPException(status_code=404, detail="User not found")
#     update_data = creds.dict(exclude_unset=True)
#     if "username" in update_data:
#         # Check for username uniqueness
#         existing = db.query(User).filter(User.username == update_data["username"]).first()
#         if existing and existing.id != db_user.id:
#             raise HTTPException(status_code=400, detail="Username already exists")
#         db_user.username = update_data["username"]
#     if "password" in update_data:
#         db_user.password = update_data["password"]
#     db.commit()
#     db.refresh(db_user)
#     return {"message": "Profile updated successfully"}

# @app.get("/customers")
# def get_all_customers(db: Session = Depends(get_customer_db)):
#     customers = db.query(Customer).all()
#     return [
#         {
#             "id": c.id,  # Include the customer ID in the response
#             "facebook_id": c.facebook_id,
#             "email": c.email,
#             "license_key": c.license_key,
#             "name": c.name,
#             "phone": c.phone,
#             "username": c.username,
#             "password": c.password,
#             "payment": c.payment,
#             "transaction_id": c.transaction_id,
#             "date": c.date,
#         }
#         for c in customers
#     ]

# @app.get("/address/by-index/{index}")
# def get_address_by_index(index: int, db: Session = Depends(get_address_db)):
#     addresses = db.query(Address).order_by(Address.id).all()
#     if not addresses or index < 0 or index >= len(addresses):
#         raise HTTPException(status_code=404, detail="Address index out of range")
#     address = addresses[index]
#     return {
#         "id": address.id,
#         "street": address.street,
#         "city": address.city,
#         "province": address.province,
#         "zip": address.zip
#     }

# @app.put("/customer/{customer_id}")
# def update_customer(customer_id: int, customer: CustomerUpdate, db: Session = Depends(get_customer_db)):
#     db_customer = db.query(Customer).filter(Customer.id == customer_id).first()
#     if not db_customer:
#         raise HTTPException(status_code=404, detail="Customer not found")
#     update_data = customer.dict(exclude_unset=True)
#     for key, value in update_data.items():
#         setattr(db_customer, key, value)
#     db.commit()
#     db.refresh(db_customer)
#     return {"message": "Customer updated successfully"}

# @app.get("/customer/{customer_id}")
# def get_customer_by_id(customer_id: int, db: Session = Depends(get_customer_db)):
#     db_customer = db.query(Customer).filter(Customer.id == customer_id).first()
#     if not db_customer:
#         raise HTTPException(status_code=404, detail="Customer not found")
#     return {
#         "id": db_customer.id,
#         "facebook_id": db_customer.facebook_id,
#         "email": db_customer.email,
#         "license_key": db_customer.license_key,
#         "name": db_customer.name,
#         "phone": db_customer.phone,
#         "username": db_customer.username,
#         "password": db_customer.password,
#         "payment": db_customer.payment,
#         "transaction_id": db_customer.transaction_id,
#         "date": db_customer.date,
#     }

# @app.delete("/customer/{customer_id}")
# def delete_customer(customer_id: int, db: Session = Depends(get_customer_db)):
#     db_customer = db.query(Customer).filter(Customer.id == customer_id).first()
#     if not db_customer:
#         raise HTTPException(status_code=404, detail="Customer not found")
#     db.delete(db_customer)
#     db.commit()
#     return {"message": "Customer deleted successfully"}
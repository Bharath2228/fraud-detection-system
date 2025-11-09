from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
from schemas import UserCreate
from database import engine, getDb
from utils import hashPassword, createAccessToken, verifyPassword, getCurrentUser

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI-Driven Fraud Detection System")
# app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Fraud Detection API is running successfully!"}

@app.post("/transactions/")
def create_transaction(amount: float, user_id: int, db: Session = Depends(getDb)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_transaction = models.Transaction(amount=amount, user_id=user_id)
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return new_transaction

@app.post("/register/")
def register_user(user: UserCreate, db: Session = Depends(getDb)):
    # Checking if the user already exists or not
    dbUser = db.query(models.User).filter(models.User.email == user.email).first()
    if dbUser:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hashing the password before saving it
    hashedPassword = hashPassword(user.password)

    # Creating a new user object and add to the DB
    newUser = models.User(username=user.username, email=user.email, password=hashedPassword)
    db.add(newUser)
    db.commit()
    db.refresh(newUser)

    accessToken = createAccessToken(data={"sub": newUser.email})

    return {"access_token": accessToken, "token_type": "bearer"}

# Creating the user login function
@app.post("/login/")
def login_user(user: UserCreate, db: Session = Depends(getDb)):
    dbUser = db.query(models.User).filter(models.User.email == user.email).first()

    if not dbUser or not verifyPassword(user.password, dbUser.password):
        raise HTTPException(status_code=400, detail="Invalid Credentials")

    accessToken = createAccessToken(data={"sub": user.email})

    return {"access_token": accessToken, "token_type": "bearer"}

@app.get("/transactions/")
def get_transactions(db: Session = Depends(getDb)):
    transactions = db.query(models.Transaction).all()
    return transactions

@app.post("/fraud_alert/")
def make_fraud_alert(transactionId: int, currentUser: models.User = Depends(getCurrentUser)):
    if currentUser.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")

    return {"message": f"Fraud alert for transaction {transactionId} marked by {currentUser.role}"}


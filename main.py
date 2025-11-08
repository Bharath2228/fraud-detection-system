from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI-Driven Fraud Detection System")
# app = FastAPI()
@app.get("/")

def read_root():
    return {"message": "Fraud Detection API is running successfully!"}

@app.post("/transactions/")
def create_transaction(amount: float, user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_transaction = models.Transaction(amount=amount, user_id=user_id)
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return new_transaction

@app.get("/transactions/")
def get_transactions(db: Session = Depends(get_db)):
    transactions = db.query(models.Transaction).all()
    return transactions
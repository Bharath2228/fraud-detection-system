from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

sqlAlchemyDatabaseURL = "postgresql://bharath:2801@localhost/fraud_detection_db"

engine = create_engine(sqlAlchemyDatabaseURL)

sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def getDb():
    db = sessionLocal()

    try:
        yield db
    finally:
        db.close()
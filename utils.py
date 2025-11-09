import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
import models
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from database import getDb

secretKey = "2801"
algorithm = "HS256"
accessTokenExpireMinutes = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

passwordContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hashing the password with bcrypt
def hashPassword(password: str) -> str:
    try:
        print(f"Original Password: {password}")
        password = password[:72]
        return passwordContext.hash(password)

    except ValueError as e:
        # Check if the error is due to password length
        if "password cannot be longer than 72 bytes" in str(e):
            raise ValueError("Password exceeds maximum length of 72 characters.")
        raise e

# Comparing the plain password with the stored hash
def verifyPassword(plainPassword: str, hashedPassword: str) -> bool:
    return passwordContext.verify(plainPassword, hashedPassword)

# Creating jwt access token using a dictionary of user data [ Including the expiration time ]
def createAccessToken(data: dict, expiresDelta: timedelta = timedelta(minutes=accessTokenExpireMinutes)):
    toEncode = data.copy()
    expire = datetime.utcnow() + expiresDelta  # need to something else
    toEncode.update({"exp": expire})
    encodedJwt = jwt.encode(toEncode, secretKey, algorithm=algorithm)
    return encodedJwt

# Decodes the token and verifies if its valid
def verifyAccessToken(token: str):
    try:
        payload = jwt.decode(token, secretKey, algorithms=[algorithm])
        return payload
    except jwt.PyJWTError:
        return None

def getCurrentUser(token: str = Depends(oauth2_scheme), db: Session = Depends(getDb)):
    credentials_exception = HTTPException(status_code=401, detail="Could not validate credentials")

    try:
        payload = verifyAccessToken(token)
        userEmail = payload.get("sub")
        if userEmail is None:
            raise credentials_exception

    except Exception:
        raise credentials_exception

    user = db.query(models.User).filter(models.User.email == userEmail).first()
    if user is None:
        raise credentials_exception
    return user

import jwt
# from passlib.context import CryptContext
import bcrypt
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

# passwordContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hashing the password with bcrypt
# def hashPassword(password: str) -> str:
#     try:
#         print(f"Original Password: {password}")
#         # bcrypt internally handles truncating passwords longer than 72 characters
#         return passwordContext.hash(password)
#     except Exception as e:
#         # Handle any other errors (like issues with the bcrypt library)
#         print(f"Error while hashing password: {str(e)}")
#         raise e

def hashPassword(password: str) -> str:
    try:
        print(f"Original Password: {password}")
        # bcrypt internally truncates passwords longer than 72 characters, so we don’t need to truncate manually
        password_bytes = password.encode('utf-8')

        # Generate a salt and hash the password
        hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
        return hashed_password.decode('utf-8')  # Convert the hashed password back to string

    except Exception as e:
        # Handle any errors related to bcrypt
        print(f"Error while hashing password: {str(e)}")
        raise e

# Comparing the plain password with the stored hash
# def verifyPassword(plainPassword: str, hashedPassword: str) -> bool:
#     return passwordContext.verify(plainPassword, hashedPassword)

def verifyPassword(plainPassword: str, hashedPassword: str) -> bool:
    try:
        # bcrypt expects both the plain password and the hashed password to be in bytes
        plainPassword_bytes = plainPassword.encode('utf-8')
        hashedPassword_bytes = hashedPassword.encode('utf-8')

        # Check if the plain password matches the hashed password
        return bcrypt.checkpw(plainPassword_bytes, hashedPassword_bytes)

    except Exception as e:
        # Handle any errors related to bcrypt
        print(f"Error while verifying password: {str(e)}")
        raise e

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

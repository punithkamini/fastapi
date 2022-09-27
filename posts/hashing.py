from passlib.context import CryptContext

pwd_cxt=CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hash():
    def bcrypt(password: str):
        hashed_password = pwd_cxt.hash(password)
        return hashed_password

    def verify_password(hashed_password, plain_password):
        return pwd_cxt.verify(plain_password,hashed_password)

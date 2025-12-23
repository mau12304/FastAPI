from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm 
import jwt 
from passlib.context import CryptContext
from datetime import datetime, timedelta
# pip install "passlib[bcrypt]" # Para encriptar contraseñas
#pip install pyjwt # Para manejar tokens JWT


router = APIRouter(
    prefix="/jwt_auth_users",
    tags=["jwt_auth_users"],
    responses={404: {"message": "Not found"}}
)# pip install fastapi
ALGORITHM = "HS256" # Algoritmo de encriptacion
ACCESS_TOKEN_DURATION = 1 # Duracion del token en minutos
#python -c "import secrets; print(secrets.token_hex(32))" #Generar una clave secreta de 32 bytes
SECRET = "33bdbdd8e53cd42f442e1e3e587e7338b5c4b588255cce340392e8769b3cec3a" # Clave secreta para encriptar el token
oauth2 = OAuth2PasswordBearer(tokenUrl="login") #OAuth2PasswordBearer Gestiona nuestra autenticacion
crypt = CryptContext(schemes=["bcrypt"], deprecated="auto", truncate_error=False)
 #criptografia #Proceso de incriptacion 

class User(BaseModel):
    username: str 
    full_name: str 
    email: str 
    disable: bool 

class UserDB(User):
    password: str


users_db ={
    "mauricio":{
        "username":"mauricio",
        "full_name": "Mauricio Lara",
        "email": "mauricilara@gmail.com",
        "disable": False,
        "password": "$2b$12$h4SNq32of.eKqko7gurvbOshtRsiD1EcDKMCXn2R2Sd5XJz785vWy"
    },
    "jose":{
        "username":"jose",
        "full_name": "Jose Diaz",
        "email": "josediaz@gmail.com",
        "disable": True,
        "password": "$2b$12$l/e7RxY/7wjWoU1Ex7pdrOkSd6jPRdVNNIcvfunZFX7d1hx0oJEXC"
    }
}
def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

async def auth_user(token: str = Depends(oauth2)): #Proceso de validacion del token
    exception = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Credenciales de autenticacion invalida",
                headers={"WWW-Authenticate": "Bearer"}
            )
    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub") # Nombre del usuario
        if username is None:
           raise exception
        
    except jwt.PyJWTError:
        raise exception
    
    return search_user(username)


async def current_user(user : User = Depends(auth_user)):
    if user.disable:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="USuario inactivo"
        )

    return user
    

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):# Dependencia de FastAPI para obtener los datos del formulario
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto"
        )
    
    user = search_user_db(form.username)
    if not crypt.verify(form.password, user.password ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta"
        )  

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)

    access_token = {
        "sub": user.username,
        "exp": expire
        }
    return {
        "access_token": jwt.encode(access_token, SECRET,algorithm=ALGORITHM) , 
        "token_type": "bearer"}


@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user

@router.get("/")
async def root():
    return {"message": "Hello World"}

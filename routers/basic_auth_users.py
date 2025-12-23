from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm #Modulo de autenticacion 

#OAuth2PasswordBearer Gestiona nuestra autenticacion
#OAuth2PasswordRequestForm capturar campos de inicio de sesion 
router =APIRouter(
    prefix="/basic_auth_users",
    tags=["basic_auth_users"],
    responses={404: {"message": "Not found"}}
)

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

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
        "password": "1234" #" #1234
    },
    "jose":{
        "username":"jose",
        "full_name": "Jose Diaz",
        "email": "josediaz@gmail.com",
        "disable": True,
        "password": "1204"  #1204 # 
    }
}


def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

async def current_user(token:str =Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Credenciales de autenticacion invalida",
            headers={"WWW-Authenticate": "Bearer"}
        )
    if user.disable:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="USuario inactivo"
        )

    return user


#Depends() dependencias si tienes la credenciales correctas o si se logeo correctamente
@router.post("/loginbasic")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto"
        )
    
    user = search_user_db(form.username)
    if not form.password == user.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta"
        )  
    
    return {"access_token": user.username, "token_type": "bearer"}

@router.get("/usersbasic/me")
async def me(user: User = Depends(current_user)):
    return user

# Clase en vídeo: https://youtu.be/_y9qQZXE24A

### Hola Mundo ###

# Documentación oficial: https://fastapi.tiangolo.com/es/

# Instala FastAPI: pip install "fastapi[all]"


from fastapi import FastAPI
from routers import users_db
from routers import products, users
from routers import basic_auth_users
from routers import jwt_auth_users, supabase

from fastapi.staticfiles import StaticFiles
# http://127.0.0.1:8000
app = FastAPI()

app.include_router(products.router)
app.include_router(users.router)
app.include_router(jwt_auth_users.router)
app.include_router(basic_auth_users.router)
app.include_router(users_db.router)
app.include_router(supabase.router)
app.mount("/statics", StaticFiles(directory="statics"), name="statics")  # Para servir archivos estaticos
 
@app.get("/") #get es una función de fastAPI que permite obtener información
#es una peticion GET, que siempre sucede al cargar la pagina
async def root():
    return "!Hola fastAPI¡"


@app.get("/url")
async def root():
    return {"url_curso": "https://www.youtube.com/"}

#Documentacion con Swagger http://127.0.0.1:8000/docs
#Documentacion con Redoc http://127.0.1:8000/redoc
# Inicia el server: uvicorn main:app --reload
# Detener el server: CTRL+C 
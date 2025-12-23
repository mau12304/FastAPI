from fastapi import APIRouter
from pydantic import BaseModel
from fastapi import HTTPException, status
from db.models.user import User
from db.schemas.user import user_schema, users_schema
from db.client import db_client
from bson import ObjectId
# USER DB API

router = APIRouter(prefix="/userdb", # prefijo para todas las rutas de este router
                   tags=["userdb"],                             # tags es para agrupar las rutas en la documentacion
                   responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}})  # Respuesta por defecto para errores 404




users_list = []



# El get es para leer datos
@router.get("/", response_model=list[User]) 
async def users():
    return users_schema(db_client.local.users.find())

#LLamar por path
@router.get("/{id}")
async def user(id: str):
    return search_user("_id", ObjectId(id))
    

#Query  /userquery/
@router.get("/")           #?id=1&name=Mauricio etc..
async def user(id: str):   #Tambien podriamos pedir un string para buscar por nombre etc..
    return search_user("_id", ObjectId(id))
    
#POST: Crear un usuario
@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED ) #response_model indica que el tipo de respuesta sera un User
async def user(user: User):
    if type(search_user("email", user.email)) == User:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User already exists")

    user_dict = dict(user)
    del user_dict["id"]
    id = db_client.local.users.insert_one(user_dict).inserted_id

    new_user = user_schema(db_client.local.users.find_one({ "_id": id})) #Clave unica que genera mongo _id 
    return new_user #User(**new_user)


#PUT: Actualizar un usuario
@router.put("/", response_model=User)
async def user(user: User):
    user_dict = dict(user)
    del user_dict["id"]
    try:
        db_client.local.users.find_one_and_replace({"_id": ObjectId(user.id)}, user_dict)
       
    except:
        return {"error": "No se ah actualizado el usuario.."}
    
    return search_user("_id", ObjectId(user.id))

@router.delete("/{id}")
async def user(id: str):
    
    found = db_client.local.users.find_one_and_delete({"_id": ObjectId(id)})
    if found:
        return HTTPException(status.HTTP_200_OK, detail="Eliminado correctamente...") 
    if not found:
       return {'error': 'No se ha eliminado el usuario'}
        
        
    

def search_user(field: str, key):
    try:
        
        user = user_schema(db_client.local.users.find_one({field: key}))
        return User(**user)
    except:
        return {"error": "User not found"}
    


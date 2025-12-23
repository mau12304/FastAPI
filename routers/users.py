from fastapi import APIRouter
from pydantic import BaseModel
from fastapi import HTTPException

#GET: leer datos 
#POST: Crear datos 
#PUT: Actualizar datos
#DELETE: Eliminar datos
# FastAPI es un framework para crear APIs RESTful de manera rapida y sencilla
# pip install fastapi   
# pip install uvicorn
# uvicorn es un servidor ASGI para ejecutar aplicaciones FastAPI
# Para levantar el servidor local se usa el comando: uvicorn main:app --reload

router = APIRouter(prefix="/users", # prefijo para todas las rutas de este router
                   tags=["users"],                             # tags es para agrupar las rutas en la documentacion
                   responses={404: {"message": "Not found"}})  # Respuesta por defecto para errores 404

# Levantar servidor local
# uvicorn users:app --reload

class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int


users_list = [User(id=1,name = "Mauricio", surname = "Lara", url = "htttp://mau.com", age = 21),
              User(id=2,name = "Mourdev", surname = "Brais", url = "htttp4://Brais.com", age = 21),
              User(id=3,name = "Juan", surname = "Jose", url = "htttp://Jose.com", age = 21)]

@router.get("/usersjson")
async def usersjson(): #async es para indicar que la funcion es asincrona #asincrona significa que puede ejecutarse en paralelo con otras tareas sin bloquear el flujo principal del programa
    return [
        {"name": "Mauricio", "surname": "Lara", "url": "htttp://mau.com", "age": 21},
        {"name": "Mourdev", "surname": "Brais", "url": "htttp://Brais.com", "age": 21},
        {"name": "Juan", "surname": "Jose", "url": "htttp://Jose.com", "age": 21}
        ]

# El get es para leer datos
@router.get("/") 
async def users():
    return users_list

#LLamar por path
@router.get("/{id}")
async def user(id: int):
    return search_user(id)
    

                           #hemos podido crear la misma operacion de dos formas diferentes, una por path y otra por query
#Query  /userquery/
@router.get("/query/")           #?id=1&name=Mauricio etc..
async def user(id: int):   #Tambien podriamos pedir un string para buscar por nombre etc..
    return search_user(id)
    
#POST: Crear un usuario
@router.post("/", response_model=User, status_code=201 ) #response_model indica que el tipo de respuesta sera un User
async def user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=404, detail="User already exists")
    
    users_list.append(user)
    return users_list


#PUT: Actualizar un usuario
@router.put("/actualizar/")
async def user(user: User):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
    if not found:
        return {"error": "User not found"}
    #else:
    #    return user

    return user #Tambien podemos devolver el usuario actualizado con else


@router.delete("/{id}")
async def user(id: int):
    found = False 
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index] 
            found = True
    
    if not found:
       return {'error': 'No se ha eliminado el usuario'}
        
        
    
       

def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]   #si se deja asi devolveria un listado tenemos que proporcionar en que posicion esta el usuario
    # se pone en 0 para devolver el primer usuario que coincida con el id
    except:
        return {"error": "User not found"}
    

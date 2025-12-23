from pydantic import BaseModel



class User(BaseModel):
    id: str | None 
    # String para poder hacer mas id mucho mas grande
    username: str
    email: str

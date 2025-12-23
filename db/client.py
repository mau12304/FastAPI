from pymongo import MongoClient 
#Mongodb en localhost por defecto
# db_client = MongoClient()

db_client = MongoClient("mongodb+srv://mauriciolara:mauriciolara0204@cluster0.wqvxmbt.mongodb.net/?appName=Cluster0").Cluster0  #Conexion a mongo en docker-compose

# from pymongo.mongo_client import MongoClient
# from pymongo.server_api import ServerApi

# uri = "mongodb+srv://mauriciolara:<db_password>@cluster0.wqvxmbt.mongodb.net/?appName=Cluster0"

# # Create a new client and connect to the server
# client = MongoClient(uri, server_api=ServerApi('1'))

# # Send a ping to confirm a successful connection
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)
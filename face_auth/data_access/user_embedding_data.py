## This code is for a python class named "UserEmbeddingData". It interacts with a MongoDB database to
#  store and retrieve user data based on user UUIDs.

from face_auth.config.database import MongodbClient
from face_auth.constant.database_constants import EMBEDDING_COLLECTION_NAME


class UserEmbeddingData:
    def __init__(self) -> None:
        self.client = MongodbClient() ## object of the "MongodbClient" class and stores it in the "client" attribute of the current object.
        self.collection_name = EMBEDDING_COLLECTION_NAME ## stores the value of the "EMBEDDING_COLLECTION_NAME" constant in the "collection_name" attribute of the current object.
        self.collection = self.client.database[self.collection_name] ##  gets the collection from the
# MongoDB database specified by the "collection_name" attribute and stores it in the "collection" attribute of the current object.

    def save_user_embedding(self, uuid_: str, embedding_list) -> None: ##  "save_user_embedding" method, which takes a UUID string and an embedding list as input parameters.
        self.collection.insert_one({"UUID": uuid_, "user_embed": embedding_list}) ## This line inserts a new document into the collection in the MongoDB database. The document consists of the UUID string and the embedding list.

    def get_user_embedding(self, uuid_: str) -> dict: ## "get_user_embedding" method, which takes a UUID string as input parameter and returns a dictionary.
        user: dict = self.collection.find_one({"UUID": uuid_}) #This line finds the document in the collection that matches the given UUID and stores it in the "user" variable.
        if user != None: ## If it is not, the "user" variable is returned
            return user
        else:
            return None ## otherwise None is returned.

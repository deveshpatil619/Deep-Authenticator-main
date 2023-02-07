import io
import sys
from ast import Bytes
from typing import List

import numpy as np
from deepface import DeepFace
from deepface.commons.functions import detect_face
from PIL import Image

from face_auth.constant.embedding_constants import (
    DETECTOR_BACKEND,
    EMBEDDING_MODEL_NAME,
    ENFORCE_DETECTION,
    SIMILARITY_THRESHOLD,
)
from face_auth.data_access.user_embedding_data import UserEmbeddingData
from face_auth.exception import AppException
from face_auth.logger import logging

## validates a user's embedding information in the database.
class UserLoginEmbeddingValidation:
    def __init__(self, uuid_: str) -> None:  
    ## the constructor method that takes a user's UUID as an argument and sets it as an instance variable 
    # self.uuid_. It also creates an instance of the UserEmbeddingData class and calls its get_user_embedding 
    # method to retrieve the user's embedding data and stores it as self.user.
        self.uuid_ = uuid_
        self.user_embedding_data = UserEmbeddingData()
        self.user = self.user_embedding_data.get_user_embedding(uuid_)

    def validate(self) -> bool: ## the method that validates the user's information and returns a boolean value
        try:
            if self.user["UUID"] == None: ## checks if the UUID of the user is None. If it is, returns False.
                return False
            if self.user["user_embed"] == None: #  checks if the user's embedding information is None. If it is, returns False.
                return False
            return True
        except Exception as e:
            raise e

    @staticmethod
    #generate_embedding that takes an input argument img_array which is of type np.ndarray (NumPy array).
    def generate_embedding(img_array: np.ndarray) -> np.ndarray:
        """
        Generate embedding from image array"""
        try:
            ##method first calls a function detect_face with the input img_array and specified detector_backend and
            # enforce_detection arguments. The purpose of this function is to detect faces in the input image.
            faces = detect_face(
                img_array,
                detector_backend=DETECTOR_BACKEND, ## we are using mtcnn algorithm for face detection
                enforce_detection=ENFORCE_DETECTION, ## ENFORCE_DETECTION is set to false
            )
            # function is used to generate an embedding from the face
            embed = DeepFace.represent(  ## calls another function DeepFace.
                img_path=faces[0], ##represent with the input faces[0] which is the first face detected
                model_name=EMBEDDING_MODEL_NAME, ## we using Facenet algorithm for generating the embeddings
                enforce_detection=False, ## 
            )
            return embed ## The generated embedding is then returned. 
        except Exception as e:
            raise AppException(e, sys) from e

    @staticmethod
    def generate_embedding_list(files: List[Bytes]) -> List[np.ndarray]: ##The method takes a list of files 
        #(binary image data) as input and returns a list of embeddings (np.ndarray).
        """
        The code defines a static method generate_embedding_list in the class UserLoginEmbeddingValidation.
        """
        embedding_list = []  ## creating empty list to store the embeddings
        for contents in files: ## It then loops over the binary data in files and for each binary data:
            img = Image.open(io.BytesIO(contents)) # Converts it to an image using the Image.open method from the PIL library. 

            img_array = np.array(img) ## Converts the image to a numpy array using the np.array method.
            
            embed = UserLoginEmbeddingValidation.generate_embedding(img_array) # the embedding of the image using the generate_embedding method from the same class.
            embedding_list.append(embed) #Adds the embedding to the embedding_list.
        return embedding_list

    @staticmethod
    def average_embedding(embedding_list: List[np.ndarray]) -> List:
        """static method named "average_embedding" that takes a list of numpy arrays and calculates the
         average of the arrays.

        Args:
            embedding_list (List[np.ndarray]): _description_

        Returns:
            List: _description_
        
        """
    #function first calculates the mean of the list of embeddings using the numpy function
    #  "np.mean" with "axis=0".
        avg_embed = np.mean(embedding_list, axis=0)
        return avg_embed.tolist() ## returns the result of the calculation as a list,
                                     # by converting the numpy array to a list using the "tolist" method.

    @staticmethod
    def cosine_simmilarity(db_embedding, current_embedding) -> bool:
        """Function to calculate cosine similarity between two embeddings

        Args:
            db_embedding (list): This embedding is extracted from the database
            current_embedding (list): This embedding is extracted from the current images

        Returns:
            int: simmilarity value
        """
#The cosine similarity is calculated by taking the dot product of the two arrays and dividing it by the
# product of their norms, which are calculated using the numpy functions "np.dot" and "np.linalg.norm".
# The result of this calculation is then returned.
        try:
            return np.dot(db_embedding, current_embedding) / (
                np.linalg.norm(db_embedding) * np.linalg.norm(current_embedding)
            )
        except Exception as e:
            raise AppException(e, sys) from e
##  implementation of a function called compare_embedding which is used to compare an image file's
#  embedding to the one stored in the database for a user
    def compare_embedding(self, files: bytes) -> bool: ## function has a single argument files which is expected to be in bytes format.
        """Function to compare the embedding of the current image with the embedding of the database

        Args:
            files (list): Bytes of images

        Returns:
            bool: Returns True if the similarity is greater than the threshold
        """
        try:

            if self.user: 
                logging.info("Validating User Embedding ......")
                # Validate user embedding
                if self.validate() == False:
                    return False

                logging.info("Embedding Validation Successfull.......")

                # Generate embedding list
                logging.info("Generating Embedding List .......")
                embedding_list = UserLoginEmbeddingValidation.generate_embedding_list(
                    files
                )
                logging.info("Embedding List generated.......")

                

                # Calculate average embedding

                logging.info("Calculating Average Embedding .......")
                avg_embedding_list = UserLoginEmbeddingValidation.average_embedding(
                    embedding_list
                )
                logging.info("Average Embedding calculated.......")

                # code then gets the embedding stored in the database for the user
                db_embedding = self.user["user_embed"]

                logging.info("Calculating Cosine Similarity .......")
                # Calculate cosine similarity  between the average embedding and the embedding stored in the database
                simmilarity = UserLoginEmbeddingValidation.cosine_simmilarity(
                    db_embedding, avg_embedding_list
                )
                logging.info("Cosine Similarity calculated.......")
## code checks if the cosine similarity is greater than or equal to a pre-defined constant SIMILARITY_THRESHOLD
                if simmilarity >= SIMILARITY_THRESHOLD:  ## SIMILARITY_THRESHOLD = 0.75
                    logging.info("User Authenticated Successfully.......")
                    return True
                else:
                    logging.info("User Authentication Failed.......")
                    return False
            logging.info("User Authentication Failed.......")

            return False
        except Exception as e:
            raise AppException(e, sys) from e

    # def get_user_embeeding_object(self, uuid_:str) -> Embedding:
    #     """_summary_

    #     Args:
    #         user_embedding (dict): _description_

    #     Returns:
    #         Embedding: _description_
    #     """
    #     try:

    #         user_embedding = self.user_embedding_data.get_user_embedding(uuid_)
    #         return user_embedding
    #     except Exception as e:
    #         raise AppException(e, sys) from e


## UserRegisterEmbeddingValidation that handles user's embedding validation while registration. 
# It has the following methods:
class UserRegisterEmbeddingValidation: 
    def __init__(self, uuid_: str) -> None:  ##the constructor method that initializes the class with uuid_ and 
        #creates an instance of the UserEmbeddingData class.
        self.uuid_ = uuid_
        self.user_embedding_data = UserEmbeddingData()

    def save_embedding(self, files: bytes):
        """This method takes files as an argument which is the byte representation of the images, 
        generates the embedding list and then calculates the average embedding of the images. 
        Args:
            files (dict): Bytes of images

        Returns:
            Embedding: saves the image to database
        """
        try:
            embedding_list = UserLoginEmbeddingValidation.generate_embedding_list(files) #It calls the generate_embedding_list 
            #method from the UserLoginEmbeddingValidation class with the files as input. The method generates the embedding from the files.
            avg_embedding_list = UserLoginEmbeddingValidation.average_embedding(embedding_list) # It calls the average_embedding 
            #method from the UserLoginEmbeddingValidation class with the embedding_list as input. This method calculates the average embedding.
            self.user_embedding_data.save_user_embedding(self.uuid_, avg_embedding_list) #code saves the average embedding in the database by 
            # calling the save_user_embedding method from the UserEmbeddingData class.
        except Exception as e:
            raise AppException(e, sys) from e







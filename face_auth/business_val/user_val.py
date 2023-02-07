import re
import sys
from typing import Optional

from passlib.context import CryptContext

from face_auth.data_access.user_data import UserData
from face_auth.entity.user import User
from face_auth.exception import AppException
from face_auth.logger import logging

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class LoginValidation:
    """_summary_
    """

    def __init__(self, email_id: str, password: str): ##constructor of the class which takes email_id and password
        # as input parameters and sets them as instance variables. 
        """_summary_

        Args:
            email_id (str): _description_
            password (str): _description_
        """
        self.email_id = email_id ## making the instance of email_id
        self.password = password ## making the instance of password
        self.regex = re.compile( ## compiles a regular expression pattern used to validate the email.
            r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
        )
##  The method validates the email_id and password by checking if they are not empty
    def validate(self) -> bool:   ## returns a boolien output
        """validate: This validates the user input

        Args:
            email_id (str): email_id of the user
            password (str): password of the user
        """
        try:## It returns an error message if any of the checks fail.
            msg = "" ## taking empty string to print the message
            if not self.email_id:
                msg += "Email Id is required"
            if not self.password:
                msg += "Password is required"
            if not self.is_email_valid(): ## to check if the email id entered is valid or not
                msg += "Invalid Email Id"
            return msg
        except Exception as e:
            raise e
## function checks if the email id provided by the user is in the correct format or not. 
    def is_email_valid(self) -> bool:   ## returns a boolien output
# The function uses the re.fullmatch method from the re module to match the email id with a regular expression self.regex
        if re.fullmatch(self.regex, self.email_id):
            return True ## If the match is found, it returns True, indicating that the email id is in a valid format.
        else:
            return False ## If the match is not found, it returns False, indicating that the email id is not in a valid format

##purpose of the function is to ensure that the entered password matches the hashed password stored in the database.
    def verify_password(self, plain_password: str, hashed_password: str) -> bool: ##takes in two arguments: plain_password and hashed_password of type string and returns a boolean value
        """Verify hashed password and plain password.

        Args:
            plain_password (str): _description_
            hashed_password (str): _description_

        Returns:
            bool: _description_
        """
        return bcrypt_context.verify(plain_password, hashed_password) ##  bcrypt_context.verify method to verify if the plain_password is equal to the hashed_password.

    def validate_login(self) -> dict: ## returns a dictionary with two keys status and msg

        """This checks all the validation conditions for the user registration
        """
        if len(self.validate()) != 0: ##  method checks the length of the result from the validate method
            return {"status": False, "msg": self.validate()} ## If it is not 0, it returns a dictionary with status set to False and msg set to the result of the validate method.
        return {"status": True} #If the length of the result is 0, it returns a dictionary with status set to True.

    def authenticate_user_login(self) -> Optional[str]:  ## can either return a string value, which is the user data, or None if the authentication fails.
        """_summary_: This authenticates the user and returns the token
        if the user is authenticated

        Args:
            email_id (str): _description_
            password (str): _description_
        """
        try:

            logging.info("Authenticating the user details.....")
            if self.validate_login()["status"]: ##  checks if the result of calling validate_login method on 
# the current object is {"status": True}. If it is, the function continues to execute, otherwise it returns False.
                userdata = UserData() ## function creates an object of the UserData class This class will have all the mongo db operations for user data .
                logging.info("Fetching the user details from the database.....")
                user_login_val = userdata.get_user({"email_id": self.email_id}) ## retrieves the user data using get_user method of userdata object.
# It retrieves the data of the user whose email id is the same as the email_id attribute of the current object.
                if not user_login_val: ## The function checks if the user data exists by checking the truthiness of the user_login_val
                    logging.info("User not found while Login") 
                    return False
                if not self.verify_password(self.password, user_login_val["password"]): ## verifies the password
# using verify_password method by passing self.password and user_login_val["password"] as arguments
                    logging.info("Password is incorrect")
                    return False
                logging.info("User authenticated successfully....")
                return user_login_val  ## returns the user data.
            return False
        except Exception as e:
            raise AppException(e, sys) from e

##  RegisterValidation which has a set of methods to validate the registration of a user.
class RegisterValidation:

    """_summary_: This authenticates the user and returns the status
    """
    
    
    def __init__(self, user: User) -> None:  ## method and accepts one argument, "user", of type "User". The return type is specified as "None"
        try:
# # It initializes the user, regular expression to validate email, UUID, UserData object and bcrypt context.
            self.user = user  ## assigns the argument passed to the constructor, "user", to an instance variable named "user".
            self.regex = re.compile(
                r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
            ) # The pattern is used to match strings that match a specific format for an email address.
            self.uuid = self.user.uuid_ ##"uuid_" attribute of the "user" object to an instance variable named "uuid".
            self.userdata = UserData()  ## instance of the "UserData" class and assigns it to an instance variable named "userdata".
            self.bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto") ## creates a "CryptContext" object, 
            #which is used for handling password hashing, using the "bcrypt" scheme. The "deprecated" argument is
            #set to "auto", which means that deprecated schemes will be automatically replaced with the most secure available scheme.
        except Exception as e:
            raise e

    def validate(self) -> bool:

        """The method that checks all validation conditions for user registration such as if all required fields are
         filled, email is valid, password length is between 8 and 16, password match, and details already exists or 
         not. It returns a message.

        Returns:
            _type_: string
        """
        try:
            msg = ""  ## empty string
            if self.user.Name == None:
                msg += "Name is required"  ## Name attribute of the user object is None, msg is updated with the string "Name is required".

            if self.user.username == None:
                msg += "Username is required" ##username attribute of the user object is None, msg is updated with the string "Username is required".

            if self.user.email_id == None:
                msg += "Email is required" ## email_id attribute of the user object is None, msg is updated with the string "Email is required".


            if self.user.ph_no == None:
                msg += "Phone Number is required" ## ph_no attribute of the user object is None, msg is updated with the string "Phone Number is required"

            if self.user.password1 == None:
                msg += "Password is required" ## password1 attribute of the user object is None, msg is updated with the string "Password is required".

            if self.user.password2 == None:
                msg += "Confirm Password is required" ## password2 attribute of the user object is None, msg is updated with the string "Confirm Password is required".

            if not self.is_email_valid():
                msg += "Email is not valid" ## if Email is not valid msg is updated with the string "Email is not valid". This is determined by calling the method is_email_valid.

            if not self.is_password_valid():
                msg += "Length of the pass`word should be between 8 and 16" ##If the password is not valid, msg is updated with the string "Length of the password should be between 8 and 16". This is determined by calling the method is_password_valid.

            if not self.is_password_match():
                msg += "Password does not match" ## If the password does not match, msg is updated with the string "Password does not match". This is determined by calling the method is_password_match.

            if not self.is_details_exists():
                msg += "User already exists"  ## If the user details already exist, msg is updated with the string "User already exists". This is determined by calling the method is_details_exists.

            return msg
        except Exception as e:
            raise e

    def is_email_valid(self) -> bool:
        """_summary_: This validates the email id

        Returns:
            bool: True if the email id is valid else False
        """
        #The re.fullmatch method returns a Match object if there is a match, and None if no match was found. 
        if re.fullmatch(self.regex, self.user.email_id): ## Try to apply the pattern to all of the string, returning a Match object, or None if no match was found.
            return True
        else:
            return False

    def is_password_valid(self) -> bool:
        """This function checks if the length of the password1 and password2 fields in the user object are between 8 and 16 characters long. 
        If the length is within this range, it returns True, otherwise it returns False."""
        if len(self.user.password1) >= 8 and len(self.user.password2) <= 16:
            return True
        else:
            return False

    def is_password_match(self) -> bool:
        """ This function returns True if the password1 and password2 are matched"""
        if self.user.password1 == self.user.password2:
            return True
        else:
            return False

    def is_details_exists(self) -> bool:
        """The function is_details_exists checks if the user already exists in the database or not."""
        username_val = self.userdata.get_user({"username": self.user.username}) ## uses the get_user method of UserData to search the database with the given username.
        emailid_val = self.userdata.get_user({"email_id": self.user.email_id}) ## uses the get_user method of UserData to search the database with the given email id.
        uuid_val = self.userdata.get_user({"UUID": self.uuid}) ## uses the get_user method of UserData to search the database with the given UUID.
        if username_val == None and emailid_val == None and uuid_val == None: # The final if statement checks if all of the username_val, emailid_val and uuid_val are None, meaning that no user was found in the database with these details.
            return True # If the details do not exist in the database, the function returns True.
            # Otherwise, it returns False.

        return False

    @staticmethod
    def get_password_hash(password: str) -> str:
        """This method get_password_hash is a static method. It takes a string parameter password and returns
         the hash of the given password as a string. """
        return bcrypt_context.hash(password) # The hash is calculated using the bcrypt_context object that
        # was created in the __init__ method of the class. This method is used to store the password securely
        #  in the database by storing its hash instead of the actual password.

    def validate_registration(self) -> bool:

        """This checks all the validation conditions for the user registration
        """
        if len(self.validate()) != 0:  ## if the validate method returns some of the error messages
            return {"status": False, "msg": self.validate()} ## set the status to false and return the error message of the validate
        return {"status": True} ## if the validate method is error free then return the status as true

    def authenticate_user_registration(self) -> bool:
        """_summary_: This saves the user details in the database
        only after validating the user details

        Returns:
            bool: _description_
        """
        try:
            logging.info("Validating the user details while Registration.....")
            if self.validate_registration()["status"]: ## checks if the validation is successful
                logging.info("Generating the password hash.....")
                hashed_password: str = self.get_password_hash(self.user.password1) ## generates the password hash using the get_password_hash function and saves it to the hashed_password variable.
                user_data_dict: dict = { # creates a dictionary of user data to be saved in the database
                    "Name": self.user.Name, 
                    "username": self.user.username,
                    "password": hashed_password,
                    "email_id": self.user.email_id,
                    "ph_no": self.user.ph_no,
                    "UUID": self.uuid,
                }
                logging.info("Saving the user details in the database.....")
                self.userdata.save_user(user_data_dict)  ## saves the user data to the database
                logging.info("Saving the user details in the database completed.....")
                return {"status": True, "msg": "User registered successfully"} ## returns the status of the registration process and a message indicating successful registration
            logging.info("Validation failed while Registration.....")
            return {"status": False, "msg": self.validate()} ## returns the status of the registration process and a message indicating the failure of the validation process
        except Exception as e:
            raise e




## This is a FastAPI code for authentication with features of user registration and login.
#  The API has two models, Login and Register, for user login and registration data.

from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, HTTPException, Request, Response, status
from jose import JWTError, jwt
from pydantic import BaseModel
from starlette.responses import JSONResponse, RedirectResponse

from face_auth.business_val.user_val import LoginValidation, RegisterValidation
from face_auth.constant.auth_constant import ALGORITHM, SECRET_KEY
from face_auth.entity.user import User


class Login(BaseModel):
    """Base model for login
    """

    email_id: str
    password: str


class Register(BaseModel):
    """
    Base model for register
    """

    Name: str
    username: str
    email_id: str
    ph_no: int
    password1: str
    password2: str


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={"401": {"description": "Not Authorized!!!"}},
)


# Calloging the logger for Database read and insert operations


async def get_current_user(request: Request):
    """This function is used to get the current user

    Args:
        request (Request): Request from the route

    Returns:
        dict: Returns the username and uuid of the user
    """
    try:
        secret_key = SECRET_KEY
        algorithm = ALGORITHM

        token = request.cookies.get("access_token")
        if token is None:
            return None

        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        uuid: str = payload.get("sub")
        username: str = payload.get("username")

        if uuid is None or username is None:
            return logout(request)
        return {"uuid": uuid, "username": username}
    except JWTError:
        raise HTTPException(status_code=404, detail="Detail Not Found")
    except Exception as e:
        msg = "Error while getting current user"
        response = JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"message": msg}
        )
        return response


## The function create_access_token generates a JSON Web Token (JWT) given the uuid and username of a user.
## The input parameters of the function are:
#uuid (str): the unique identifier of the user
#username (str): the username of the user
#expires_delta (timedelta, optional): the token expiration time, which is optional and by default is set to 15 minutes after the current time

def create_access_token(
    uuid: str, username: str, expires_delta: Optional[timedelta] = None
) -> str:
    """This function is used to create the access token

    Args:
        uuid (str): uuid of the user
        username (str): username of the user

    Raises:
        e: _description_

    Returns:
        _type_: _description_
    """

    try:
        ## secret_key and algorithm are used as the secret key and algorithm for the encoding.
        secret_key = SECRET_KEY
        algorithm = ALGORITHM
        ## The encode dictionary contains the information to be included in the JWT, and has two keys: sub and username.
        ## which has information of uuid and username
        encode = {"sub": uuid, "username": username}
        if expires_delta:  ## The token expiration is set to the current time plus the expires_delta (or 15 minutes if it's not provided).
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        encode.update({"exp": expire}) ##The encode dictionary is updated with the exp key and its value set to the token expiration.
        # Finally, the jwt.encode function is used to encode the encode dictionary into a JWT, using the secret_key and algorithm.
        return jwt.encode(encode, secret_key, algorithm=algorithm) 
    except Exception as e:
        raise e


@router.post("/token")
async def login_for_access_token(response: Response, login) -> dict:
    """Set the access token

    Returns:
        dict: response
    """

    try:
        user_validation = LoginValidation(login.email_id, login.password)
        user: Optional[str] = user_validation.authenticate_user_login()
        if not user:
            return {"status": False, "uuid": None, "response": response}
        token_expires = timedelta(minutes=15)
        token = create_access_token(
            user["UUID"], user["username"], expires_delta=token_expires
        )
        response.set_cookie(key="access_token", value=token, httponly=True)
        return {"status": True, "uuid": user["UUID"], "response": response}
    except Exception as e:
        msg = "Failed to set access token"
        response = JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"message": msg}
        )
        return {"status": False, "uuid": None, "response": response}


@router.get("/", response_class=JSONResponse)
async def authentication_page(request: Request):
    """Login GET route

    Returns:
        _type_: JSONResponse
    """
    try:
        return JSONResponse(
            status_code=status.HTTP_200_OK, content={"message": "Authentication Page"}
        )
    except Exception as e:
        raise e


@router.post("/", response_class=JSONResponse)
async def login(request: Request, login: Login):
    """Route for User Login

    Returns:
        _type_: Login Response
    """
    try:
        # response = RedirectResponse(url="/application/", status_code=status.HTTP_302_FOUND)
        msg = "Login Successful"
        response = JSONResponse(
            status_code=status.HTTP_200_OK, content={"message": msg}
        )
        token_response = await login_for_access_token(response=response, login=login)
        if not token_response["status"]:
            msg = "Incorrect Username and password"
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"status": False, "message": msg},
            )
            # return RedirectResponse(url="/", status_code=status.HTTP_401_UNAUTHORIZED, headers={"msg": msg})
        # msg = "Login Successfull"
        # response = JSONResponse(status_code=status.HTTP_200_OK, content={"message": msg}, headers={"uuid": "abda"})
        response.headers["uuid"] = token_response["uuid"]

        return response

    except HTTPException:
        msg = "UnKnown Error"
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"status": False, "message": msg},
        )
        # return RedirectResponse(url="/", status_code=status.HTTP_401_UNAUTHORIZED, headers={"msg": msg})
    except Exception as e:
        msg = "User NOT Found"
        response = JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"status": False, "message": msg},
        )
        return response

## The code defines an API endpoint "/register" using FastAPI's @router.get decorator.
@router.get("/register", response_class=JSONResponse) ## When a GET request is sent to this endpoint, the authentication_page function will be executed.
async def authentication_page(request: Request):  ## The function takes in a single argument request which is an instance of the FastAPI Request class.
    """Route for User Registration

    Returns:
        _type_: Register Response
    """
    try:
        return JSONResponse(
            status_code=status.HTTP_200_OK, content={"message": "Registration Page"}  ##The function returns a JSONResponse with a status code of 200 (OK) and a content of {"message": "Registration Page"}.
        )
    except Exception as e:
        raise e

## The above code defines a function register_user with route /register that handles a POST request and takes
# in two parameters request and register.
@router.post("/register", response_class=JSONResponse)
async def register_user(request: Request, register: Register):

    """Post request to register a user

    Args:
        request (Request): Request Object
        register (Register):    Name: str
                                username: str
                                email_id: str
                                ph_no: int
                                password1: str
                                password2: str

    Raises:
        e: If the user registration fails

    Returns:
        _type_: Will redirect to the embedding generation route and return the UUID of user
    """
    try:
        ## Extract the details from the register object, which contains information about the user to be registered.
        name = register.Name
        username = register.username
        password1 = register.password1
        password2 = register.password2
        email_id = register.email_id
        ph_no = register.ph_no

        # Adds the user's unique identifier (UUID) to the session.
        user = User(name, username, email_id, ph_no, password1, password2)
        request.session["uuid"] = user.uuid_

        # Validate the user data using the RegisterValidation class.
        user_registration = RegisterValidation(user)

        # If the validation is not successful, it returns a JSONResponse with a status code of 
#          401 (Unauthorized) and a message indicating why the validation failed.
        validate_regitration = user_registration.validate_registration()
        if not validate_regitration["status"]:
            msg = validate_regitration["msg"]
            response = JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"status": False, "message": msg},
            )
            return response

        validation_status = user_registration.authenticate_user_registration()
        ## If the validation is successful, the user data is saved, and a JSONResponse is returned with a status
        # code of 200 (OK) and a message indicating that the registration was successful. The response also includes a header with the user's UUID.
        msg = "Registration Successful...Please Login to continue"
        response = JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"status": True, "message": validation_status["msg"]},
            headers={"uuid": user.uuid_},
        )
        return response
    except Exception as e:  # If an exception occurs, it will be raised.
        raise e


@router.get("/logout")
async def logout(request: Request):
    """Route for User Logout

    Returns:
        _type_: Logout Response
    """
    try:
        msg = "You have been logged out"
        response =  RedirectResponse(url="/auth/", status_code=status.HTTP_302_FOUND, headers={"msg": msg})
        response.delete_cookie(key="access_token")
        response = JSONResponse(
            status_code=status.HTTP_200_OK, content={"status": True, "message": msg}
        )
        return response
    except Exception as e:
        raise e


from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, HTTPException, Request, Response, status
from jose import JWTError, jwt
from pydantic import BaseModel
from starlette.responses import JSONResponse, RedirectResponse

from face_auth.business_val.user_val import LoginValidation, RegisterValidation
from face_auth.constant.auth_constant import ALGORITHM, SECRET_KEY
from face_auth.entity.user import User

## Defines the Login and Register data models. These classes define the expected inputs for the authentication APIs.

class Login(BaseModel):
    """Base model for login
    """

    email_id: str
    password: str


class Register(BaseModel):
    """
    Base model for register
    """

    Name: str
    username: str
    email_id: str
    ph_no: int
    password1: str
    password2: str

## Creates an APIRouter instance to handle the authentication APIs. The router is set up with a prefix of "/auth",
#  a tag of "auth", and a response with a 401 status code.
router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={"401": {"description": "Not Authorized!!!"}},
)


# Calloging the logger for Database read and insert operations


async def get_current_user(request: Request):
    """This function is used to get the current user

    Args:
        request (Request): Request from the route

    Returns:
        dict: Returns the username and uuid of the user
    """
    try:
        ## try block is used to handle exceptions that might occur while getting the current user.
        ## secret_key and algorithm are assigned values from SECRET_KEY and ALGORITHM respectively.
        secret_key = SECRET_KEY
        algorithm = ALGORITHM
        ## access_token is retrieved from the cookies in the request using request.cookies.get("access_token")
        token = request.cookies.get("access_token")
        if token is None:
            return None ## If the token is None, the function returns None

        ## The payload of the token is decoded using jwt.decode(token, secret_key, algorithms=[algorithm]).
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        ## uuid and username are extracted from the payload using payload.get("sub") and payload.get("username") respectively.
        uuid: str = payload.get("sub")
        username: str = payload.get("username")
        ## uuid or username is None, the function calls logout(request) and returns its result.
        if uuid is None or username is None:
            return logout(request)
        return {"uuid": uuid, "username": username} ## uuid and username are not None, a dictionary with uuid and username as keys is returned.
    except JWTError:
        raise HTTPException(status_code=404, detail="Detail Not Found") #JWTError is caught, an HTTPException with a status code of 404 and detail "Detail Not Found" is raised.
    except Exception as e: ## If any other exception occurs, an error message is created and a JSONResponse object with the error message and a status code of 404 is returned.
        msg = "Error while getting current user"
        response = JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"message": msg}
        )
        return response

## The function create_access_token generates a JSON Web Token (JWT) given the uuid and username of a user.
def create_access_token(
    uuid: str, username: str, expires_delta: Optional[timedelta] = None 
) -> str:  ## The input parameters of the function are:
#uuid (str): the unique identifier of the user
#username (str): the username of the user
#expires_delta (timedelta, optional): the token expiration time, which is optional and by default is set to 15 minutes after the current time 
    """This function is used to create the access token

    Args:
        uuid (str): uuid of the user
        username (str): username of the user

    Raises:
        e: _description_

    Returns:
        _type_: _description_
    """

    try: ## secret_key and algorithm are used as the secret key and algorithm for the encoding.
        secret_key = SECRET_KEY
        algorithm = ALGORITHM

        encode = {"sub": uuid, "username": username} #The encode dictionary contains the information to be included in the JWT, and has two keys: sub and username.
                                                     # sub had uuid in it 
        if expires_delta:
            expire = datetime.utcnow() + expires_delta 
        else: ##The token expiration is set to the current time plus the expires_delta (or 15 minutes if it's not provided).
            expire = datetime.utcnow() + timedelta(minutes=15)
        encode.update({"exp": expire})
        # return jwt.encode(encode, Configuration().SECRET_KEY, algorithm=Configuration().ALGORITHM)
        return jwt.encode(encode, secret_key, algorithm=algorithm) ## The encode dictionary is updated with the exp key and its value set to the token expiration.
    except Exception as e:
        raise e


@router.post("/token")
async def login_for_access_token(response: Response, login) -> dict:
    """Set the access token

    Returns:
        dict: response
    """

    try:
        user_validation = LoginValidation(login.email_id, login.password)
        user: Optional[str] = user_validation.authenticate_user_login()
        if not user:
            return {"status": False, "uuid": None, "response": response}
        token_expires = timedelta(minutes=15)
        token = create_access_token(
            user["UUID"], user["username"], expires_delta=token_expires
        )
        response.set_cookie(key="access_token", value=token, httponly=True)
        return {"status": True, "uuid": user["UUID"], "response": response}
    except Exception as e:
        msg = "Failed to set access token"
        response = JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"message": msg}
        )
        return {"status": False, "uuid": None, "response": response}

# This code is a FastAPI endpoint function that maps to the "/register" route.
@router.get("/", response_class=JSONResponse) ## When a GET request is made to the "/register" endpoint, the function authentication_page will be executed.
async def authentication_page(request: Request): ##The function takes a single argument request of type Request from the FastAPI library.
    """Login GET route

    Returns:
        _type_: JSONResponse
    """
    try: ## Inside the function, the function returns a JSONResponse with a status code of 200 (OK) and 
        # a content of {"message": "Authentication Page"}.
        return JSONResponse(
            status_code=status.HTTP_200_OK, content={"message": "Authentication Page"}
        )
    except Exception as e:
        raise e


@router.post("/", response_class=JSONResponse)
async def login(request: Request, login: Login):
    """Route for User Login

    Returns:
        _type_: Login Response
    """
    try:
        # response = RedirectResponse(url="/application/", status_code=status.HTTP_302_FOUND)
        msg = "Login Successful"
        response = JSONResponse(
            status_code=status.HTTP_200_OK, content={"message": msg}
        )
        token_response = await login_for_access_token(response=response, login=login)
        if not token_response["status"]:
            msg = "Incorrect Username and password"
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"status": False, "message": msg},
            )
            # return RedirectResponse(url="/", status_code=status.HTTP_401_UNAUTHORIZED, headers={"msg": msg})
        # msg = "Login Successfull"
        # response = JSONResponse(status_code=status.HTTP_200_OK, content={"message": msg}, headers={"uuid": "abda"})
        response.headers["uuid"] = token_response["uuid"]

        return response

    except HTTPException:
        msg = "UnKnown Error"
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"status": False, "message": msg},
        )
        # return RedirectResponse(url="/", status_code=status.HTTP_401_UNAUTHORIZED, headers={"msg": msg})
    except Exception as e:
        msg = "User NOT Found"
        response = JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"status": False, "message": msg},
        )
        return response


##This code is a FastAPI endpoint function that maps to the "/register" route.
@router.get("/register", response_class=JSONResponse) #When a GET request is made to the "/register" endpoint, the function authentication_page will be executed.
async def authentication_page(request: Request): ## function takes a single argument request of type Request from the FastAPI library.


    """Route for User Registration

    Returns:
        _type_: Register Response
    """
    try:
        return JSONResponse( ##the function returns a JSONResponse with a status code of 200 (OK) and a content of {"message": "Registration Page"}.
            status_code=status.HTTP_200_OK, content={"message": "Registration Page"}
        )
    except Exception as e:
        raise e

## code block defines a FastAPI endpoint for registering a new user.
@router.post("/register", response_class=JSONResponse) ##It starts with the "@router.post" decorator which maps this function to the /register endpoint for HTTP POST requests.
async def register_user(request: Request, register: Register): ## It takes two arguments: "request" and
    # "register". "request" is a standard FastAPI request object, while "register" is a Pydantic model 
    # representing the information that the user provides during registration.

    """Post request to register a user

    Args:
        request (Request): Request Object
        register (Register):    Name: str
                                username: str
                                email_id: str
                                ph_no: int
                                password1: str
                                password2: str

    Raises:
        e: If the user registration fails

    Returns:
        _type_: Will redirect to the embedding generation route and return the UUID of user
    """
    try: ## Within the function, the user information is extracted from the "register" object and assigned to 
        #separate variables: name, username, password1, password2, email_id, and ph_no.
        name = register.Name
        username = register.username
        password1 = register.password1
        password2 = register.password2
        email_id = register.email_id
        ph_no = register.ph_no

        # The user's UUID is then added to the session using the user object's uuid_ attribute.
        user = User(name, username, email_id, ph_no, password1, password2)
        request.session["uuid"] = user.uuid_

        #user information is then passed to a RegisterValidation object for validation by calling the validate_registration method.
        user_registration = RegisterValidation(user)
        #If the validation fails, a JSONResponse object with status code 401 (Unauthorized) is returned, along
        #  with an error message indicating why the validation failed.
        validate_regitration = user_registration.validate_registration()
        if not validate_regitration["status"]:
            msg = validate_regitration["msg"]
            response = JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"status": False, "message": msg},
            )
            return response

        # Save user if the validation is successful
        validation_status = user_registration.authenticate_user_registration()
        ## If the validation is successful, the authenticate_user_registration method is called to save the user
        # information to the database.
        msg = "Registration Successful...Please Login to continue"
        ##the user is successfully registered, a JSONResponse object with status code 200 (OK) is returned,
        # along with a message indicating that the registration was successful. The UUID of the user is also returned in the headers.
        response = JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"status": True, "message": validation_status["msg"]},
            headers={"uuid": user.uuid_},
        )
        return response
    except Exception as e:
        raise e


@router.get("/logout")
async def logout(request: Request):
    """Route for User Logout

    Returns:
        _type_: Logout Response
    """
    try:
        msg = "You have been logged out"
        response =  RedirectResponse(url="/auth/", status_code=status.HTTP_302_FOUND, headers={"msg": msg})
        response.delete_cookie(key="access_token")
        response = JSONResponse(
            status_code=status.HTTP_200_OK, content={"status": True, "message": msg}
        )
        return response
    except Exception as e:
        raise e

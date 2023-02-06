import os
from typing import List

from fastapi import APIRouter, File, Request
from starlette import status
from starlette.responses import JSONResponse, RedirectResponse

from controller.auth_controller.authentication import get_current_user
from face_auth.business_val.user_embedding_val import (
    UserLoginEmbeddingValidation,
    UserRegisterEmbeddingValidation,
)

router = APIRouter(
    prefix="/application",
    tags=["application"],
    responses={"401": {"description": "Not Authorized!!!"}},
)

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"


@router.post("/")
async def login_embedding(
    request: Request,
    files: List[bytes] = File(description="Multiple files as UploadFile"),
):
    """This function is used to get the embedding of the user while login

    Args:
        request (Request): _description_
        files (List[UploadFile], optional): _description_. Defaults to \File(description="Multiple files as UploadFile").

    Returns:
        response: If user is authenticated then it returns the response
    """

    try:
        user = await get_current_user(request)
        if user is None:
            return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

        user_embedding_validation = UserLoginEmbeddingValidation(user["uuid"])

        # Compare embedding
        user_simmilariy_status = user_embedding_validation.compare_embedding(files)

        if user_simmilariy_status:
            msg = "User is authenticated"
            response = JSONResponse(
                status_code=status.HTTP_200_OK, content={"status": True, "message": msg}
            )
            return response
        else:
            msg = "User is NOT authenticated"
            response = JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"status": False, "message": msg},
            )
            return response
    except Exception as e:
        msg = "Error in Login Embedding in Database"
        response = JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"status": False, "message": msg},
        )
        return response

""" After the register(authentication_user_registration) in authentication we will do the register embedding part"""
@router.post("/register_embedding")
async def register_embedding(  ##  function register_embedding takes two arguments, request and files. 
    request: Request,   ## request is a Request object, and files is a list of binary files that are uploaded by the user.
    files: List[bytes] = File(description="Multiple files as UploadFile"),
):
    """This function is used to get the embedding of the user while register

    Args:
        request (Request): _description_
        files (List[UploadFile], optional): _description_. Defaults to \File(description="Multiple files as UploadFile").

    Returns:
        Response: If user is registered then it returns the response
    """

    try:
        
        uuid = request.session.get("uuid") # retrieves the UUID from the session.
        if uuid is None:
            return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND) ##checks if the UUID is present
            # in the session. If it's not present, the function returns a redirect to the "/auth" endpoint with a 302 Found HTTP status code.
        user_embedding_validation = UserRegisterEmbeddingValidation(uuid) ##creates an instance of the UserRegisterEmbeddingValidation class and passes the UUID as an argument.

        # saves the user's embeddings to the database.
        user_embedding_validation.save_embedding(files)
#If the embeddings are saved successfully, the function returns a JSONResponse object with a 200 OK HTTP status code
#  and a message that says "Embedding Stored Successfully in Database". The UUID is also included in the headers
        msg = "Embedding Stored Successfully in Database"
        response = JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"status": True, "message": msg},
            headers={"uuid": uuid},
        )
        return response
    except Exception as e:
## If there is an error in storing the embeddings, the function returns a JSONResponse object with a 404 Not Found
#  HTTP status code and a message that says "Error in Storing Embedding in Database"
        msg = "Error in Storing Embedding in Database"
        response = JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"status": True, "message": msg},
        )
        return response

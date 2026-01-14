from app.services.user_service import UserService
from fastapi import APIRouter
from app.models.user_model import (UserModel,
                                   UserItem, UserRequest, UserResponse, UserResponses)
from app.services.user_service import UserService
user_router = APIRouter()

@user_router.get("")
async def default_user():
    return {"response"," api "}


@user_router.post("get/user")
async def get_user(request:UserRequest)->UserResponse:
    response = UserResponses()
    try:
        return response
    except Exception as ex:
        response.IsInvalid = True
        response.Message = {"error": str(ex)}
        return response


@user_router.post("get/users")
async def get_user(request:UserRequest)->UserResponse:
    response = UserResponses()
    try:
        return response
    except Exception as ex:
        response.IsInvalid = True
        response.Message = {"error": str(ex)}
        return response

@user_router.post("update/user")
async def update_user(request:UserRequest)->UserResponse:
    response = UserResponse()
    try:
        return response
    except Exception as ex:
        response.IsInvalid = True
        response.Message = {"error": str(ex)}
        return response


@user_router.post("create/user")
async def create_user(request:UserRequest)->UserResponse:
    response = UserResponse()
    try:
        model = UserModel()
        service = UserService()
        service.create_user()
        return response
    except Exception as ex:
        response.IsInvalid = True
        response.Message = {"error": str(ex)}
        return response



@user_router.post("delete/user")
async def delete_user(request:UserRequest)->UserResponse:
    response = UserResponse()
    try:
        return response
    except Exception as ex:
        response.IsInvalid = True
        response.Message = {"error": str(ex)}
        return response


@user_router.post("upsert/user")
async def upsert_user(request:UserRequest)->UserResponse:
    response = UserResponse()
    try:
        return response
    except Exception as ex:
        response.IsInvalid = True
        response.Message = {"error": str(ex)}
        return response



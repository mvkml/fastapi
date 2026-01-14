from app.models.user_model import (
    UserModel,
    UserItem
    )
from fastapi import Depends
from app.dal.repositories.user_repository import UserRepository


class UserService():
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create_user(self, model: UserModel) -> UserModel:
        return self.user_repository.create_user(model)


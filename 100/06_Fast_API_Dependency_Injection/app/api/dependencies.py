from   fastapi import Depends
from app.services.user_service import UserService
from app.dal.repositories.user_repository import UserRepository
from app.dal.connections.sql_connection import get_db


def get_user_repository(db = Depends(get_db)):
    return UserRepository(db)


def get_user_service(user_repository = Depends(get_user_repository)):
    return UserService(user_repository)

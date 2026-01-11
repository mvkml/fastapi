import json
# This module defines the FastAPI router for the `api_pt` endpoints, which provide
# APIs for interacting with OpenAI's language models and retrieving application configuration.
# Endpoints included:
# - `/` : Returns a default response to verify the API is running.
# - `/config` : Returns current application and database configuration settings.
# - `/mock_prompt` : Returns a mock prompt for testing purposes.
# - `/prompt` : Invokes the OpenAI API with a user prompt and context, returning the model's response.
# Helper functions are provided for:
# - Constructing OpenAI client instances.
# - Formatting prompts and messages for the OpenAI API.
# - Retrieving configuration and model details from application settings.
# This router is intended for use in applications that require AI-powered responses,
# such as a medical insurance assistant, and demonstrates best practices for
# asynchronous API design and integration with external AI services.
from fastapi import APIRouter
from openai import OpenAI
# from core.config import  settings 

''' wirte a comment'''
api_pt_router = APIRouter()

'''
/api_pt
'''
@api_pt_router.get("/")
async def get_default_async():
    """
    Asynchronously returns a default response message for the api_pt endpoint.

    Returns:
        dict: A dictionary containing a default message.
    """
    return {"message": "Default response from api_pt harsha"}

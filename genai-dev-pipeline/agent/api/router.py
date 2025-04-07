# agent/api/router.py

from fastapi import APIRouter
from agent.api.v1 import scene01_endpoints# , scene02_endpoints

api_router = APIRouter(prefix="/v1")

api_router.include_router(scene01_endpoints.router)
# api_router.include_router(scene02_endpoints.router)
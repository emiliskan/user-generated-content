import logging

from fastapi import APIRouter
from pymongo import MongoClient

from models.review import Review

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/reviews")
async def create_review():
    pass


@router.get("/reviews/{review_id}")
async def get_review():
    pass


@router.delete("/reviews/{review_id}")
async def delete_review():
    pass


@router.patch("/reviews/{review_id}")
async def update_review():
    pass

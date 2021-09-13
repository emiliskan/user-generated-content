import logging
from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Query, Depends, HTTPException
from fastapi.security import HTTPBearer

from models.base import PydanticObjectId
from models import Review, ReviewQuery
from services.exceptions import DocumentNotFound, NotAllowed
from services.reviews import UserReviewsService, get_user_reviews_service
from core.auth import auth

router = APIRouter()
logger = logging.getLogger(__name__)

auth_scheme = HTTPBearer()


@router.get(
    "/reviews",
    description="Reviews list.",
    response_model=List[Review]
)
async def get_reviews(
        query: ReviewQuery,
        service: UserReviewsService = Depends(get_user_reviews_service),
):
    return await service.search(query)


@router.post(
    "/reviews",
    description="Create review.",
    response_model=Review,
    status_code=201
)
async def create_review(
        review: Review,
        service: UserReviewsService = Depends(get_user_reviews_service),
        user_id: str = Depends(auth),
) -> dict:
    return await service.add(user_id, review)


@router.get(
    "/reviews/{review_id}",
    description="Get review.",
    response_model=Review
)
async def get_review(
        review_id: PydanticObjectId = Query(None, description="Review ID"),
        service: UserReviewsService = Depends(get_user_reviews_service),
) -> dict:

    try:
        review = await service.get(review_id)
    except DocumentNotFound:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

    return review


@router.delete(
    "/reviews/{review_id}",
    description="Remove review."
)
async def delete_review(
        review_id: str = Query(None, description="Review ID"),
        service: UserReviewsService = Depends(get_user_reviews_service),
        user_id: str = Depends(auth),
):
    review_id = PydanticObjectId(review_id)
    try:
        await service.remove(user_id, review_id)
    except NotAllowed:
        raise HTTPException(status_code=HTTPStatus.METHOD_NOT_ALLOWED)
    except DocumentNotFound:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)


@router.patch(
    "/reviews/{review_id}",
    description="Update review.",
    response_model=Review
)
async def update_review(
        review: Review,
        review_id: str = Query(None, description="Review ID"),
        service: UserReviewsService = Depends(get_user_reviews_service),
        user_id: str = Depends(auth),
) -> None:

    review_id = PydanticObjectId(review_id)
    try:
        await service.update(user_id, review_id, review)
    except NotAllowed:
        raise HTTPException(status_code=HTTPStatus.METHOD_NOT_ALLOWED)
    except DocumentNotFound:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

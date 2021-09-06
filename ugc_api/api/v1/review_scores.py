import logging

from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Query, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPBasicCredentials

from models.base import PydanticObjectId
from services.exceptions import DocumentNotFound, NotAllowed
from services.review_scores import UserReviewScoresService, get_user_review_scores_service
from services.auth import get_user_id, AuthServiceUnavailable
from models.review_score import ReviewScore

router = APIRouter()
logger = logging.getLogger(__name__)

auth_scheme = HTTPBearer()


@router.post("/reviews/scores/", response_model=ReviewScore, description="Add score to review.")
async def create_review_score(
        review_score: ReviewScore,
        service: UserReviewScoresService = Depends(get_user_review_scores_service),
        credentials: HTTPBasicCredentials = Depends(auth_scheme),
):
    token = credentials.credentials
    try:
        user_id = await get_user_id(token)
    except AuthServiceUnavailable:
        raise HTTPException(status_code=HTTPStatus.SERVICE_UNAVAILABLE)

    return await service.add(user_id, review_score)


@router.patch(
    "/reviews/scores/{review_score_id}",
    description="Update review score.",
    response_model=ReviewScore
)
async def update_review(
        review_score: ReviewScore,
        review_score_id: str,
        service: UserReviewScoresService = Depends(get_user_review_scores_service),
        credentials: HTTPBasicCredentials = Depends(auth_scheme),
):
    token = credentials.credentials
    try:
        user_id = await get_user_id(token)
    except AuthServiceUnavailable:
        raise HTTPException(status_code=HTTPStatus.SERVICE_UNAVAILABLE)

    review_score_id = PydanticObjectId(review_score_id)
    try:
        updated = await service.update(user_id, review_score_id, review_score)
    except NotAllowed:
        raise HTTPException(status_code=HTTPStatus.METHOD_NOT_ALLOWED)
    except DocumentNotFound:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

    return updated


@router.delete("/reviews/scores/{review_score_id}", description="Remove review score.")
async def delete_review_score(
        review_score_id: str,
        service: UserReviewScoresService = Depends(get_user_review_scores_service),
        credentials: HTTPBasicCredentials = Depends(auth_scheme),
):
    token = credentials.credentials
    try:
        user_id = await get_user_id(token)
    except AuthServiceUnavailable:
        raise HTTPException(status_code=HTTPStatus.SERVICE_UNAVAILABLE)

    review_score_id = PydanticObjectId(review_score_id)
    try:
        await service.remove(user_id, review_score_id)
    except NotAllowed:
        raise HTTPException(status_code=HTTPStatus.METHOD_NOT_ALLOWED)
    except DocumentNotFound:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)


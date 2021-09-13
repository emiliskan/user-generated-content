import pytest
from settings import API_SERVICE_URL, API

API_URL = f"{API_SERVICE_URL}/api/{API}/reviews/scores"
API_REVIEWS_URL = f"{API_SERVICE_URL}/api/{API}/reviews"


REVIEW_ID = "613fbddfa3ff7e7f63a81463"


@pytest.mark.asyncio
async def test_create_review(headers, make_post_request):
    data = {
        "id": REVIEW_ID,
        "movie_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "text": "New text."
    }
    response = await make_post_request(
        f"{API_REVIEWS_URL}/",
        data=data,
        headers=headers
    )

    assert response.status == 201, "Couldn't create review."


@pytest.mark.asyncio
async def test_add_review_score(headers, make_post_request, make_get_request):
    response = await make_get_request(f"{API_REVIEWS_URL}/{REVIEW_ID}",
                                      headers=headers)
    assert response.status == 200, "Couldn't get review."
    review = response.body

    data = {
        "review_id": REVIEW_ID,
        "score": 10
    }
    response = await make_post_request(
        f"{API_URL}/",
        data=data,
        headers=headers
    )
    assert response.status == 201, "Couldn't add review score."

    response = await make_get_request(f"{API_REVIEWS_URL}/{REVIEW_ID}",
                                      headers=headers)
    assert response.status == 200, "Couldn't get review."
    assert response.body["scores_quality"] == review["scores_quality"] + 1
    assert response.body["rating"] >= review["rating"]


@pytest.mark.asyncio
async def test_delete_review_score(headers, make_get_request,
                                   make_delete_request):
    response = await make_get_request(f"{API_REVIEWS_URL}/{REVIEW_ID}",
                                      headers=headers)
    assert response.status == 200, "Couldn't get review."
    review = response.body
    assert review["scores_quality"] != 0, "Review doesn't have scores"

    review_score_id = review["scores"][0]
    response = await make_delete_request(f"{API_URL}/{review_score_id}",
                                         headers=headers)
    assert response.status == 200, "Couldn't delete review score."

    response = await make_get_request(f"{API_URL}/{review_score_id}",
                                      headers=headers)
    assert response.status == 404, "Couldn't delete review score."

    response = await make_get_request(f"{API_REVIEWS_URL}/{REVIEW_ID}",
                                      headers=headers)
    assert response.status == 200, "Couldn't get review."
    assert review["scores_quality"] > response.body["scores_quality"]


@pytest.mark.asyncio
async def test_delete_review(headers,make_get_request, make_delete_request):
    response = await make_delete_request(f"{API_REVIEWS_URL}/{REVIEW_ID}",
                                         headers=headers)
    assert response.status == 200, "Couldn't delete review."

    response = await make_get_request(f"{API_REVIEWS_URL}/{REVIEW_ID}",
                                      headers=headers)
    assert response.status == 404, "Couldn't delete review"

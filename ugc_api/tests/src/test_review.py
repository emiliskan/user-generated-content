import pytest
from settings import API_SERVICE_URL, API

API_URL = f"{API_SERVICE_URL}/api/{API}/reviews"

REVIEW_ID = "613fbddfa3ff7e7f63a81463"


@pytest.mark.asyncio
async def test_create_review(headers, make_post_request):
    data = {
        "id": REVIEW_ID,
        "movie_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "text": "New text."
    }
    response = await make_post_request(
        f"{API_URL}/",
        data=data,
        headers=headers
    )

    assert response.status == 201, "Couldn't create review."


@pytest.mark.asyncio
async def test_get_reviews(headers, make_get_request):
    data = {"filters": {}, "offset": 0, "limit": 10}
    response = await make_get_request(
        f"{API_URL}/",
        data=data,
        headers=headers
    )
    assert response.status == 200, "Couldn't get review list."


@pytest.mark.asyncio
async def test_update_review(headers, make_patch_request):
    data = {
        "movie_id": "0cbc2d7c-fcb0-486d-89e8-905c38a196ed",
        "text": "New text."
    }
    response = await make_patch_request(
        f"{API_URL}/{REVIEW_ID}",
        data=data,
        headers=headers
    )
    assert response.status == 200, "Couldn't update review."


@pytest.mark.asyncio
async def test_delete_review(headers, make_delete_request,
                             make_get_request):
    response = await make_delete_request(f"{API_URL}/{REVIEW_ID}",
                                         headers=headers)
    assert response.status == 200, "Couldn't delete review."

    response = await make_get_request(f"{API_URL}/{REVIEW_ID}",
                                      headers=headers)
    assert response.status == 404

import pytest
from settings import API_SERVICE_URL, API

API_URL = f"{API_SERVICE_URL}/api/{API}/reviews"


@pytest.mark.asyncio
async def test_create_review(auth, make_post_request, make_get_request, make_patch_request, make_delete_request):

    headers = {
        "Authorization": f"Bearer {auth}"
    }

    data = {
        "movie_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "text": "New text."
    }
    response = await make_post_request(
        f"{API_URL}/",
        data=data,
        headers=headers
    )
    assert response.status == 200, "Couldn't create review."
    review_id = response.body["_id"]

    # list
    data = {
        "filters": {},
        "offset": 0,
        "limit": 10,
    }
    response = await make_get_request(
        f"{API_URL}/",
        data=data,
        headers=headers
    )
    assert response.status == 200, "Couldn't get review list."

    # get
    response = await make_get_request(f"{API_URL}/{review_id}", headers=headers)
    assert response.status == 200, "Couldn't get review."

    # update
    data = {
        "movie_id": "0cbc2d7c-fcb0-486d-89e8-905c38a196ed",
        "text": "New text."
    }
    response = await make_patch_request(
        f"{API_URL}/{review_id}",
        data=data,
        headers=headers
    )
    assert response.status == 200, "Couldn't update review."

    # delete
    response = await make_delete_request(f"{API_URL}/{review_id}", headers=headers)
    assert response.status == 200, "Couldn't delete review."

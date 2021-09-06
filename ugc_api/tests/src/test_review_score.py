import pytest
from settings import API_SERVICE_URL, API

API_URL = f"{API_SERVICE_URL}/api/{API}/reviews/scores"
API_REVIEWS_URL = f"{API_SERVICE_URL}/api/{API}/reviews"


@pytest.mark.asyncio
async def test_review_scores(auth, make_post_request, make_get_request, make_patch_request, make_delete_request):

    headers = {
        "Authorization": f"Bearer {auth}"
    }

    data = {
        "_id": "61366713518a6389d3ed7ee7",
        "movie_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "text": "New text.",
    }
    response = await make_post_request(
        f"{API_REVIEWS_URL}/",
        data=data,
        headers=headers
    )
    assert response.status == 200, "Couldn't create review."
    review_id = response.body["_id"]

    # add score
    data = {
        "review_id": review_id,
        "score": 1,
    }
    response = await make_post_request(
        f"{API_URL}/",
        data=data,
        headers=headers
    )
    assert response.status == 200
    review_score_id_1 = response.body["_id"]

    data = {
        "review_id": review_id,
        "score": 10,
    }
    response = await make_post_request(
        f"{API_URL}/",
        data=data,
        headers=headers
    )
    assert response.status == 200
    review_score_id_2 = response.body["_id"]

    # check score
    response = await make_get_request(f"{API_REVIEWS_URL}/{review_id}", headers=headers)
    assert response.body["rating"] == 5.5
    assert response.body["scores_quality"] == 2

    # delete first
    response = await make_delete_request(f"{API_URL}/{review_score_id_1}", headers=headers)
    assert response.status == 200, "Couldn't delete review score."

    # check score
    response = await make_get_request(f"{API_REVIEWS_URL}/{review_id}", headers=headers)
    assert response.body["rating"] == 10
    assert response.body["scores_quality"] == 1

    # update
    data = {
        "review_id": review_id,
        "score": 1,
    }
    response = await make_patch_request(
        f"{API_URL}/{review_score_id_2}",
        data=data,
        headers=headers
    )
    assert response.status == 200, "Couldn't update review."

    # check score
    response = await make_get_request(f"{API_REVIEWS_URL}/{review_id}", headers=headers)
    assert response.body["rating"] == 1
    assert response.body["scores_quality"] == 1

    # delete second
    response = await make_delete_request(f"{API_URL}/{review_score_id_2}", headers=headers)
    assert response.status == 200, "Couldn't delete review score."

    # check score
    response = await make_get_request(f"{API_REVIEWS_URL}/{review_id}", headers=headers)
    assert response.body["rating"] == 0
    assert response.body["scores_quality"] == 0

    # delete review
    response = await make_delete_request(f"{API_REVIEWS_URL}/{review_id}", headers=headers)
    assert response.status == 200, "Couldn't delete review."

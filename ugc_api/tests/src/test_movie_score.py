import pytest
from settings import API_SERVICE_URL, API

API_URL = f"{API_SERVICE_URL}/api/{API}/scores/movie_score"


@pytest.mark.asyncio
async def test_movie_score(auth, make_post_request, make_patch_request,
                           make_delete_request, make_get_request):

    headers = {
        "Authorization": f"Bearer {auth}"
    }

    score_info = {
        "movie_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "score": 5
    }

    response = await make_post_request(f"{API_URL}", data=score_info, headers=headers)

    assert response.status == 201, "Couldn't create movie score."
    assert len(response.body) == 4, "Couldn't get movie score."

    score_info = {
        "id": response.body.get("_id"),
        "movie_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "score": 6
    }

    response = await make_patch_request(f"{API_URL}", data=score_info, headers=headers)
    assert response.status == 200, "Couldn't update movie score."
    assert response.body.get("score") == 6, "Couldn't change movie score."

    _id = response.body.get("_id")

    response = await make_get_request(f"{API_URL}/{_id}", headers=headers)
    assert response.status == 200

    response = await make_delete_request(f"{API_URL}/{_id}", headers=headers)
    assert response.status == 200, "Couldn't remove movie score."

    response = await make_get_request(f"{API_URL}/{_id}", headers=headers)
    assert response.status == 404




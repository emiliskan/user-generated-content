import pytest
from settings import API_SERVICE_URL, API

API_URL = f"{API_SERVICE_URL}/api/{API}/scores/movie_score"

MOVIE_ID = "3fa85f64-5717-4562-b3fc-2c963f66afa6"


@pytest.mark.asyncio
async def test_create_movie_score(headers, make_post_request):

    score_info = {"movie_id": MOVIE_ID, "score": 5}
    response = await make_post_request(f"{API_URL}", data=score_info,
                                       headers=headers)

    assert response.status == 201, "Couldn't create movie score."
    assert len(response.body) == 4, "Couldn't get movie score."


@pytest.mark.asyncio
async def test_get_movie_score(headers, make_get_request):
    response = await make_get_request(f"{API_URL}/{MOVIE_ID}",
                                      headers=headers)
    assert response.status == 200


@pytest.mark.asyncio
async def test_update_movie_score(headers, make_patch_request):
    data = {"movie_id": MOVIE_ID, "score": 6}
    response = await make_patch_request(f"{API_URL}", data=data,
                                        headers=headers)
    assert response.status == 200, "Couldn't update movie score."
    assert response.body.get("score") == 6, "Couldn't change movie score."


@pytest.mark.asyncio
async def test_delete_movie_score(headers, make_delete_request,
                                  make_get_request):
    response = await make_delete_request(f"{API_URL}/{MOVIE_ID}",
                                         headers=headers)
    assert response.status == 200, "Couldn't remove movie score."

    response = await make_get_request(f"{API_URL}/{MOVIE_ID}",
                                      headers=headers)
    assert response.status == 404

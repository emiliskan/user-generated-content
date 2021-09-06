import pytest
from settings import API_SERVICE_URL, API

API_URL = f"{API_SERVICE_URL}/api/{API}/scores/movies"


@pytest.mark.asyncio
async def test_movie_score(make_get_request):

    movie_id = "3fa85f64-5717-4562-b3fc-2c963f66afa6"
    response = await make_get_request(f"{API_URL}/{movie_id}")

    assert response.status == 200, "Couldn't find movie."

import pytest

API_URL = 'movies/save_movie_progress'


@pytest.mark.asyncio
async def test_save_movie_progress(make_get_request, auth):
    movie_id = 1
    viewed_frame = 1000

    token = await auth()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = await make_get_request(
        method=f"{API_URL}?movie_id={movie_id}&viewed_frame={viewed_frame}",
        headers=headers
    )
    assert response.status == 200, "UCG service unavailable"


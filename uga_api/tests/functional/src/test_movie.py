import pytest
import pytest_cases

API_URL = 'movies/save_movie_progress'


@pytest_cases.parametrize(
    "movie_id, viewed_frame",
    [
        ("31cecdfc-3a35-4ca6-8816-47456f6e513e", 2000),
    ],
)
@pytest.mark.asyncio
async def test_save_movie_progress(movie_id, viewed_frame,
                                   make_get_request, auth):

    headers = {
        "Authorization": f"Bearer {auth}"
    }
    response = await make_get_request(
        method=f"{API_URL}?movie_id={movie_id}&viewed_frame={viewed_frame}",
        headers=headers
    )
    assert response.status == 200, "Couldn't save movie progress."

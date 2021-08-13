import pytest
from fastapi import status
import pytest_cases

API_URL = "genres"


@pytest_cases.parametrize(
    "genre_id, http_status",
    [
        ("31cecdfc-3a35-4ca6-8816-47456f6e513e", status.HTTP_200_OK),
        ("111", status.HTTP_404_NOT_FOUND),
    ],
)
@pytest.mark.asyncio
async def test_genre_detail(genre_id, http_status, make_get_request):
    response = await make_get_request(method=f"{API_URL}/{genre_id}")
    assert response.status == http_status
    if http_status == status.HTTP_200_OK:
        assert response.body.get("id") == genre_id


@pytest_cases.parametrize(
    "count_genres, http_status, params",
    [
        (10, status.HTTP_200_OK, {}),
        (1, status.HTTP_200_OK, {"page": 1, "size": 1}),
        (5, status.HTTP_200_OK, {"page": 2, "size": 5}),
        (None, status.HTTP_404_NOT_FOUND, {"page": 3, "size": 5}),
    ],
)
@pytest.mark.asyncio
async def test_persons_list(count_genres, http_status, params, make_get_request):
    response = await make_get_request(method=API_URL, params=params)
    assert response.status == http_status
    if count_genres:
        assert len(response.body) == count_genres

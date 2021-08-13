import pytest
import pytest_cases
from fastapi import status

API_URL = "film"


@pytest_cases.parametrize(
    "film_id, http_status",
    [("88218caf-1abe-40a9-a533-da14884d6a5c", status.HTTP_200_OK), ("111", status.HTTP_404_NOT_FOUND)],
)
@pytest.mark.asyncio
async def test_film_detail(film_id, http_status, make_get_request):
    response = await make_get_request(method=f"{API_URL}/{film_id}")
    assert response.status == http_status
    if http_status == status.HTTP_200_OK:
        assert response.body.get("id") == film_id


@pytest_cases.parametrize(
    "rating, http_status, params",
    [(8.7, status.HTTP_200_OK, {"sort": "-imdb_rating"}), (2.1, status.HTTP_200_OK, {"sort": "imdb_rating"})],
)
@pytest.mark.asyncio
async def test_film_search_sort(rating, http_status, params, make_get_request):
    response = await make_get_request(method=API_URL, params=params)
    assert response.status == http_status
    assert response.body[0].get("imdb_rating") == rating


@pytest_cases.parametrize(
    "count_film, http_status, params",
    [
        (10, status.HTTP_200_OK, {}),
        (1, status.HTTP_200_OK, {"page": 1, "size": 1}),
        (5, status.HTTP_200_OK, {"page": 2, "size": 5}),
        (None, status.HTTP_404_NOT_FOUND, {"page": 3, "size": 5}),
        (None, status.HTTP_422_UNPROCESSABLE_ENTITY, {"page": -1, "size": 5}),
        (3, status.HTTP_200_OK, {"filter[genre]": "Documentary"}),
        (2, status.HTTP_200_OK, {"filter[genre]": "Short"}),
        (2, status.HTTP_200_OK, {"query": "Characters"}),
        (10, status.HTTP_200_OK, {"query": "Star"}),
    ],
)
@pytest.mark.asyncio
async def test_film_search_page_and_filter(count_film, http_status, params, make_get_request):
    response = await make_get_request(method=API_URL, params=params)
    assert response.status == http_status
    if count_film:
        assert len(response.body) == count_film


@pytest.mark.asyncio
async def test_film_cache(redis_client, make_get_request):
    await redis_client.flushall()
    response = await make_get_request(method=API_URL)
    all_keys = await redis_client.keys("**")
    assert len(all_keys) == 1

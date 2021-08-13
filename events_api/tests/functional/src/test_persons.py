import pytest
import pytest_cases
from fastapi import status

API_URL = "persons"


@pytest_cases.parametrize(
    "person_id, http_status",
    [
        ("756c6ff4-232d-4458-9850-fa24a75dfc37", status.HTTP_200_OK),
        ("111", status.HTTP_404_NOT_FOUND),
    ],
)
@pytest.mark.asyncio
async def test_person_detail(person_id, http_status, make_get_request):
    response = await make_get_request(method=f"{API_URL}/{person_id}")
    assert response.status == http_status
    if http_status == status.HTTP_200_OK:
        assert response.body.get("id") == person_id


@pytest_cases.parametrize(
    "count_persons, http_status, params",
    [
        (1, status.HTTP_200_OK, {"query": "Chip"}),
        (2, status.HTTP_200_OK, {"query": "Michael"}),
        (None, status.HTTP_404_NOT_FOUND, {"query": "Star"})
    ],
)
@pytest.mark.asyncio
async def test_persons_search(count_persons, http_status, params, make_get_request):
    response = await make_get_request(method=f"{API_URL}/search", params=params)
    assert response.status == http_status
    if count_persons:
        assert len(response.body) == count_persons


@pytest_cases.parametrize(
    "count_persons, http_status, params",
    [
        (10, status.HTTP_200_OK, {}),
        (1, status.HTTP_200_OK, {"page": 1, "size": 1}),
        (5, status.HTTP_200_OK, {"page": 2, "size": 5}),
        (None, status.HTTP_404_NOT_FOUND, {"page": 3, "size": 5}),
    ],
)
@pytest.mark.asyncio
async def test_persons_list(count_persons, http_status, params, make_get_request):
    response = await make_get_request(method=API_URL, params=params)
    assert response.status == http_status
    if count_persons:
        assert len(response.body) == count_persons


@pytest_cases.parametrize(
    "person_id, http_status, film_count",
    [
        ("756c6ff4-232d-4458-9850-fa24a75dfc37", status.HTTP_200_OK, 1),
        ("645d6985-d8cf-4fee-99aa-9a3ade8a99f6", status.HTTP_200_OK, 2),
    ],
)
@pytest.mark.asyncio
async def test_person_films(person_id, http_status, film_count, make_get_request):
    response = await make_get_request(method=f"{API_URL}/{person_id}/film")
    assert response.status == http_status
    assert len(response.body) == film_count

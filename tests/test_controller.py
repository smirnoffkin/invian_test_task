from datetime import datetime

import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.parametrize("controller_data", [
    ({
        "datetime": "2023-07-18T16:45:14",
        "payload": 0
    }),
    ({
        "datetime": "2023-07-18T17:00:12",
        "payload": 17
    }),
    ({
        "datetime": "2023-07-30T11:32:27",
        "payload": 28
    })
])
async def test_create_controller(client: AsyncClient, controller_data: dict):
    res = await client.post("/controller/", json=controller_data)
    data = res.json()
    assert res.status_code == status.HTTP_201_CREATED
    assert data["success"]
    assert data["datetime"] == controller_data["datetime"]
    assert data["payload"] == controller_data["payload"]


@pytest.mark.parametrize("controller_data", [
    ({
        "datetime": "2023-07-18T16:45:14",
        "payload": 0
    }),
    ({
        "datetime": "2023-07-18T17:00:12",
        "payload": 17
    }),
    ({
        "datetime": "2023-07-30T11:32:27",
        "payload": 28
    })
])
async def test_create_controller_which_already_exists(client: AsyncClient, controller_data: dict):
    res = await client.post("/controller/", json=controller_data)
    assert res.status_code == status.HTTP_400_BAD_REQUEST
    assert res.json() == {"detail": "This controller is already exists"}


@pytest.mark.parametrize("expected", [
    ({
        "datetime": "2023-07-18T16:45:14",
        "status": "UP"
    }),
    ({
        "datetime": "2023-07-18T17:00:12",
        "status": "DOWN"
    }),
    ({
        "datetime": "2023-07-30T11:32:27",
        "status": "UP"
    })
])
async def test_get_controller(client: AsyncClient, expected: dict):
    res = await client.get(f"/controller/{expected['datetime']}")
    data = res.json()
    assert res.status_code == status.HTTP_200_OK
    assert data["datetime"] == expected["datetime"]
    assert data["status"] == expected["status"]


@pytest.mark.parametrize("date", [
    ("2023-08-18T16:45:14"),
    ("2024-07-18T17:00:12"),
    ("2023-07-30T15:32:27")
])
async def test_get_controller_not_exists(client: AsyncClient, date: datetime):
    res = await client.get(f"/controller/{date}")
    assert res.status_code == status.HTTP_404_NOT_FOUND
    assert res.json() == {"detail": "Controller not found."}


@pytest.mark.parametrize("expected", [
    ({
        "datetime": "2023-07-18T16:45:14",
        "status": "UP"
    }),
    ({
        "datetime": "2023-07-18T17:00:12",
        "status": "DOWN"
    }),
    ({
        "datetime": "2023-07-30T11:32:27",
        "status": "UP"
    })
])
async def test_delete_controller(client: AsyncClient, expected: dict):
    res = await client.delete(f"/controller/{expected['datetime']}")
    data = res.json()
    assert res.status_code == status.HTTP_200_OK
    assert data["datetime"] == expected["datetime"]
    assert data["status"] == expected["status"]


@pytest.mark.parametrize("date", [
    ("2023-07-18T16:45:14"),
    ("2024-07-18T17:00:12"),
    ("2023-07-30T15:32:27")
])
async def test_delete_post_not_exists(client: AsyncClient, date: datetime):
    res = await client.delete(f"/controller/{date}")
    assert res.status_code == status.HTTP_404_NOT_FOUND
    assert res.json() == {"detail": "Controller not found."}

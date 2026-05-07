import pytest
import httpx
import pytest_asyncio
from typing import AsyncGenerator

BASE_URL = "http://localhost:8000/api"


def unwrap(response: httpx.Response):
    """Unwrap unified response format {data, error}."""
    body = response.json()
    return body.get("data"), body.get("error")


@pytest_asyncio.fixture
async def client() -> AsyncGenerator[httpx.AsyncClient, None]:
    async with httpx.AsyncClient(base_url=BASE_URL, follow_redirects=True) as c:
        yield c


@pytest.mark.asyncio
class TestAgentAPI:
    async def test_get_agents(self, client: httpx.AsyncClient):
        """Test listing all agents (seeded data exists)."""
        response = await client.get("/agents")
        assert response.status_code == 200
        data, error = unwrap(response)
        assert error is None
        assert isinstance(data, list)
        assert len(data) >= 10  # 10 seeded agents

    async def test_get_agent_by_id(self, client: httpx.AsyncClient):
        """Test getting a single agent by ID."""
        # First, get the list to find a valid ID
        list_resp = await client.get("/agents")
        data, _ = unwrap(list_resp)
        first = data[0]
        agent_id = first["id"]

        response = await client.get(f"/agents/{agent_id}")
        assert response.status_code == 200
        data, error = unwrap(response)
        assert error is None
        assert data["id"] == agent_id
        assert data["name"] == first["name"]

    async def test_get_agent_not_found(self, client: httpx.AsyncClient):
        """Test getting a non-existent agent returns 404 with error body."""
        response = await client.get("/agents/non-existent-id")
        assert response.status_code == 404
        data, error = unwrap(response)
        assert data is None
        assert error["code"] == "NOT_FOUND"

    async def test_agent_tasks(self, client: httpx.AsyncClient):
        """Test getting tasks assigned to an agent."""
        list_resp = await client.get("/agents")
        data, _ = unwrap(list_resp)
        agent_id = data[0]["id"]
        response = await client.get(f"/agents/{agent_id}/tasks")
        assert response.status_code == 200
        data, error = unwrap(response)
        assert error is None
        assert isinstance(data, list)


@pytest.mark.asyncio
class TestTaskAPI:
    async def test_create_task_success(self, client: httpx.AsyncClient):
        """Test successfully creating a task."""
        payload = {
            "title": "测试任务",
            "description": "这是一个测试任务描述",
            "priority": "high",
            "status": "todo",
        }
        response = await client.post("/tasks", json=payload)
        assert response.status_code == 201
        data, error = unwrap(response)
        assert error is None
        assert data["title"] == payload["title"]
        assert "id" in data
        return data["id"]

    async def test_get_tasks_list(self, client: httpx.AsyncClient):
        """Test listing tasks with priority filter."""
        await client.post("/tasks", json={"title": "Low priority task", "priority": "low"})
        await client.post("/tasks", json={"title": "High priority task", "priority": "high"})

        response = await client.get("/tasks", params={"priority": "low"})
        assert response.status_code == 200
        data, error = unwrap(response)
        assert error is None
        assert all(t["priority"] == "low" for t in data)

    async def test_update_task_status(self, client: httpx.AsyncClient):
        """Test updating a task's status."""
        create_resp = await client.post("/tasks", json={"title": "Update Test", "status": "todo"})
        task_id = unwrap(create_resp)[0]["id"]

        update_resp = await client.put(f"/tasks/{task_id}", json={"status": "in_progress"})
        assert update_resp.status_code == 200
        data, error = unwrap(update_resp)
        assert error is None
        assert data["status"] == "in_progress"

    async def test_delete_task(self, client: httpx.AsyncClient):
        """Test deleting a task and verifying it is gone."""
        create_resp = await client.post("/tasks", json={"title": "Delete Test"})
        task_id = unwrap(create_resp)[0]["id"]

        delete_resp = await client.delete(f"/tasks/{task_id}")
        assert delete_resp.status_code == 204

        get_resp = await client.get(f"/tasks/{task_id}")
        assert get_resp.status_code == 404
        _, error = unwrap(get_resp)
        assert error["code"] == "NOT_FOUND"

    async def test_move_task(self, client: httpx.AsyncClient):
        """Test moving a task between columns."""
        create_resp = await client.post("/tasks", json={"title": "Move Test"})
        task_id = unwrap(create_resp)[0]["id"]

        move_resp = await client.patch(
            f"/tasks/{task_id}/move",
            json={"column_id": "col-in-progress", "column_position": 1.0},
        )
        assert move_resp.status_code == 200
        data, error = unwrap(move_resp)
        assert error is None
        assert data["column_id"] == "col-in-progress"


@pytest.mark.asyncio
class TestColumnAPI:
    async def test_get_columns(self, client: httpx.AsyncClient):
        """Test listing columns with their tasks."""
        response = await client.get("/columns")
        assert response.status_code == 200
        data, error = unwrap(response)
        assert error is None
        assert len(data) >= 4
        names = [c["name"] for c in data]
        assert "待办" in names
        for col in data:
            assert "tasks" in col


@pytest.mark.asyncio
class TestEdgeCases:
    async def test_create_task_invalid_data(self, client: httpx.AsyncClient):
        """Test creating a task without required fields."""
        response = await client.post("/tasks", json={"description": "No title"})
        assert response.status_code == 422

    async def test_update_task_invalid_status(self, client: httpx.AsyncClient):
        """Test updating a task with an invalid status value."""
        response = await client.put("/tasks/any-id", json={"status": "invalid-status"})
        assert response.status_code in (422, 404)

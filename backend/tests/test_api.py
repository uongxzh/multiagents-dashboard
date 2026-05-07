import pytest
import httpx
import pytest_asyncio
from typing import AsyncGenerator

BASE_URL = "http://localhost:8000/api"

@pytest_asyncio.fixture
async def client() -> AsyncGenerator[httpx.AsyncClient, None]:
    async with httpx.AsyncClient(base_url=BASE_URL, follow_redirects=True) as client:
        yield client

@pytest.mark.asyncio
class TestAgentAPI:
    async def test_get_agents_empty(self, client: httpx.AsyncClient):
        """测试获取 Agent 列表（初始状态或空数据）"""
        response = await client.get("/agents")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    async def test_get_agent_not_found(self, client: httpx.AsyncClient):
        """测试获取不存在的 Agent"""
        response = await client.get("/agents/non-existent-id")
        assert response.status_code == 404

@pytest.mark.asyncio
class TestTaskAPI:
    async def test_create_task_success(self, client: httpx.AsyncClient):
        """测试成功创建任务"""
        payload = {
            "title": "测试任务",
            "description": "这是一个测试任务描述",
            "priority": "high",
            "status": "todo"
        }
        response = await client.post("/tasks", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == payload["title"]
        assert "id" in data
        return data["id"]

    async def test_get_tasks_list(self, client: httpx.AsyncClient):
        """测试获取任务列表并筛选"""
        # 先创建一个任务
        await client.post("/tasks", json={"title": "Filter Test", "priority": "low"})
        
        response = await client.get("/tasks", params={"priority": "low"})
        assert response.status_code == 200
        tasks = response.json()
        assert all(t["priority"] == "low" for t in tasks)

    async def test_update_task_status(self, client: httpx.AsyncClient):
        """测试更新任务状态"""
        # 1. 创建任务
        create_res = await client.post("/tasks", json={"title": "Update Test", "status": "todo"})
        task_id = create_res.json()["id"]

        # 2. 更新为 in_progress
        update_res = await client.put(f"/tasks/{task_id}", json={"status": "in_progress"})
        assert update_res.status_code == 200
        assert update_res.json()["status"] == "in_progress"

    async def test_delete_task(self, client: httpx.AsyncClient):
        """测试删除任务"""
        # 1. 创建
        create_res = await client.post("/tasks", json={"title": "Delete Test"})
        task_id = create_res.json()["id"]

        # 2. 删除
        delete_res = await client.delete(f"/tasks/{task_id}")
        assert delete_res.status_code == 204

        # 3. 验证已删除
        get_res = await client.get(f"/tasks/{task_id}")
        assert get_res.status_code == 404

@pytest.mark.asyncio
class TestColumnAPI:
    async def test_get_columns(self, client: httpx.AsyncClient):
        """测试获取看板列"""
        response = await client.get("/columns")
        assert response.status_code == 200
        columns = response.json()
        assert len(columns) >= 4  # 默认应有 待办/进行中/审核中/已完成
        names = [c["name"] for c in columns]
        assert "待办" in names or "Todo" in names

@pytest.mark.asyncio
class TestEdgeCases:
    async def test_create_task_invalid_data(self, client: httpx.AsyncClient):
        """测试使用无效数据创建任务（边界情况）"""
        # 缺少必填字段 title
        response = await client.post("/tasks", json={"description": "No title"})
        assert response.status_code == 422  # FastAPI 默认验证失败代码

    async def test_update_task_invalid_status(self, client: httpx.AsyncClient):
        """测试更新任务为无效状态"""
        # 假设任务已存在
        response = await client.put("/tasks/any-id", json={"status": "invalid-status"})
        # 即使 ID 不存在，数据验证也可能先失败
        assert response.status_code in [422, 404]

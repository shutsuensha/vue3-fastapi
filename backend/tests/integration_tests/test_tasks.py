import pytest
from app.models.tasks import Task
from httpx import AsyncClient
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.fixture(autouse=True)
async def clear_tables(db: AsyncSession):
    await db.execute(delete(Task))

    yield

    await db.execute(delete(Task))


async def test_read_tasks(ac: AsyncClient, db: AsyncSession):
    new_task = Task(title="Test task", completed=False)
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)

    response = await ac.get("/tasks/")

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert any(task["title"] == "Test task" and task["completed"] is False for task in data)


async def test_create_new_task(ac: AsyncClient, db: AsyncSession):
    payload = {"title": "Create via POST", "completed": False}

    response = await ac.post("/tasks/", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Create via POST"
    assert data["completed"] is False
    assert "id" in data

    task_in_db = await db.get(Task, data["id"])
    assert task_in_db is not None
    assert task_in_db.title == "Create via POST"


async def test_patch_task(ac: AsyncClient, db: AsyncSession):
    task = Task(title="Original title", completed=False)
    db.add(task)
    await db.commit()
    await db.refresh(task)

    patch_data = {"title": "Updated title"}
    response = await ac.patch(f"/tasks/{task.id}", json=patch_data)

    assert response.status_code == 200
    data = response.json()

    assert data["id"] == task.id
    assert data["title"] == "Updated title"
    assert data["completed"] is False

    await db.refresh(task)
    updated = await db.get(Task, task.id)
    assert updated.title == "Updated title"
    assert updated.completed is False


async def test_delete_task(ac: AsyncClient, db: AsyncSession):
    task = Task(title="To be deleted", completed=False)
    db.add(task)
    await db.commit()
    await db.refresh(task)

    response = await ac.delete(f"/tasks/{task.id}")

    assert response.status_code == 204
    assert response.content == b""

    result = await db.execute(select(Task).where(Task.id == task.id))
    deleted_task = result.scalar_one_or_none()
    assert deleted_task is None

import pytest
from app.models.tasks import Task
from app.schemas.tasks import TaskIn, TaskPatch
from app.services.tasks import (
    create_task,
    delete_task,
    get_task_by_id,
    list_tasks,
    update_task,
)
from fastapi import HTTPException
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.fixture(autouse=True)
async def clear_books_table(db: AsyncSession):
    await db.execute(delete(Task))
    await db.commit()

    yield

    await db.execute(delete(Task))
    await db.commit()


async def test_get_task_by_id_success(db: AsyncSession):
    task = Task(title="test title", completed=False)
    db.add(task)
    await db.commit()
    await db.refresh(task)

    fetched_task = await get_task_by_id(db, task_id=task.id)

    assert fetched_task.id == task.id
    assert fetched_task.title == task.title
    assert fetched_task.completed == task.completed


async def test_get_task_by_id_not_found(db: AsyncSession):
    non_existing_id = 9999

    with pytest.raises(HTTPException) as exc_info:
        await get_task_by_id(db, task_id=non_existing_id)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Task not found"


async def test_list_tasks(db: AsyncSession):
    task1 = Task(title="test title1", completed=False)
    task2 = Task(title="test title2", completed=False)
    db.add_all([task1, task2])
    await db.commit()
    await db.refresh(task1)
    await db.refresh(task2)

    tasks = await list_tasks(db)

    assert len(tasks) == 2
    titles = [task.title for task in tasks]
    assert "test title1" in titles
    assert "test title2" in titles


async def test_create_task_success(db: AsyncSession):
    task_data = TaskIn(title="test title", completed=False)

    task = await create_task(db, task_data)

    assert task.title == task_data.title
    assert task.completed == task_data.completed


async def test_update_task_success(db: AsyncSession):
    task = Task(title="test title1", completed=False)
    db.add(task)
    await db.commit()
    await db.refresh(task)

    update_data = TaskIn(title="new task", completed=True)
    updated = await update_task(db, task_id=task.id, task_data=update_data)

    assert updated.id == task.id
    assert updated.title == "new task"
    assert updated.completed


async def test_partial_update_task_success(db: AsyncSession):
    task = Task(title="test title1", completed=False)
    db.add(task)
    await db.commit()
    await db.refresh(task)

    update_data = TaskPatch(completed=True)
    updated = await update_task(db, task_id=task.id, task_data=update_data)

    assert updated.id == task.id
    assert updated.title == "test title1"
    assert updated.completed


async def test_update_task_not_found(db: AsyncSession):
    non_existing_id = 9999
    update_data = TaskIn(title="new title", completed=True)

    with pytest.raises(HTTPException) as exc_info:
        await update_task(db, task_id=non_existing_id, task_data=update_data)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Task not found"


async def test_delete_user_success(db: AsyncSession):
    task = Task(title="test title1", completed=False)
    db.add(task)
    await db.commit()
    await db.refresh(task)

    await delete_task(db, task_id=task.id)

    with pytest.raises(HTTPException) as exc_info:
        await get_task_by_id(db, task_id=task.id)

    assert exc_info.value.status_code == 404


async def test_delete_user_not_found(db: AsyncSession):
    non_existing_id = 9999

    with pytest.raises(HTTPException) as exc_info:
        await delete_task(db, task_id=non_existing_id)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Task not found"

from fastapi import APIRouter, status

from app.dependencies.db import db
from app.schemas.tasks import TaskIn, TaskOut, TaskPatch
from app.services.tasks import create_task, delete_task, list_tasks, update_task

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=list[TaskOut], status_code=status.HTTP_200_OK)
async def read_tasks(session: db) -> list[TaskOut]:
    return await list_tasks(session)


@router.post("/", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
async def create_new_task(task: TaskIn, session: db) -> TaskOut:
    return await create_task(session, task)


@router.patch("/{task_id}", response_model=TaskOut, status_code=status.HTTP_200_OK)
async def partial_update_existing_task(task_id: int, task: TaskPatch, session: db) -> TaskOut:
    return await update_task(session, task_id, task)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_user(task_id: int, session: db):
    await delete_task(session, task_id)

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tasks import Task
from app.schemas.tasks import TaskIn


async def get_task_by_id(session: AsyncSession, task_id: int) -> Task:
    result = await session.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    return task


async def list_tasks(session: AsyncSession) -> list[Task]:
    result = await session.execute(select(Task).order_by(Task.id.desc()))
    return result.scalars().all()


async def create_task(session: AsyncSession, task_data: TaskIn) -> Task:
    new_task = Task(**task_data.model_dump())
    session.add(new_task)
    await session.commit()
    await session.refresh(new_task)
    return new_task


async def update_task(session: AsyncSession, task_id: int, task_data: TaskIn) -> Task:
    task = await get_task_by_id(session, task_id)

    for field, value in task_data.model_dump(exclude_unset=True).items():
        setattr(task, field, value)

    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


async def delete_task(session: AsyncSession, task_id: int) -> None:
    task = await get_task_by_id(session, task_id)
    await session.delete(task)
    await session.commit()

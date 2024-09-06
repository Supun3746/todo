from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import Task, UpdateTask
from database import Todo


async def create_task(session: AsyncSession, task_in: Task):
    task = Todo(**task_in.model_dump())
    session.add(task)
    await session.commit()
    return task


async def get_all_tasks(session: AsyncSession):
    stmt = select(Todo).order_by(Todo.id)
    res = await session.execute(stmt)
    tasks = res.scalars().all()
    return list(tasks)


async def get_task(session: AsyncSession, id: int):
    return await session.get(Todo, id)


async def update_task(
    session: AsyncSession,
    task: Task,
    task_update: UpdateTask,
):
    for name, value in task_update.model_dump().items():
        setattr(task, name, value)
    await session.commit()
    return task


async def delete_task(session: AsyncSession, task: Task):
    await session.delete(task)
    await session.commit()

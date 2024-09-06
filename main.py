import asyncio

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

import crud
import database
from database import create_tables, session_factory
from schemas import Task, UpdateTask

app = FastAPI(title="ToDo list")


@app.post(
    "/create",
    response_model=Task,
    status_code=status.HTTP_201_CREATED,
)
async def create_task(
    task: Task,
    session: AsyncSession = Depends(database.scoped_session_dependency),
):
    return await crud.create_task(session=session, task_in=task)


@app.get("/get-tasks")
async def get_tasks(
    session: AsyncSession = Depends(database.scoped_session_dependency),
):
    return await crud.get_all_tasks(session=session)


@app.get("/{id}")
async def get_task(
    id: int,
    session: AsyncSession = Depends(database.scoped_session_dependency),
):
    return await crud.get_task(session, id)


@app.patch("/{task_id}")
async def update_task(
    task_update: UpdateTask,
    task: Task = Depends(get_task),
    session: AsyncSession = Depends(database.scoped_session_dependency),
):
    return await crud.update_task(session=session, task_update=task_update, task=task)


@app.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    task: Task = Depends(get_task),
    session: AsyncSession = Depends(database.scoped_session_dependency),
):
    await crud.delete_task(session=session, task=task)


if __name__ == "__main__":
    asyncio.run(create_tables())
    uvicorn.run("main:app", reload=True)

from pydantic import BaseModel


class BaseTask(BaseModel):
    task: str
    process: str


class Task(BaseTask):
    pass


class UpdateTask(BaseTask):
    task: str | None = None
    process: str | None = None

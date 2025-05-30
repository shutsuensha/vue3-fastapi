from typing import Optional

from pydantic import BaseModel, ConfigDict


def to_camel(string: str) -> str:
    parts = string.split("_")
    return parts[0] + "".join(word.capitalize() for word in parts[1:])


class TaskIn(BaseModel):
    title: str
    completed: bool


class TaskPatch(BaseModel):
    title: Optional[str] = None
    completed: Optional[bool] = None


class TaskOut(BaseModel):
    id: int
    title: str
    completed: bool

    model_config = ConfigDict(from_attributes=True, alias_generator=to_camel)

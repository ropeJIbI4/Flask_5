from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from typing import List


app = FastAPI()


class Task(BaseModel):
    id: int
    title: str
    description: str
    status: bool


tasks = [
    {
        "id": 1,
        "title": "Учеба",
        "description": "Закрыть хвосты",
        "status": False,
    },
    {
        "id": 2,
        "title": "Работа",
        "description": "Работа без выходных",
        "status": True,
    }
]


@app.get("/tasks", response_model=List[Task])
def read_tasks():
    return tasks


@app.get("/tasks/{task_id}", response_model=Task)
def read_task(task_id: int):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if task:
        return task
    else:
        raise HTTPException(status_code=404, detail=f"Task {task_id} Не найден")


@app.post("/tasks", response_model=Task)
def create_task(task: Task):
    task.id = len(tasks) + 1
    tasks.append(task.dict())
    return task


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task: Task):
    task_to_update = next((t for t in tasks if t["id"] == task_id), None)
    if task_to_update:
        task_to_update.update(task.dict())
        return task_to_update
    else:
        raise HTTPException(status_code=404, detail=f"Task {task_id} Не найден")


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    task_to_delete = next((t for t in tasks if t["id"] == task_id), None)
    if task_to_delete:
        tasks.remove(task_to_delete)
        return {"message": f"Task {task_id} успешно удален"}
    else:
        raise HTTPException(status_code=404, detail=f"Task {task_id} Не найден")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=5000)

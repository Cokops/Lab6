from fastapi import FastAPI
import uvicorn
from fastapi.responses import HTMLResponse

app = FastAPI()


tasks = [
    {"id": 1, "title": "Купить молоко", "done": False},
    {"id": 2, "title": "Сделать уроки", "done": True},
]

@app.get("/tasks")
def get_tasks():
    return tasks

@app.post("/tasks")
def add_task(title: str):
    new_id = len(tasks) + 1
    task = {"id": new_id, "title": title, "done": False}
    tasks.append(task)
    return task

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return HTMLResponse(status_code=404,content="Не найдено!")

@app.put("/tasks/{task_id}/toggle")
def toggle_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = not task["done"]
            return task
        return HTMLResponse(status_code=404,content="Не найдено!")

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    global tasks
    tasks = [t for t in tasks if t["id"] != task_id]
    return {"deleted": task_id, "remaining": len(tasks)}

if __name__ == "__main__":
    uvicorn.run("main:app",reload=True)
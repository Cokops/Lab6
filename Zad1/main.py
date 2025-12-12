from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

languages = [
    {"id": 1, "name": "Русский", "hello": "Привет"},
    {"id": 2, "name": "Английский", "hello": "Hello"},
    {"id": 3, "name": "Испанский", "hello": "Hola"},
    {"id": 4, "name": "Французский", "hello": "Bonjour"},
    {"id": 5, "name": "Немецкий", "hello": "Hallo"},
]

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "langs": languages
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)






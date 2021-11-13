import os

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


app = FastAPI()

templates = Jinja2Templates(directory=os.path.abspath(os.path.expanduser('templates')))


@app.get("/", tags=["Hello"], name="Hello", response_class=HTMLResponse)
async def hello(request: Request):
    return templates.TemplateResponse("hello_template.html", {"request": request, })

from fastapi import FastAPI
from fastapi.responses import HTMLResponse 
from fastapi.templating import Jinja2Templates

app = FastAPI()

@app.get('/', response_class=HTMLResponse)
def get_html():
    try:
        with open('index.html', 'r', encoding='UTF-8') as f:
            html_content = f.read()
        return html_content
    
    except FileExistsError:
        return HTMLResponse(status_code=404, content="<h1>404: Файл не найден</h1>")

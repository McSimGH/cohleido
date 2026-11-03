from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from . import algorithms, models
from .database import engine
from .schemas import ImagesList

# Создаем таблицы в БД (если их нет)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Cohleidoscope API", description="API математической модели когерентных целей")

# Подключаем папку со статикой (фронтенд)
app.mount("/app", StaticFiles(directory="app/static", html=True), name="static")

@app.post("/api/calculate")
def calculate_goals(data: ImagesList):
    images_data = [
        {"id": i+1, "name": img.name, "type": img.type, "tags": img.tags} 
        for i, img in enumerate(data.images)
    ]
    result = algorithms.build_graph_and_calculate(images_data)
    return result
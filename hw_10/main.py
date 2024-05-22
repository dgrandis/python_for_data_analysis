import os
import json
import pandas as pd
import uvicorn

from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from src.utils import prepare_data, train_model, read_model

app = FastAPI()

# Путь к модели
model_path = 'linear_model.pkl'
# Путь до датасета
data_path = 'data/realty_data.csv'


if not os.path.exists(model_path):
    train_data = prepare_data(data_path)
    train_data.to_csv('data/data.csv', index=False)
    model, mae = train_model(train_data)

else:
    model = read_model(model_path)
    with open("data/mae.json", "r") as json_file:
        mae_dict = json.load(json_file)
        mae = mae_dict["mae"]

class ModelRequestData(BaseModel):
    total_square: float
    rooms: int
    floor: int


class Result(BaseModel):
    result: str
    
@app.get("/health")
def health():
    return JSONResponse(content={"message": "I'm totally fine!"}, status_code=200)

@app.get("/predict_get")
def preprocess_data_get(
    total_square: float = Query(..., gt=0, description="Total square of the apartment"),
    rooms: int = Query(..., gt=0, description="Number of rooms in the apartment"),
    floor: int = Query(..., description="Floor of the apartment")
):
    input_data = {"total_square": total_square, "rooms": rooms, "floor": floor}
    input_df = pd.DataFrame(input_data, index=[0])
    result = model.predict(input_df)[0]
    return Result(result=f"{round(result)} +/- {mae}")


@app.post("/predict_post", response_model=Result)
def preprocess_data_post(data: ModelRequestData):
    input_data = data.dict()
    input_df = pd.DataFrame(input_data, index=[0])
    result = model.predict(input_df)[0]
    return Result(result=f"{round(result)} +/- {mae}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
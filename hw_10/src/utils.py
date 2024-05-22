import os
import pickle
import json
import pandas as pd

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error


def prepare_data(data_path):
  train = pd.read_csv(data_path)

  list_drop = ['product_name',
              'period',
              'postcode',
              'address_name',
              'lat',
              'lon',
              'object_type',
              'settlement',
              'district',
              'area',
              'description',
              'source',
              'city']

  train = train.drop(list_drop, axis=1)

  train["rooms"] = train["rooms"].fillna(1)

  train['rooms'] = train['rooms'].astype(int)
  train['floor'] = train['floor'].astype(int)

  return train


def train_model(train):
    X, y = train.drop("price", axis=1), train['price']
    
    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=21)

    model = LinearRegression()
    model.fit(x_train, y_train)
    
    y_pred = model.predict(x_test)
    mae = round(mean_absolute_error(y_test, y_pred))
    
    with open('linear_model.pkl', 'wb') as file:
        pickle.dump(model, file) 
    
    # Запись значения mae в файл JSON формата
    mae_dict = {"mae": mae}
    with open("data/mae.json", "w") as json_file:
        json.dump(mae_dict, json_file)
    
    return model, mae

def read_model(model_path):
    if not os.path.exists(model_path):
        raise FileNotFoundError("Model file not exists")

    with open(model_path, 'rb') as file:
        model = pickle.load(file)

    return model
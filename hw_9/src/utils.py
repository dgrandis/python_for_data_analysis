import os
import pickle

import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import RandomizedSearchCV
from sklearn.pipeline import Pipeline


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
              'source']

  train = train.drop(list_drop, axis=1)

  train["rooms"] = train["rooms"].fillna(1)
  train["city"] = train["city"].fillna("Не указано")

  train['rooms'] = train['rooms'].astype(int)
  train['floor'] = train['floor'].astype(int)

  train = pd.get_dummies(train, drop_first=False)

  return train


def train_model(train):
    X, y = train.drop("price", axis=1), train['price']

    pipeline = Pipeline([("rf_reg", RandomForestRegressor(random_state=42))])

    param_dist = {
        "rf_reg__n_estimators": np.arange(200, 2001, 200),
        "rf_reg__max_features": ["auto", "sqrt", "log2"],
        "rf_reg__max_depth": list(np.arange(10, 101, 10)) + [None],
        "rf_reg__min_samples_split": [2, 5, 10],
        "rf_reg__min_samples_leaf": [1, 2, 4, 8],
        "rf_reg__bootstrap": [True, False]
    }

    rf = RandomizedSearchCV(
        pipeline,
        param_dist,
        cv=5,
        n_iter=1, # 50
        n_jobs=4,
        verbose=1,
    )
    rf.fit(X, y)

    with open('rf_ForestRegressor.pkl', 'wb') as file:
        pickle.dump(rf, file)


def read_model(model_path):
    if not os.path.exists(model_path):
        raise FileNotFoundError("Model file not exists")

    with open(model_path, 'rb') as file:
        model = pickle.load(file)

    return model
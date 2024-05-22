import os

import pandas as pd
import streamlit as st

from src.utils import prepare_data, train_model, read_model

st.set_page_config(
    page_title="Housing valuation",
)

model_path = 'rf_ForestRegressor.pkl'
data_path = 'data/realty_data.csv'

# Общая площадь
total_square = st.sidebar.number_input("Total area",
                                       min_value=8.0,
                                       max_value=2070.0,
                                       value=50.0,
                                       step=1.0)
# Количество комнат
rooms = st.sidebar.selectbox("How many rooms in the flat?", (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13), index=1)

# Этаж
floor = st.slider("What floor the flat is on?", 1, 63, 1)

# Город
city = st.sidebar.selectbox(
    "In which city the flat is located?",
    ('Не указано',
     'Балашиха',
     'Видное',
     'Дзержинский',
     'Долгопрудный',
     'Ивантеевка',
     'Королёв',
     'Котельники',
     'Красногорск',
     'Лобня',
     'Лыткарино',
     'Люберцы',
     'Москва',
     'Московский',
     'Мытищи',
     'Одинцово',
     'Подольск',
     'Пушкино',
     'Реутов',
     'Химки',
     'Щербинка',
     'Щёлково'),
)

inputDF = pd.DataFrame(
    {
        "total_square": total_square,
        "rooms": rooms,
        "floor": floor,
        'city_Балашиха': city == 'Балашиха',
        'city_Видное': city == 'Видное',
        'city_Дзержинский': city ==  'Дзержинский',
        'city_Долгопрудный': city == 'Долгопрудный',
        'city_Ивантеевка': city == 'Ивантеевка',
        'city_Королёв': city == 'Королёв',
        'city_Котельники': city == 'Котельники',
        'city_Красногорск': city == 'Красногорск',
        'city_Лобня': city == 'Лобня',
        'city_Лыткарино': city == 'Лыткарино',
        'city_Люберцы': city == 'Люберцы',
        'city_Москва': city == 'Москва',
        'city_Московский': city == 'Московский',
        'city_Мытищи': city == 'Мытищи',
        'city_Не указано': city == 'Не указано',
        'city_Одинцово': city == 'Одинцово',
        'city_Подольск': city == 'Подольск',
        'city_Пушкино': city == 'Пушкино',
        'city_Реутов': city == 'Реутов',
        'city_Химки': city == 'Химки',
        'city_Щербинка': city == 'Щербинка',
        'city_Щёлково': city == 'Щёлково',

    },
    index=[0],
)

if not os.path.exists(model_path):
    train_data = prepare_data(data_path)
    train_data.to_csv('data/data.csv', index=False)
    train_model(train_data)

model = read_model(model_path)

preds = model.predict(inputDF)

print('Результат: ', preds)

preds = round(preds[0])

print('Результат: ', preds)

st.image("imgs/Housing valuation.png", use_column_width=True)
st.write(f"The cost of the selected accommodation consists of: {preds} ₽")
# Практическое задание #5

# **1. Polars**

1. Считайте датасет из файла train.csv (это данные о выживаемости на Титанике) с помощью polars - **1 балл**

2. Выведите основную информацию о датасете: информацию о типах данных, число пропусков, средние значения и т.д. - **1 балл**

 hint: используйте методы и атрибуты датафрейма: describe(), dtypes, null_count(), mean()...

3. Посчитайте количество пассажиров каждого класса (Pclass) - **1 балл**

 hint: используйте методы: get_column(), value_counts()...

4. Выведите количество выживших мужчин и женщин на корабле - **1 балл**

 hint: используйте методы: groupby(), agg(), pl.col(), sum()...

5. Выведите часть таблицы с пассажирами, возраст которых больше 44 лет - **1 балл**
 
 hint: используйте методы: filter(), pl.col()...


# **2. Ускорение работы с pandas**

1. Считайте датасет из файла train.csv (это данные о выживаемости на Титанике) с помощью pandas

2. Посчитайте средний возраст пассажиров и его стандартное отклонение с помощью bottleneck - **1 балл**

 hint: используйте методы: bn.nanmean(), bn.nanstd()

3. Для каждого пассажира умножьте значение столбца Fare на 1.3 и сохраните результаты как новый столбец Fare_new - **1 балл**

 hint: используйте методы: .itertuples() или apply()

 # **3. Оптимизация типов pandas**

1. Считайте датасет из файла Housing.csv (это данные о ценах домов) с помощью pandas

2. Для каждого столбца определите оптимальный с точки зрения потребления памяти тип данных - напишите свои выводы в комментариях - **2 балла**

3. Поменяйте типы данных столбцов датафрейма на выбранные вами в прошлом пункте и сравните потребление памяти до и после оптимизации - **1 балл**
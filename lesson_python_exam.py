import pandas as pd
import matplotlib.pyplot as plt

# Чтение данных из CSV файла
solar_data = pd.read_csv('solarpower.csv')

# Заполнение пропусков в cum_power
for i in range(0, len(solar_data)-1):
    if solar_data.loc[i, 'cum_power'] == -1:
        prev_val = solar_data.loc[i-1, 'cum_power']
        next_val = solar_data.loc[i+1, 'cum_power']
        solar_data.loc[i, 'cum_power'] = (float(prev_val) + float(next_val)) / 2

# Создание столбца day_power
solar_data['day_power'] = solar_data['cum_power'].diff().fillna(solar_data['cum_power'])

# Преобразование столбца даты в формат datetime
solar_data['date'] = pd.to_datetime(solar_data['date'])

# Создание столбца с периодами (год-месяц)
solar_data['month_year'] = solar_data['date'].dt.to_period('M')

# Группировка по месяц-год и расчет средней ежедневной выработки
monthly_avg = solar_data.groupby('month_year')['day_power'].mean().reset_index()

# Преобразование month_year обратно в datetime для построения графика
monthly_avg['month_year'] = monthly_avg['month_year'].dt.to_timestamp()

# Фильтрация данных для 2017 года
data2017 = solar_data[solar_data['date'].dt.year == 2017]
print(data2017['day_power'].mean())

# Построение графика
plt.figure(figsize=(12, 6))
plt.plot(monthly_avg['month_year'], monthly_avg['day_power'], marker='o')
plt.title('Средняя ежедневная выработка солнечной энергии на каждый месяц-год')
plt.xlabel('Месяц-Год')
plt.ylabel('Средняя ежедневная выработка (кВтч)')
plt.xticks(rotation=45)
plt.grid()
plt.tight_layout()
plt.show()

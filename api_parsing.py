import requests
from bs4 import BeautifulSoup
from datetime import date
import numpy as np
import pandas as pd
import re
import time



def parsing(name_of_city_ww, id_city_pogoda360):

    previous_year = date.today().year - 1

    # Для считывания API
    headers = {
        'user-agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0"
    }

    # 1. World Weather (Средняя температура и скорость ветра за 5 лет соответственно)
    # В эти переменные будут заносится средние температуры
    sum_month_temp = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    sum_wind_speeds = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    # Тут мы используем сайт world-weather, где считываем два вышеуказанных параметра
    for i in range(5):
        year = previous_year - i
        # print(year)
        url_ww = f"https://world-weather.ru/pogoda/russia/{name_of_city_ww}/{year}/"

        response_ww = requests.get(url_ww, headers=headers)
        bs_ww = BeautifulSoup(response_ww.text, "html.parser")

        month_elements = bs_ww.find_all('div', class_='year-temp')
        month_elements = [element.text.strip() for element in month_elements]
        month_temp = []
        for value in month_elements:
            month_temp.append(int(value.split("°")[0]))

        wind_elements = bs_ww.find_all("div", class_="tooltip", title="Скорость ветра")
        wind_speeds = [element.text.strip() for element in wind_elements]
        wind_speeds = [float(value.split("м/с")[0]) for value in wind_speeds]

        sum_month_temp = np.add(sum_month_temp, month_temp)  # тут сумма за 5 лет
        sum_wind_speeds = np.add(sum_wind_speeds, wind_speeds)  # тут сумма за 5 лет

    # тут получаем среднее за 5 лет
    avg_month_temp = sum_month_temp / 5
    avg_wind_speeds = sum_wind_speeds / 5

    # 2. Pogoda360 Кол-во дней с осадками, Кол-во дней с осадками/кол-во дней, кол-во осадков/кол-во дней с осадками

    url_pogoda360 = f'http://russia.pogoda360.ru/{id_city_pogoda360}/avg/'

    response_pogoda360 = requests.get(url_pogoda360, headers=headers)

    rainfall_mm = response_pogoda360.text.strip('chartPrecipDays')

    bs_pogoda360 = BeautifulSoup(response_pogoda360.text, "html.parser")
    first = bs_pogoda360.find('chartTemp')

    function_name = 'chart.drawYBars'
    remaining_text = response_pogoda360.text  # Create a copy
    n_rainfall = []
    h_rainfall = []

    while True:
        match = re.search(f'{function_name}\s*\((.*?)\);', remaining_text, re.DOTALL)
        if not match:
            break
        function_str = match.group(1)

        data = eval(function_str)

        if data[0] == 'chartPrecip':

            data_rainfall = data[1][0]
            for month, rainfall in data_rainfall:
                h_rainfall.append(rainfall)

        if data[0] == 'chartPrecipDays':
            n_rainfall = data[1][0]

        # Тут мы выбираем только необходимые значения
        remaining_text = remaining_text[match.end():]

    n_days = 1
    n_rainfall = 1

    # n_rainfall_div_n = np.divide(n_rainfall, n_days)
    n_rainfall_div_n = 0 if n_days == 0 else np.divide(n_rainfall, n_days)
    # h_rainfall_div_n_rainfall = np.divide(h_rainfall, n_rainfall)
    h_rainfall_div_n_rainfall = 0 if n_rainfall == 0 else np.divide(h_rainfall, n_rainfall)
    # Тут опять сайт world-weather
    # Тут будет парситься 60 страниц 12*5, где в переменной ссылки на страницу есть название месяца
    months_ww = ["january", "february", "march", "april", "may", "june",
                 "july", "august", "september", "october", "november", "december"]

    data = []  # для срдней температуры
    data_n = []  # для кол-ва дней, когда t>
    data_1 = []
    data_2 = []
    data_3 = []
    data_4 = []
    data_5 = []

    for i in range(5):
        year = previous_year = date.today().year - 1 - i
        data_before = []
        num_t_more_25_full = []

        for month in months_ww:
            print(year)
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!month = ', month)

            url_pogodaklimat = f'https://world-weather.ru/pogoda/russia/{name_of_city_ww}/{month}-{year}'
            response_pogodaklimat = requests.get(url_pogodaklimat, headers=headers)
            # print('response_pogodaklimat = ', response_pogodaklimat)
            bs_pogodaklimat = BeautifulSoup(response_pogodaklimat.text, "html.parser")

            weather_month = bs_pogodaklimat.find_all("ul", class_="ww-month")

            # print(weather_month)

            # Loop through each row
            for row in weather_month:
                # Find all temperature elements in the row
                temperatures = row.find_all("li")

                # Extract the temperature text from each element
                num = 0
                num_t_more_25 = 0
                for temperature in temperatures:

                    # Strip any whitespace and degree symbols from the text
                    temperature_text = temperature.text.strip().strip("°")
                    # Print the temperature
                    # print(type(temperature_text))
                    print(temperature_text)
                    if len(temperature_text) != 0:
                        # print('num = ', num)
                        num += 1
                        temperature_text_new = temperature_text[len(str(int(num))):]
                        print('num = ', num)
                        print(len(str(num)))
                        print('temperature_text_new = ', temperature_text_new)
                        temperature_text_new = temperature_text_new.split('°')[0]
                        if temperature_text_new != '':
                            print(int(temperature_text_new))
                            if int(temperature_text_new) > 25:
                                num_t_more_25 += 1

                    # print('num_t_more_25 = ', num_t_more_25)

                print('num_t_more_25_month = ', num_t_more_25)
                print('num = ', num)
                num_t_more_25_month_div_n = float(num_t_more_25) / num
                print('num_t_more_25_month_div_n = ', num_t_more_25_month_div_n)

                data_before.append(num_t_more_25_month_div_n)
                num_t_more_25_full.append(num_t_more_25)

                print("data_before", data_before)

                time.sleep(2)

        if year == (date.today().year - 1):
            data_1 = data_before
            data_n_1 = num_t_more_25_full
        elif year == (date.today().year - 2):
            data_2 = data_before
            data_n_2 = num_t_more_25_full
        elif year == (date.today().year - 3):
            data_3 = data_before
            data_n_3 = num_t_more_25_full
        elif year == (date.today().year - 4):
            data_4 = data_before
            data_n_4 = num_t_more_25_full
        elif year == (date.today().year - 5):
            data_5 = data_before
            data_n_5 = num_t_more_25_full

    for i in range(len(data_1)):
        data.append(data_1[i] + data_2[i] + data_3[i] + data_4[i] + data_5[i])
    print(type(data))
    data = np.array(data) / 5

    for i in range(len(data_n_1)):
        data_n.append(data_n_1[i] + data_n_2[i] + data_n_3[i] + data_n_4[i] + data_n_5[i])
    print(type(data_n))
    data_n = np.array(data_n) / 5

    # Формируем датафрейм

    # Месяцы
    months = ["January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December"]

    df = pd.DataFrame({

        "Month": months,
        "avg_month_temp": avg_month_temp,
        "avg_wind_speeds": avg_wind_speeds,
        "n_rainfall": n_rainfall,
        'n_rainfall_div_n': n_rainfall_div_n,
        'h_rainfall_div_n_rainfall': h_rainfall_div_n_rainfall,
        'h_rainfall': h_rainfall,
        'n_t_div_n': data,
        'n_t': data_n

    })



    return df





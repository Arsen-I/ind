from api_parsing import parsing
from creating_indic import func_ind
import pandas
import openpyxl

def main():
    #Параметры, соответствующие ближайшему населенному пункту

    #id для world weather
    name_of_city_ww = 'pogranichny'

    #id для Pogoda360
    id_city_pogoda360 = 320818

    data = parsing(name_of_city_ww,id_city_pogoda360)
    indicatrices = func_ind((data))



    # indicatrices.to_csv(f'indicatricies_{name_of_city_ww}.csv')
    indicatrices.to_excel(f'indicatricies_{name_of_city_ww}.xlsx',  index=False)







if __name__ == '__main__':
    main()
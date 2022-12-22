Модуль для работы с гидродинамическими моделями в ПО tNavigator

Установка: pip install oilyreports-1.1.tar.gz

Для работы нужны пакеты:
import pandas as pd
import os
import datetime
import getpass

Так же для связи с навигаторовскими классами нужно добавить:
keyword = {'grou':get_all_groups(), 'wells':get_all_wells(), 'mod' : get_all_models(), 'step':get_all_timesteps()}

Список функций:

create_report_dir - Создает папку result и устанавливает ее по умолчанию при записи файлов

dataframe_creater - Функция для преобразования навигаторовского формата в датафрейм pandas
     *args - перечень аргументов для выдачи во фрейм
     dimens - ну тут одно из двух:
       well - для выдачи фрейма по скважинам
       group - для выдачи по группе
     start - дата, с которой формируем фрейм

df_from_histtab - создает pandas Dataframe с данными из таблицы с историей в дизайнере модели.
    paramert_list - параметры для выгрузки, полный список можно получить через get_production_types
    keyword = {'wells': get_well_filter_by_name (name='14').get_wells (), требуемый список скважин
           'mod': get_all_wells_production_tables ()[0], таблица с данными по исптории
           'step': get_all_timesteps()}

interpolate_press_by_sipy - функция для интерполяции и сглаживания давлений,
должны быть столбцы BHPH,THPH
interpolate_prod_by_sipy - функция для сглаживания добычи,
должны быть столбцы QLIQ,WCT

adapt_report -  выдает фрейм данных с основными показателями адаптации модели

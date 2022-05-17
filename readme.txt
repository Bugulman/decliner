Модуль для работы с гидродинамическими моделями в ПО tNavigator

Установка: pip install oilyreports-1.0.tar.gz

Для работы нужны пакеты:
import pandas as pd
import pprint
import os
import datetime
import getpass
import urllib
import sqlalchemy

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
					
adapt_report -  выдает фрейм данных с основными показателями адаптации модели

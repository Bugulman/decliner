#Automaticaly recalculate=true
#Single model=false
# Automaticaly recalculate=true
# Single model=false
import oily_report as olr
import pandas as pd
import pprint
import os
import datetime
import getpass
import urllib
import sqlalchemy

keyword = {'grou': get_all_groups(),
           'wells': get_wells_from_filter ('Фильтр по скважинам 1'),
           'mod': get_all_models(),
           'step': get_all_timesteps()}
user = getpass.getuser()
date = datetime.datetime.strftime(datetime.datetime.now(), '%d.%m.%y')
olr.create_report_dir(path=get_project_folder())
olr.dataframe_creater(wlpt, wlpr, wopt, wopr, wwir, wwit, wbp9, wbhp,
                      start='01.01.2010', **keyword).to_csv(f'wells_to_invest_{user}_{date}.csv')

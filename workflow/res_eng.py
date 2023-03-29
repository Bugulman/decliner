#  Этот файл был сгенерирован тНавигатор v22.4-2430-g74f144146650.
#  Copyright (C) Рок Флоу Динамикс 2005-2022.
#  Все права защищены.

# This file is MACHINE GENERATED! Do not edit.

#api_version=v0.0.77

from __main__.tnav.workflow import *
from tnav_debug_utilities import *
from datetime import datetime, timedelta


declare_workflow (workflow_name="res_eng",
      variables=[])


res_eng_variables = {

}

def res_eng (variables = res_eng_variables):
    pass
    check_launch_method ()


    begin_user_imports ()
    end_user_imports ()

    if False:
        begin_wf_item (index = 1, name = "Отладка")
        workflow_folder ()
        if True:
            pass



            if False:
                begin_wf_item (index = 2, is_custom_code = True)
                from datetime import datetime
                import getpass
                import pandas as pd



                prod_data = get_all_wells_production_tables ()[0]
                w = get_well_by_name (name='10002')


                paramert_list= ['oil', 'water', 'gas', 'liquid', 'gas_injection', 'water_injection', 'thp', 'bhp', 'wefac']

                keyword = {'wells': get_all_wells(),
                           'mod': get_all_wells_production_tables ()[0],
                           'step': get_all_timesteps()}
                           
                coll_name = ['well', 'date']+paramert_list

                user = getpass.getuser()
                date = datetime.strftime(datetime.now(), '%d.%m.%y')
                start_date = datetime.strptime('01.01.1990', '%d.%m.%Y')

                print(prod_data.name, w.name, get_production_types ())
                #paramert_list= get_production_types ()
                df=[]
                for rec in prod_data.get_records(well=w):
                	row=[]
                	row.append(w.name)
                	row.append(rec.get_date().date())
                	row = row+[rec.get_value(type = parametr) for parametr in paramert_list]
                	df.append(row)
                frame = pd.DataFrame(df, columns = coll_name)
                print(frame.info())
                frame.set_index('date', inplace=True)
                frame.sort_values(by=['date'], ascending=True, inplace=True)
                print(frame)

                #for w in get_well_filter_by_name (name='14').get_wells ():
                #	print(w)

                end_wf_item (index = 2)


            if False:
                begin_wf_item (index = 3, is_custom_code = True)
                from datetime import datetime
                import getpass
                import os


                paramert_list= ['oil', 'water', 'gas', 'liquid', 'resv', 'gas_injection', 'water_injection', 'thp', 'bhp', 'wefac']

                keyword = {'wells': get_well_filter_by_name (name='14').get_wells (),
                           'mod': get_all_wells_production_tables ()[0],
                           'step': get_all_timesteps()}

                user = getpass.getuser()
                date = datetime.strftime(datetime.now(), '%d.%m.%y')

                paramert_list= ['oil', 'water', 'gas', 'liquid', 'resv', 'gas_injection', 'water_injection', 'thp', 'bhp', 'wefac']

                def dataframe_creater(paramert_list=paramert_list, start='01.01.1950', **kwarg):
                    """создает pandas Dataframe с данными из таблицы с историей."""
                    import pandas as pd
                    df=[]
                    coll_name = ['well', 'date']+paramert_list
                    start_date = datetime.strptime(start, '%d.%m.%Y')
                    for w in kwarg['wells']:
                         print(w.name)
                         for t in kwarg['mod'].get_records(well=w):
                            if t.get_date().date() >= start_date.date():
                            		row=[]
                            		row.append(w.name)
                            		row.append(t.get_date().date())
                            		row = row+[t.get_value(type = parametr) for parametr in paramert_list]
                            		df.append(row)
                            else:
                                        continue
                    print(coll_name)
                    result = pd.DataFrame(df, columns = coll_name)
                    result.set_index('date', inplace=True)
                    result.sort_values(by=['well', 'date'], ascending=True, inplace=True)
                    return result

                frame = dataframe_creater(start='01.01.2010', **keyword)

                frame.to_csv(f'wells_frame_{user}_{date}.csv')
                print(os.getcwd())
                end_wf_item (index = 3)



        end_wf_item (index = 1)


    begin_wf_item (index = 5, name = "DCA")
    workflow_folder ()
    if True:
        pass



        if False:
            begin_wf_item (index = 6)
            wells_production_table_calculate_wef_by_operation_time (table=find_object (name="hist",
                  type="gt_wells_production_data"))
            end_wf_item (index = 6)


        begin_wf_item (index = 7, is_custom_code = True, name = "через библиотеку")
        import getpass
        import os
        import oily_report as olr
        from datetime import datetime
        import pandas as pd
        import sqlalchemy 

        engine = sqlalchemy.create_engine('postgresql://test:test@localhost:5434/test') 


        keyword = {#'wells': get_all_wells (),
                   'wells': get_well_filter_by_name (name='target').get_wells (),
                   'mod': get_wells_production_table_by_name (name='hist'),
                   'step': get_all_timesteps()}

        user = getpass.getuser()
        date = datetime.strftime(datetime.now(), '%d.%m.%y')
        olr.create_report_dir(get_project_folder ())
        paramert_list= ['oil', 'water', 'gas', 'water_injection', 'bhp', 'thp', 'wefac']


        frame = olr.df_from_histtab(paramert_list=paramert_list, start='01.01.1950', **keyword)
        frame.reset_index(inplace=True)
        frame.to_sql(name ='hist', con=engine)

        smooth_frame = olr.histor_smoothing(frame, gas=True)
        #smooth_frame.to_csv(f'smoooth_wells_{user}_{date}.csv')
        smooth_frame.to_sql(name ='hist_smooth', con=engine)
        predict = pd.DataFrame()#columns=['well', 'date', 'SOIL', 'QOIL', 'Time_x', 'Time_y', 'rate', 'month_prod'])
        to_table = pd.DataFrame()

        for name, fr in smooth_frame.groupby('well'):
        	dca_param = olr.decline_fit(fr, '2000',target_coll='QGAS')
        	try:
        		well_predict = olr.prod_predict(long=120, **dca_param)
        		dca_param = pd.DataFrame([dca_param])
        	except:
        		print(f'Нет профиля для скважины {name}')
        	predict = pd.concat([predict, well_predict], ignore_index=True)
        	to_table = pd.concat([to_table, dca_param], ignore_index=True)


        predict.to_sql(name ='DCA', con=engine)
        to_table.to_sql(name ='DCA_param', con=engine)

        #predict.to_csv(f'predicted_{user}_{date}.csv')
        #to_table.to_csv(f'dca_params_{user}_{date}.csv')
        print(os.getcwd())
        end_wf_item (index = 7)


        if False:
            begin_wf_item (index = 8)
            table_import (splitter=True,
                  file_names=["reports/dca_params_reg16_02.01.23.csv"],
                  splitter2=True,
                  delimiter="comma")
            end_wf_item (index = 8)


        if False:
            begin_wf_item (index = 9)
            wells_history_import_simple_table_format (wells=find_object (name="Wells",
                  type="gt_wells_entity"),
                  well_searcher="name",
                  well_production=find_object (name="dca",
                  type="gt_wells_production_data"),
                  reload_all=False,
                  splitter=True,
                  file_names=["reports/predicted_reg16_09.01.23.csv"],
                  tabulator=TableFormat (separator="comma",
                  comment="",
                  skip_lines=1,
                  columns=["skip", "Date", "skip", "Gas rate", "Well"]),
                  placeholder="-",
                  zero_missing_columns=True,
                  efficiency_factor_units="Relative",
                  date_format="YYYY-MM-DD",
                  use_start_date=False,
                  start_date=datetime (year=2022,
                  month=10,
                  day=6,
                  hour=0,
                  minute=0,
                  second=0),
                  time_format="HH:MM:SS",
                  date_filter=False,
                  first_date=datetime (year=2022,
                  month=10,
                  day=6,
                  hour=0,
                  minute=0,
                  second=0),
                  last_date=datetime (year=2022,
                  month=10,
                  day=6,
                  hour=0,
                  minute=0,
                  second=0),
                  liquid_rate_units="sm3/day",
                  gas_rate_units="sm3/day",
                  reservoir_rate_units="rm3/day",
                  liquid_volume_units="sm3",
                  gas_volume_units="sm3",
                  reservoir_volume_units="rm3",
                  pressure_absolute_units="bara",
                  pressure_units="bara",
                  enthalpy_units="kJ/kg-M",
                  temperature_units="C",
                  mass_concentration_units="kg/sm3",
                  molar_rate_units="kg-m/day",
                  reaction_energy_units="kJ/day",
                  liquid_liquid_units="sm3_div_sm3",
                  fraction_units="fraction",
                  liquid_gas_units="sm3_div_sm3",
                  gas_liquid_units="sm3_div_sm3")
            end_wf_item (index = 9)



    end_wf_item (index = 5)


    begin_wf_item (index = 11, is_custom_code = True)
    import sqlalchemy 
    import urllib 
    import pandas as pd 
     
     

    engine = sqlalchemy.create_engine('postgresql://test:test@localhost:5434/test') 
     
    d = { 
        "one": pd.Series([1.0, 2.0, 3.0], index=["a", "b", "c"]), 
        "two": pd.Series([1.0, 2.0, 3.0, 4.0], index=["a", "b", "c", "d"]), 
    } 
    date = pd.DataFrame(d) 
    date.to_sql(name ='tests', con=engine)
    end_wf_item (index = 11)



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
        begin_wf_item (index = 1, is_custom_code = True)
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

        end_wf_item (index = 1)


    if False:
        begin_wf_item (index = 2, is_custom_code = True)
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
        end_wf_item (index = 2)


    begin_wf_item (index = 3, is_custom_code = True, name = "через библиотеку")
    import getpass
    import os
    import oily_report as olr
    from datetime import datetime



    keyword = {'wells': get_well_filter_by_name (name='14').get_wells (),
               'mod': get_all_wells_production_tables ()[0],
               'step': get_all_timesteps()}

    user = getpass.getuser()
    date = datetime.strftime(datetime.now(), '%d.%m.%y')
    olr.create_report_dir(get_project_folder ())
    paramert_list= ['oil', 'water', 'gas', 'water_injection', 'bhp', 'thp', 'wefac']


    frame = olr.df_from_histtab(paramert_list=paramert_list, start='01.01.2010', **keyword)
    frame.reset_index(inplace=True)
    print(frame.head())
    smooth_frame = olr.histor_smoothing(frame, gas=True)
    #dca_param = olr.decline_fit(smooth_frame, start_year='2010')


    names = df.loc[(df.status == 'prod') & (df['date'] > '2010'), 'well'].unique()
    #predict = pd.DataFrame(columns=['well', 'date', 'SOIL', 'QOIL', 'Time_x', 'Time_y', 'rate', 'month_prod'])
    to_table = pd.DataFrame(columns=['well', 'first_date', 'qi', 'Di', 'bi', 'Dterm'])
    for name, fr in smooth_frame.groupby('well'):
    	dca_param = olr.decline_fit(fr)
    	# predict = pd.concat([predict, well_predict], ignore_index=True)
    	to_table = pd.concat([to_table, dca_param], ignore_index=True)



    smooth_frame.to_csv(f'smoooth_wells_{user}_{date}.csv')
    print(os.getcwd())
    end_wf_item (index = 3)



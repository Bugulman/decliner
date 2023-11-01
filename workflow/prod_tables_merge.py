#  Этот файл был сгенерирован тНавигатор v23.2-3636-gbbb9c73.
#  Copyright (C) Рок Флоу Динамикс 2005-2023.
#  Все права защищены.

# This file is MACHINE GENERATED! Do not edit.

#api_version=v0.0.94a

from __main__.tnav.workflow import *
from tnav_debug_utilities import *
from datetime import datetime, timedelta


declare_workflow (workflow_name="prod_tables_merge",
      variables=[])


prod_tables_merge_variables = {

}

def prod_tables_merge (variables = prod_tables_merge_variables):
    pass
    check_launch_method ()


    begin_user_imports ()
    import getpass
    import os
    import oily_report as olr
    from datetime import datetime
    import pandas as pd
    from pathlib import Path
    end_user_imports ()

    begin_wf_item (index = 1, name = "Сшивка таблиц")
    workflow_folder ()
    if True:
        pass



        begin_wf_item (index = 2)
        prod = pd.DataFrame()
        set_var_type (n = "prod", t = "PY_EXPR", it = "PY_EXPR", val = prod)
        press = pd.DataFrame()
        set_var_type (n = "press", t = "PY_EXPR", it = "PY_EXPR", val = press)

        end_wf_item (index = 2)


        if False:
            begin_wf_item (index = 3)
            wells_production_table_calculate_wef_by_operation_time (table=find_object (name="hist",
                  type="gt_wells_production_data"))
            end_wf_item (index = 3)


        begin_wf_item (index = 4, is_custom_code = True, name = "Функции")
        def df_from_histtab(paramert_list: list, start='01.01.1950', **kwarg):
            df = []
            coll_name = ['well', 'date']+paramert_list
            start_date = datetime.strptime(start, '%d.%m.%Y')
            for w in kwarg['wells']:
                print(w.name)
                for t in kwarg['mod'].get_records(well=w):
                    if t.get_date().date() >= start_date.date():
                        row = []
                        row.append(w.name)
                        row.append(t.get_date().date())
                        row = row+[t.get_value(type=parametr)
                                   for parametr in paramert_list]
                        df.append(row)
                    else:
                        continue
            print(coll_name)
            result = pd.DataFrame(df, columns=coll_name)
            result.set_index('date', inplace=True)
            result.sort_values(by=['well', 'date'], ascending=True, inplace=True)
            return result

        def dataframe_creater(*args, start='01.01.1950', **kwarg):
            indicators = [x for x in args]
            name = ['Parametr{}'.format(x) for x in range(0, len(indicators))]
            indicators_dict = dict.fromkeys(['date', 'well']+name)
            indicators_dict = {x: [] for x in indicators_dict.keys()}
            assos_dict = {x: y for x, y in zip(indicators, name)}
            start_date = datetime.strptime(start, '%d.%m.%Y')
            try:
                for m in kwarg['mod']:
                    for w in kwarg['wells']:
                        for t in kwarg['step']:
                            if t.to_datetime() >= start_date:
                                indicators_dict['date'].append(t.to_datetime())
                                indicators_dict['well'].append(w.name)
                                for i in indicators:
                                    indicators_dict[assos_dict[i]].append(
                                        i[m, w, t].to_list()[0])
                            else:
                                continue
            except Exception as e:
                m = kwarg['mod']
                for w in kwarg['wells']:
                    for t in kwarg['step']:
                        if t.to_datetime() >= start_date:
                            indicators_dict['date'].append(t.to_datetime())
                            indicators_dict['well'].append(w.name)
                            for i in indicators:
                                indicators_dict[assos_dict[i]].append(
                                    i[m, w, t].to_list()[0])
                        else:
                            continue
            result = pd.DataFrame(indicators_dict, index=indicators_dict['date'])
            return result.drop('date', axis=1)



        def adapt_report_frame(frame, **kwarg):
            frame.columns = ['well', 'wlpt', 'wlpth', 'wopt', 'wopth']
            well_cum = frame.loc[frame.index == frame.index.max()]
            well_cum['lik_diff'] = (
                well_cum['wlpth']-well_cum['wlpt'])/well_cum['wlpth']*100
            well_cum['oil_diff'] = (
                well_cum['wopth']-well_cum['wopt'])/well_cum['wopth']*100
            well_cum['oil'] = pd.cut(
                well_cum['oil_diff'], [-1000, -20, 20.5, 1000], labels=['to_mach', 'good', 'poor'])
            well_cum['lik'] = pd.cut(
                well_cum['lik_diff'], [-1000, -20, 20.5, 1000], labels=['to_mach', 'good', 'poor'])
            final = {}
            final['user'] = getpass.getuser()
            final['model'] = [i.name for i in kwarg['mod']][0]
            final['date'] = datetime.now()
            final['total_wells'] = well_cum.loc[well_cum['wopth']
                                                > 0, 'well'].unique().shape[0]
            final['total_oil'] = well_cum['wopt'].sum()/well_cum['wopth'].sum()*100
            final['total_liq'] = well_cum['wlpt'].sum()/well_cum['wlpth'].sum()*100
            final['oil_adapt'] = well_cum.loc[well_cum['oil'] ==
                                              'good', 'wopth'].sum()/well_cum['wopth'].sum()*100
            final['liq_adapt'] = well_cum['lik'].value_counts(normalize=True)[1]*100
            final['wells_adapt'] = well_cum['oil'].value_counts(normalize=True)[1]*100
            return pd.DataFrame(final, index=[1])


        def create_report_dir(path):
            path = Path(path)
            path = path.joinpath('reports')
            path.mkdir(parents=True, exist_ok=True)
            os.chdir(path)


        def interpolate_press_by_sipy(frame, a=2, b=0.1):
            b, a = signal.butter(a, b)
            if frame.shape[0] > 12:
                frame.index = frame['date']
                frame['SBHPH'] = signal.filtfilt(
                    b, a, frame['BHPH'].interpolate(method='time').fillna(method='bfill'))
                frame['STHPH'] = signal.filtfilt(
                    b, a, frame['THPH'].interpolate(method='time').fillna(method='bfill'))
                frame.loc[frame['BHPH'].interpolate(
                    method='time').isnull(), 'SBHPH'] = np.NaN
                frame.loc[frame['THPH'].interpolate(
                    method='time').isnull(), 'STHPH'] = np.NaN
                frame.loc[(frame['status'] == 'not_work'), 'SBHPH'] = np.NaN
                frame.reset_index(drop=True, inplace=True)
            else:
                frame['SBHPH'] = np.NaN
                frame['STHPH'] = np.NaN
            return frame


        def interpolate_prod_by_sipy(frame, a=2, b=0.2, gas=False):
            b, a = signal.butter(a, b)
            if frame.shape[0] > 12 and gas == False:
                frame.index = frame['date']
                frame['SQLIQ'] = signal.filtfilt(
                    b, a, frame['QLIQ'].interpolate(method='time').fillna(method='bfill'))
                frame.loc[(frame['status'] == 'not_work'), 'SQLIQ'] = 0
                frame.loc[(frame['status'] == 'inj'), 'SQLIQ'] = 0
                frame.loc[(frame['SQLIQ'] < 0), 'SQLIQ'] = 0
                frame['SWCT'] = signal.filtfilt(
                    b, a, frame['WCT'].interpolate(method='time').fillna(method='bfill'))
                frame.loc[(frame['status'] == 'not_work'), 'SWCT'] = 0
                frame.loc[(frame['status'] == 'inj'), 'SWCT'] = 0
                frame.loc[(frame['SWCT'] < 0), 'SWCT'] = 0
                frame.reset_index(drop=True, inplace=True)
            elif frame.shape[0] > 12 and gas == True:
                frame.index = frame['date']
                frame['SQLIQ'] = signal.filtfilt(
                    b, a, frame['QLIQ'].interpolate(method='time').fillna(method='bfill'))
                frame.loc[(frame['status'] == 'not_work'), 'SQLIQ'] = 0
                frame.loc[(frame['status'] == 'inj'), 'SQLIQ'] = 0
                frame.loc[(frame['SQLIQ'] < 0), 'SQLIQ'] = 0
                frame['SWCT'] = signal.filtfilt(
                    b, a, frame['WCT'].interpolate(method='time').fillna(method='bfill'))
                frame['SGOR'] = signal.filtfilt(
                    b, a, frame['GOR'].interpolate(method='time').fillna(method='bfill'))
                frame.loc[(frame['status'] == 'not_work'), ['SWCT', 'SGOR']] = 0
                frame.loc[(frame['status'] == 'inj'), ['SWCT', 'SGOR']] = 0
                frame.loc[(frame['SWCT'] < 0), 'SWCT'] = 0
            else:
                frame['SQLIQ'] = np.NaN
                frame['SWCT'] = np.NaN
                frame['SGOR'] = np.NaN
            return frame


        def prod_smooth(frame, a=15, b=0.1):
            b, a = signal.butter(a, b)
            if frame.shape[0] > 12:
                frame.index = frame['date']
                frame.loc[(frame['SPROD'] < 0), 'SPROD'] = np.NaN
                frame.loc[(frame['SPROD'] > frame['SPROD'].quantile(0.8)),
                          'SPROD'] = np.NaN
                frame.loc[(frame['SPROD'] < frame['SPROD'].quantile(0.2)),
                          'SPROD'] = np.NaN
                frame['SPROD'] = signal.filtfilt(
                    b, a, frame['SPROD'].interpolate(method='time').fillna(method='bfill'))
                frame.loc[(frame['status'] == 'not_work'), 'SPROD'] = 0
                frame.loc[(frame['status'] == 'inj'), 'SPROD'] = 0
                temp = frame['SPROD'].groupby(frame.index.year).agg('median')
                temp.name = 'PROD_AV'
                frame = pd.merge(frame, temp, left_on=frame.index.year,
                                 right_on=temp.index)
                frame.reset_index(drop=True, inplace=True)
            else:
                frame['SPROD'] = np.NaN
            return frame


        def histor_smoothing(df, gas=False):
            df.date=pd.to_datetime(df.date)
            if gas == False:
                df.columns = ['date', 'well', 'QOIL', 'QWAT',
                              'QWIN', 'BHPH', 'THPH']
            else:
                df.columns = ['date', 'well', 'QOIL', 'QWAT', 'QGAS',
                              'QWIN', 'BHPH', 'THPH']
                df['GOR'] = df['QGAS']/df['QOIL']

            df['QLIQ'] = df['QOIL']+df['QWAT']
            df['WCT'] = (df['QLIQ']-df['QOIL'])/df['QLIQ']
            df['status'] = 'prod'
            df.loc[df['QWIN'] > 0, 'status'] = 'inj'
            df.loc[((df['QWIN'] == 0) & (df['QLIQ'] == 0)), 'status'] = 'not_work'
            df['THPH'] = df['THPH'].replace([-999, 0], np.nan)
            df['BHPH'] = df['BHPH'].replace([-999, 0], np.nan)
            df.loc[((df['BHPH'] > df['THPH']) & (df['status'] == 'prod')), 'THPH'] = np.NaN
            df = pd.DataFrame(df.groupby(by='well').apply(interpolate_press_by_sipy))
            df.reset_index(drop=True, inplace=True)
            if gas == False:
                df = pd.DataFrame(df.groupby(by='well').apply(
                    interpolate_prod_by_sipy))
            else:
                df = pd.DataFrame(df.groupby(by='well').apply(
                    interpolate_prod_by_sipy, gas=True))
            df.reset_index(drop=True, inplace=True)
            df['SOIL'] = df['SQLIQ']*(1-df['SWCT'])
            if gas == True:
                df['SQGAS'] = df['SOIL']*df['SGOR']
            else:
                pass
            df['SPROD'] = df['SQLIQ']/(df['STHPH']-df['SBHPH'])
            df['PROD'] = df['QLIQ']/(df['THPH']-df['BHPH'])
            df.loc[df['QLIQ'].isnull(), 'SPROD'] = np.NaN
            df['SPROD'] = df['SQLIQ']/(df['STHPH']-df['SBHPH'])
            df['PROD'] = df['QLIQ']/(df['THPH']-df['BHPH'])
            # TODO: разобраться с работой данного функционала. Вылетают ошибки, но не на самом удачном примере
            # df = pd.DataFrame(df.groupby(by='well').apply(prod_smooth))
            # df.reset_index(drop=True, inplace=True)
            df.loc[df['QLIQ'].isnull(), 'SPROD'] = np.NaN
            # df['SBHPH'] = df['STHPH']-(df['SQLIQ']/df['PROD_AV'])
            df.loc[(df['SBHPH'] <= 0), 'SBHPH'] = np.NaN
            df['SBHPH'].fillna(method='bfill')
            return df


        def model_frame(**kwarg):
            df = dataframe_creater(
                woprh, wwprh, wwirh, wbhph, wthph, wlpr, wbhp, wbp9, start='01.01.1955', **kwarg)
            df = df.reset_index()
            df.columns = ['date', 'well', 'QOIL', 'QWAT',
                          'QWIN', 'BHPH', 'THPH', 'MQLIQ', 'MBHP', 'MPRES']
            return df


        # FAQ: Тут включаются функции с анализом падения добычи

        def declane_fit(frame, start_year:str):
            frame = frame.loc[
                (frame["date"] > "2010") & (frame.status == "prod"),
                ["well", "date", "SOIL", "QOIL"],
            ]
            name = frame["well"].unique()
            frame["Time"] = frame["date"] - frame["date"].min()
            frame["Time"] = frame["Time"] / np.timedelta64(1, "D")
            shift = frame.loc[frame["QOIL"] == frame["QOIL"].max(), "Time"]
            shift = int(shift.head(1).values)
            frame["Time"] = frame["Time"] - shift
            sub = frame.copy()
            sub = sub[sub["Time"] >= 0]
            frame["Time"] = frame["Time"] + shift
            last_deb = float(frame["QOIL"].tail(1))
            try:
                qi, di, b, RMSE = dca.arps_fit(
                    sub["Time"].values, sub["SOIL"].values, plot=False
                )
            except ValueError:
                print(f"Ошибка определения темпа для скважины {name}")
                qi, di, b, RMSE = [last_deb, 0.2, 0.2, 0.99]
            except RuntimeError:
                print(f"Ошибка определения темпа для скважины {name}")
                qi, di, b, RMSE = [last_deb, 0.2, 0.2, 0.99]
            logging.info(
                f"Скважина {name[0]},начало прогноза-{sub.date.min()}, \
                        qi-{round(qi,2)} Di-{round(di,2)}, {b}"
            )

            pivot_info = {"well": name[0], "first_date": sub.date.min(), "qi": qi}
            # pivot_info = {'well':name[0],'first_date':sub.date.min(),
            # 'qi':round(qi[0],2), 'Di':round(qi[1],2), 'bi':round(qi[2],2), 'Dterm':round(qi[3], 2)}
            pivot_info = pd.DataFrame([pivot_info])
            return pivot_info



        end_wf_item (index = 4)


        begin_wf_item (index = 5, is_custom_code = True, name = "Парсим таблицы добычи и давления")

        keyword = {'wells': get_all_wells (),
        #           'wells': get_well_filter_by_name (name='target').get_wells (),
                   'mod': get_wells_production_table_by_name (name='UNGKM_prod_from_VAR'),
                   'step': get_all_timesteps()}

        paramert_list= ['oil', 'water', 'gas', 'thp', 'wefac']

        prod = df_from_histtab(paramert_list=paramert_list, start='01.01.1950', **keyword)
        prod.reset_index(inplace=True)


        keyword = {'wells': get_all_wells (),
        #           'wells': get_well_filter_by_name (name='target').get_wells (),
                   'mod': get_wells_production_table_by_name (name='Month_press'),
                   'step': get_all_timesteps()}


        paramert_list= ['bhp']

        press = df_from_histtab(paramert_list=paramert_list, start='01.01.1950', **keyword)
        press.reset_index(inplace=True)
        end_wf_item (index = 5)


        begin_wf_item (index = 6, is_custom_code = True, name = "Сшиваем таблицы по")
        create_report_dir(get_project_folder ())
        res = pd.merge(prod, press, left_on=['well', 'date'], right_on=['well', 'date'])
        res.thp = res.thp*10
        res.to_csv('press_prod.csv')
        end_wf_item (index = 6)


        if False:
            begin_wf_item (index = 7)
            table_import (splitter=True,
                  file_names=["reports/press_prod.csv"],
                  splitter2=True,
                  delimiter="comma",
                  import_header=False)
            end_wf_item (index = 7)


        begin_wf_item (index = 8)
        wells_history_import_simple_table_format (wells=find_object (name="Wells",
              type="gt_wells_entity"),
              well_searcher="name",
              well_production=find_object (name="merged_table",
              type="gt_wells_production_data"),
              reload_all=False,
              splitter=True,
              file_names=["reports/press_prod.csv"],
              tabulator=TableFormat (separator="comma",
              comment="",
              skip_lines=1,
              columns=["skip", "Date", "Well", "Oil Rate", "Water Rate", "Gas rate", "Tubing Head Pressure", "WEF", "Bottom Hole Pressure"]),
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
        end_wf_item (index = 8)



    end_wf_item (index = 1)



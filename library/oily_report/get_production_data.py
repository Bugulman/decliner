import getpass
import logging
from datetime import datetime
import numpy as np
import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    filename=r"d:\work\python\decliner\py_log.log",
    filemode="w",
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def graph_name(name):
    """Get graph name"""
    return [k for k, v in globals().items() if v is name][0]


def data_from_model(*args, **kwarg):
    """Функция создает датафрейм из произольного набора векторов
    arg - названия требуемых для выгрузки векторов
    kwarg - словарь для передачи функций и генераторов из навигатора в функцию. См. readme к библиотеке
    """
    m = kwarg["mod"]
    wells = [w.name for w in kwarg["wells"]]
    groups = [w.group for w in kwarg["wells"]]
    steps = [t.to_datetime() for t in kwarg["step"]]
    df = pd.DataFrame(getpass.getuser(), index=[wells, groups], columns=steps)
    df = df.melt(ignore_index=False).reset_index()
    df.columns = ["well", "group", "date", "user"]
    graph_names = list(map(graph_name, args))
    for arg in zip(args, graph_names):
        df[arg[1]] = np.array(arg[0][m]).flatten("F")
    return df


def dataframe_creater(*args, start="01.01.1950", **kwarg):
    """создает pandas Dataframe с данными из модели.
    Принимает неограниченное количество параметров для
     импорта, позволяет осуществлять импорт как по скважинам
     так и по группам заданием kwarg
    function for converting navigation format to pandas dataframe
    *args - list of arguments to issue in the frame
        dimens - well, here is one of two:
                   well - for issuing a frame for wells
                   group - for issuing by group"""
    indicators = [x for x in args]
    name = ["Parametr{}".format(x) for x in range(0, len(indicators))]
    indicators_dict = dict.fromkeys(["date", "well"] + name)
    indicators_dict = {x: [] for x in indicators_dict.keys()}
    assos_dict = {x: y for x, y in zip(indicators, name)}
    start_date = datetime.strptime(start, "%d.%m.%Y")
    try:
        for m in kwarg["mod"]:
            for w in kwarg["wells"]:
                for t in kwarg["step"]:
                    if t.to_datetime() >= start_date:
                        indicators_dict["date"].append(t.to_datetime())
                        indicators_dict["well"].append(w.name)
                        for i in indicators:
                            indicators_dict[assos_dict[i]].append(
                                i[m, w, t].to_list()[0]
                            )
                    else:
                        continue
    except Exception as e:
        m = kwarg["mod"]
        for w in kwarg["wells"]:
            for t in kwarg["step"]:
                if t.to_datetime() >= start_date:
                    indicators_dict["date"].append(t.to_datetime())
                    indicators_dict["well"].append(w.name)
                    for i in indicators:
                        indicators_dict[assos_dict[i]].append(i[m, w, t].to_list()[0])
                else:
                    continue
    result = pd.DataFrame(indicators_dict, index=indicators_dict["date"])
    return result.drop("date", axis=1)


def df_from_histtab(paramert_list: list, start="01.01.1950", **kwarg):
    """создает pandas Dataframe с данными из таблицы с историей в дизайнере модели.
    paramert_list - параметры для выгрузки, полный список можно получить через get_production_types
    keyword = {'wells': get_well_filter_by_name (name='14').get_wells (), требуемый список скважин
           'mod': get_all_wells_production_tables ()[0], таблица с данными по исптории
           'step': get_all_timesteps()}
    """

    from datetime import datetime

    import pandas as pd

    df = []
    coll_name = ["well", "date"] + paramert_list
    start_date = datetime.strptime(start, "%d.%m.%Y")
    for w in kwarg["wells"]:
        print(w.name)
        for t in kwarg["mod"].get_records(well=w):
            if t.get_date().date() >= start_date.date():
                row = []
                row.append(w.name)
                row.append(t.get_date().date())
                row = row + [t.get_value(type=parametr) for parametr in paramert_list]
                df.append(row)
            else:
                continue
    result = pd.DataFrame(df, columns=coll_name)
    result.set_index("date", inplace=True)
    result.sort_values(by=["well", "date"], ascending=True, inplace=True)
    result.fillna(0, inplace=True)
    return result

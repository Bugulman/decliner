# Automaticaly recalculate=false
# Single model=false
import datetime
import os
from datetime import datetime

import numpy as np
import pandas as pd
from scipy import signal

keyword = {
    "wells": get_wells_from_filter("Фильтр по скважинам 1"),
    "mod": get_all_models(),
    "step": get_all_timesteps(),
}

# создает pandas Dataframe с данными из модели. Принимает неограниченное количество параметров для
# импорта, позволяет осуществлять импорт как по скважинам так и по группам заданием kwarg


def dataframe_creater(*args, start="01.01.1950", **kwarg):
    """Function for converting navigation format to pandas dataframe
    *args - list of arguments to issue in the frame
        dimens - well, here is one of two:
                   well - for issuing a frame for wells
                   group - for issuing by group"""
    indicators = [x for x in args]
    name = ["Parametr{}".format(x) for x in range(0, len(indicators))]
    indicators_dict = dict.fromkeys(["date", "well"] + name)
    indicators_dict = {x: [] for x in indicators_dict.keys()}
    assos_dict = {x: y for x, y in zip(indicators, name)}
    start_date = datetime.datetime.strptime(start, "%d.%m.%Y")
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
    except Exception:
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


# функция сглаживает давление по DataFrame. Коэффициенты a и b для настройки.
# Чем выше a и ниже b тем сильнее сглаживание.
def interpolate_press_by_sipy(frame, a=15, b=0.1):
    b, a = signal.butter(a, b)
    _b, _a = signal.butter(5, 0.5)
    if frame.shape[0] > 12:
        frame.index = frame["date"]
        frame["SBHPH"] = signal.filtfilt(
            _b, _a, frame["BHPH"].interpolate(method="time").fillna(method="bfill")
        )
        frame.loc[
            ((frame["SBHPH"] > frame["THPH"]) & (frame["status"] == "prod")), "THPH"
        ] = np.NaN
        frame["STHPH"] = signal.filtfilt(
            b, a, frame["THPH"].interpolate(method="time").fillna(method="bfill")
        )
        frame.loc[frame["BHPH"].interpolate(method="time").isnull(), "SBHPH"] = np.NaN
        frame.loc[frame["THPH"].interpolate(method="time").isnull(), "STHPH"] = np.NaN
        frame.loc[(frame["status"] == "not_work"), "SBHPH"] = np.NaN
        frame.reset_index(drop=True, inplace=True)
    else:
        frame["SBHPH"] = np.NaN
        frame["STHPH"] = np.NaN
    return frame


# функция сглаживает добычу по DataFrame. Коэффициенты a и b для настройки.
# Чем выше a и ниже b тем сильнее сглаживание.
def prod_smooth(frame, a=5, b=0.1):
    b, a = signal.butter(a, b)
    if frame.shape[0] > 12:
        frame.index = frame["date"]
        frame.loc[(frame["SPROD"] < 0), "SPROD"] = np.NaN
        frame.loc[(frame["SPROD"] > frame["SPROD"].quantile(0.8)), "SPROD"] = np.NaN
        frame.loc[(frame["SPROD"] < frame["SPROD"].quantile(0.2)), "SPROD"] = np.NaN
        frame["SPROD"] = signal.filtfilt(
            b, a, frame["SPROD"].interpolate(method="time").fillna(method="bfill")
        )
        frame.loc[(frame["status"] == "not_work"), "SPROD"] = 0
        frame.loc[(frame["status"] == "inj"), "SPROD"] = 0
        temp = frame["SPROD"].groupby(frame.index.year).agg("median")
        temp.name = "PROD_AV"
        frame = pd.merge(frame, temp, left_on=frame.index.year, right_on=temp.index)
        frame.reset_index(drop=True, inplace=True)
    else:
        frame["SPROD"] = np.NaN
    return frame


# функция сглаживает добычу по DataFrame. Коэффициенты a и b для настройки.
# Чем выше a и ниже b тем сильнее сглаживание.
def interpolate_prod_by_sipy(frame, a=3, b=0.1):
    b, a = signal.butter(a, b)
    if frame.shape[0] > 12:
        frame.index = frame["date"]
        frame["SQLIQ"] = signal.filtfilt(
            b, a, frame["QLIQ"].interpolate(method="time").fillna(method="bfill")
        )
        frame.loc[(frame["status"] == "not_work"), "SQLIQ"] = 0
        frame.loc[(frame["status"] == "inj"), "SQLIQ"] = 0
        frame["SWCT"] = signal.filtfilt(
            b, a, frame["WCT"].interpolate(method="time").fillna(method="bfill")
        )
        frame.loc[(frame["status"] == "not_work"), "SWCT"] = 0
        frame.loc[(frame["status"] == "inj"), "SWCT"] = 0
        frame.reset_index(drop=True, inplace=True)
    else:
        frame["SQLIQ"] = np.NaN
        frame["SWCT"] = np.NaN
    return frame


# основная функция скрипта, преобразовывающая данные из модели.
# Выполняет выгрузку в датафрейм, предобработку данных и применение функций сглаживания


def histor_smoothing(**kwarg):
    """Relives and smoothes pressure in source data
    :kwarg: navigator API keyword = {'grou':get_all_groups(),
                                                                    'wells':get_all_wells(),
                                                                    'mod': get_all_models(),
                                                                    'step':get_all_timesteps()}
    :returns: pandas DataFrame with smoothing press
    """
    df = dataframe_creater(
        woprh,
        wwprh,
        wwirh,
        wbhph,
        wthph,
        wlpr,
        wbhp,
        wbp9,
        wstart="01.01.1955",
        **kwarg,
    )
    df = df.reset_index()
    df.columns = [
        "date",
        "well",
        "QOIL",
        "QWAT",
        "QWIN",
        "BHPH",
        "THPH",
        "MQLIQ",
        "MBHP",
        "MPRES",
    ]
    df["QLIQ"] = df["QOIL"] + df["QWAT"]
    df["WCT"] = (df["QLIQ"] - df["QOIL"]) / df["QLIQ"]
    df["status"] = "prod"
    df.loc[df["QWIN"] > 0, "status"] = "inj"
    df.loc[((df["QWIN"] == 0) & (df["QLIQ"] == 0)), "status"] = "not_work"
    df["THPH"] = df["THPH"].replace([-999, 0], np.nan)
    df["BHPH"] = df["BHPH"].replace([-999, 0], np.nan)
    df.loc[((df["BHPH"] > df["THPH"]) & (df["status"] == "prod")), "THPH"] = np.NaN
    df = pd.DataFrame(df.groupby(by="well").apply(interpolate_press_by_sipy))
    df.reset_index(drop=True, inplace=True)
    df = pd.DataFrame(df.groupby(by="well").apply(interpolate_prod_by_sipy))
    df.reset_index(drop=True, inplace=True)
    df["SOIL"] = df["SQLIQ"] * (1 - df["SWCT"])
    df["SPROD"] = df["SQLIQ"] / (df["STHPH"] - df["SBHPH"])
    df["PROD"] = df["QLIQ"] / (df["THPH"] - df["BHPH"])
    df.loc[df["QLIQ"].isnull(), "SPROD"] = np.NaN
    df["SPROD"] = df["SQLIQ"] / (df["STHPH"] - df["SBHPH"])
    df["PROD"] = df["QLIQ"] / (df["THPH"] - df["BHPH"])
    df = pd.DataFrame(df.groupby(by="well").apply(prod_smooth))
    df.reset_index(drop=True, inplace=True)
    df["MPROD"] = df["MQLIQ"] / (df["MPRES"] - df["MBHP"])
    df.loc[df["QLIQ"].isnull(), "SPROD"] = np.NaN
    df["SBHPH"] = df["STHPH"] - (df["SQLIQ"] / df["PROD_AV"])
    df.loc[(df["SBHPH"] <= 0), "SBHPH"] = np.NaN
    df["SBHPH"].fillna(method="bfill")
    df["Pres_dif"] = (df["THPH"] - df["MPRES"]) ** 2
    df["Pres_dif"] = df["Pres_dif"].cumsum()
    return df


# создание папки reports в рабочем каталоге модели


def create_report_dir(path):
    """Creates a result folder and sets it by default when writing files
    path = r let to the model's sensor"""
    if os.path.exists((path + r"\\reports")):
        os.chdir(path + r"\\reports")
    else:
        os.chdir(path)
        os.mkdir("reports")
        os.chdir(path + r"\\reports")


def main():
    print("lets go")
    create_report_dir(path=get_project_folder())
    frame = histor_smoothing(**keyword)
    # импорт сглаженных данных в навигатор
    bhp = graph(type="well", default_value=0)
    thp = graph(type="well", default_value=0)
    liq = graph(type="well", default_value=0)
    oil = graph(type="well", default_value=0)
    wct = graph(type="well", default_value=0)
    sprod = graph(type="well", default_value=0)
    prod = graph(type="well", default_value=0)
    mprod = graph(type="well", default_value=0)
    press_diff = graph(type="well", default_value=0)
    for index, rows in frame.iterrows():
        w = get_well_by_name(rows["well"])
        t = get_timestep_from_datetime(
            pd.to_datetime(rows["date"]).date(), mode="nearest"
        )
        zab = float(rows["SBHPH"])
        plast = float(rows["STHPH"])
        w_liq = float(rows["SQLIQ"])
        w_oil = float(rows["SOIL"])
        w_wct = float(rows["SWCT"])
        w_sp = float(rows["PROD_AV"])
        w_p = float(rows["PROD"])
        m_p = float(rows["MPROD"])
        p_diff = float(rows["Pres_dif"])
        bhp[w, t] = zab
        thp[w, t] = plast
        liq[w, t] = w_liq
        oil[w, t] = w_oil
        wct[w, t] = w_wct
        sprod[w, t] = w_sp
        prod[w, t] = w_p
        mprod[w, t] = m_p
        press_diff[w, t] = p_diff
    export(bhp, name="SBHP", units="pressure")
    export(thp, name="STHP", units="pressure")
    export(liq, name="SLIQ", units="liquid_surface_rate")
    export(oil, name="SOIL", units="liquid_surface_rate")
    export(wct, name="SWCT", units="no")
    export(sprod, name="SPROD", units="no")
    export(prod, name="PROD", units="no")
    export(mprod, name="Model_PROD", units="no")
    export(press_diff, name="Pressure diff", units="no")
    # frame['well']=frame['well'].apply(lambda x: transliterate.translit(x, 'ru'))
    frame.to_csv("productiviti.csv")


main()

import getpass
import logging
from datetime import datetime
import numpy as np
import pandas as pd
from scipy import signal

logging.basicConfig(
    level=logging.INFO,
    filename=r"d:\work\python\decliner\py_log.log",
    filemode="w",
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def interpolate_press_by_sipy(frame, a=2, b=0.1):
    """функция сглаживает давление по DataFrame. Коэффициенты a и b для настройки.
    Чем выше a и ниже b тем сильнее сглаживание.
    """
    b, a = signal.butter(a, b)
    if frame.shape[0] > 12:
        frame.index = frame["date"]
        frame["SBHPH"] = signal.filtfilt(
            b, a, frame["BHPH"].interpolate(method="time").fillna(method="bfill")
        )
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


def interpolate_prod_by_sipy(frame, a=2, b=0.2, gas=False):
    """функция сглаживает добычу по DataFrame. Коэффициенты a и b для настройки.
    Чем выше a и ниже b тем сильнее сглаживание.
    """
    b, a = signal.butter(a, b)
    if frame.shape[0] > 12 and gas == False:
        frame.index = frame["date"]
        frame["SQLIQ"] = signal.filtfilt(
            b, a, frame["QLIQ"].interpolate(method="time").fillna(method="bfill")
        )
        frame.loc[(frame["status"] == "not_work"), "SQLIQ"] = 0
        frame.loc[(frame["status"] == "inj"), "SQLIQ"] = 0
        frame.loc[(frame["SQLIQ"] < 0), "SQLIQ"] = 0
        frame["SWCT"] = signal.filtfilt(
            b, a, frame["WCT"].interpolate(method="time").fillna(method="bfill")
        )
        frame.loc[(frame["status"] == "not_work"), "SWCT"] = 0
        frame.loc[(frame["status"] == "inj"), "SWCT"] = 0
        frame.loc[(frame["SWCT"] < 0), "SWCT"] = 0
        frame.reset_index(drop=True, inplace=True)
    elif frame.shape[0] > 12 and gas == True:
        frame.index = frame["date"]
        frame["SQLIQ"] = signal.filtfilt(
            b, a, frame["QLIQ"].interpolate(method="time").fillna(method="bfill")
        )
        frame["SGAS"] = signal.filtfilt(
            b, a, frame["QGAS"].interpolate(method="time").fillna(method="bfill")
        )
        frame.loc[(frame["status"] == "not_work"), ["SGAS", "SQLIQ"]] = 0
        frame.loc[(frame["status"] == "inj"), ["SGAS", "SQLIQ"]] = 0
        frame.loc[(frame["SQLIQ"] < 0), "SQLIQ"] = 0
        frame["SWCT"] = signal.filtfilt(
            b, a, frame["WCT"].interpolate(method="time").fillna(method="bfill")
        )
        # frame['SGOR'] = signal.filtfilt(
        # b, a, frame['GOR'].interpolate(method='time').fillna(method='bfill'))
        # TODO: сглаживание газового фактора тут убрал пока что
        frame.loc[(frame["status"] == "not_work"), ["SWCT"]] = 0
        frame.loc[(frame["status"] == "inj"), ["SWCT"]] = 0
        frame.loc[(frame["SWCT"] < 0), "SWCT"] = 0
    else:
        frame["SQLIQ"] = np.NaN
        frame["SWCT"] = np.NaN
        frame["SGOR"] = np.NaN
    return frame


def prod_smooth(frame, a=15, b=0.1):
    """функция сглаживает продуктивность по DataFrame.
    Чем выше a и ниже b тем сильнее сглаживание.
    """
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


def histor_smoothing(df, gas=False):
    """Relives and smoothes pressure in source data
    :df:panda DataFrame with well production data. Should contain well|data|oil_rate|water_rate|
    gas_rate(optional)|water_injection|bottemhole_pressure|pres_meash
    :returns: pandas DataFrame with smoothing press
    """
    df.date = pd.to_datetime(df.date)
    # logging.info(f'GAS in {gas} cols {df.columns}, table_info {df.info()}')
    if gas == False:
        df.columns = ["date", "well", "QOIL", "QWAT", "QWIN", "BHPH", "THPH", "WEFA"]
    else:
        df.columns = [
            "date",
            "well",
            "QOIL",
            "QWAT",
            "QGAS",
            "QWIN",
            "BHPH",
            "THPH",
            "WEFA",
        ]
        df["GOR"] = df["QGAS"] / df["QOIL"]

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
    if gas == False:
        df = pd.DataFrame(df.groupby(by="well").apply(interpolate_prod_by_sipy))
    else:
        df = pd.DataFrame(
            df.groupby(by="well").apply(interpolate_prod_by_sipy, gas=True)
        )
    df.reset_index(drop=True, inplace=True)
    df["SOIL"] = df["SQLIQ"] * (1 - df["SWCT"])
    if gas == True:
        df["SQGAS"] = df["SOIL"] * df["SGOR"]
    else:
        pass
    df["SPROD"] = df["SQLIQ"] / (df["STHPH"] - df["SBHPH"])
    df["PROD"] = df["QLIQ"] / (df["THPH"] - df["BHPH"])
    df.loc[df["QLIQ"].isnull(), "SPROD"] = np.NaN
    df["SPROD"] = df["SQLIQ"] / (df["STHPH"] - df["SBHPH"])
    df["PROD"] = df["QLIQ"] / (df["THPH"] - df["BHPH"])
    # TODO: разобраться с работой данного функционала. Вылетают ошибки, но не на самом удачном примере
    # df = pd.DataFrame(df.groupby(by='well').apply(prod_smooth))
    # df.reset_index(drop=True, inplace=True)
    df.loc[df["QLIQ"].isnull(), "SPROD"] = np.NaN
    # df['SBHPH'] = df['STHPH']-(df['SQLIQ']/df['PROD_AV'])
    df.loc[(df["SBHPH"] <= 0), "SBHPH"] = np.NaN
    df["SBHPH"].fillna(method="bfill")
    return df

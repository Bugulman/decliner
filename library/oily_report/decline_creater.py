import pandas as pd
import logging
from utiltools import worked_time


def prod_check(func):
    """Декаратор для проверки датафреймов на наличие добычи"""

    def _prod_check(frame, start_year, *arg, **kwarg):
        filtred_frame = frame.loc[
            (frame["date"] > start_year) & (frame.status == "prod")
        ]
        if (
            filtred_frame.QOIL.max()
            + filtred_frame.QWAT.max()
            + filtred_frame.QGAS.max()
            > 0
        ):
            res = func(frame, start_year, *arg, **kwarg)
            return res
        else:
            print(f"Скважина {frame.well.unique()} без добычи")
            pass

    return _prod_check


@prod_check
def decline_fit(frame, start_year, target_coll="QOIL", to_df=False):
    """Находит максимум добычи на временном интервале и от
    него считает коэффициенты для кривой падения добычи"""
    frame.date = pd.to_datetime(frame.date)
    frame = frame.loc[
        (frame["date"] > start_year) & (frame.status == "prod"),
        ["well", "date", target_coll],
    ]
    name = frame["well"].unique()
    logging.info(f"DCA for well {name}")
    frame = worked_time(frame)
    max_prod = frame.loc[
        frame[target_coll] == frame[target_coll].max(), ["date", "Time"]
    ]
    max_prod_date, max_prod_Time = max_prod.values[0]
    sub = frame.copy()
    sub = sub[sub["date"] >= max_prod_date]
    last_deb = float(frame[target_coll].tail(1))
    try:
        qi, di, b, RMSE = dca.arps_fit(sub["date"], sub[target_coll], plot=False)
    except:
        print(f"Ошибка определения темпа для скважины {name}")
        qi, di, b, RMSE = [last_deb, 0.2, 0.2, 0.99]
    logging.info(
        f"Скважина {name[0]}, начало прогноза-{sub.date.min()}, qi-{qi}, Di-{di}, {b}"
    )
    dca_info = {
        "well": name[0],
        "parametr": target_coll,
        "start_match_data": max_prod_date,
        "start_match_time": max_prod_Time,
        "current_data": frame["date"].max(),
        "current_time": frame["Time"].max(),
        "qi": qi,
        "Di": di,
        "b": b,
        "Accuracy": RMSE,
    }
    return pd.DataFrame([dca_info]) if to_df == True else dca_info


def prod_predict(long=120, **kwarg):
    """Прогноз добычи по параметрам функции decline_fit"""
    delta = kwarg["current_data"].to_period("M") - kwarg["start_match_data"].to_period(
        "M"
    )
    long = delta.n + long
    prog = pd.DataFrame(
        pd.date_range(kwarg["start_match_data"], periods=long, freq="MS")
    )
    prog.columns = ["date"]
    worked_time(prog)
    prog[kwarg["parametr"]] = dca.hyperbolic(
        prog.Time, kwarg["qi"], kwarg["Di"], kwarg["b"]
    )
    prog["well"] = kwarg["well"]
    return prog


#     prog['rate'] = mh.rate(prog.Time)
#     prog['month_prod'] = mh.monthly_vol(prog.Time)
#     # frame=pd.merge(frame, prog, left_on='date', right_on ='date', how='outer')
#     # frame['well'].fillna(method='ffill', inplace=True)
#     return prog['rate']
#

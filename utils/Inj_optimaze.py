# Automaticaly recalculate=true
# Single model=false
# Automaticaly recalculate=true
# Single model=false
# Automaticaly recalculate=true
# Single model=false
# Automaticaly recalculate=true
# Single model=false
# пишите здесь ваш код
from datetime import datetime
import os
import oily_report as olr
import numpy as np

start = "01.01.2020"


# скрипт для формирования файлов расчета по диапазонам приемистостей исходя из исторической информации о приемистости скважин с отбраковкой выбросов
def quantile(nav_vector, q):
    """TODO: Docstring for quantile.
    :returns: TODO

    """
    res = np.quantile(nav_vector, q)
    return float(res)


olr.create_report_dir(get_project_folder())

with open("wconinj.txt", "w") as f:
    f.write("WCONINJ\n")
    start_date = datetime.strptime(start, "%d.%m.%Y")
    last_date = get_all_timesteps()[-1].to_datetime() - start_date
    last_date = last_date.days
    for m in get_all_models():
        for t in get_all_timesteps():
            if t.to_datetime() == start_date:
                for w in get_all_wells():
                    if wwit[m, w].max(dates=get_all_timesteps()[-1]) > 0:
                        avg_wir_for_forecast = (
                            wwit[m, w].max(dates="all") - wwit[m, w, t]
                        ) / last_date
                        avg_bhp_for_forecast = wbhp[m, w].fix(
                            date=get_all_timesteps()[-1]
                        )
                        avg_bhp_for_forecast = float(avg_bhp_for_forecast)
                        avg_wir_for_forecast = float(avg_wir_for_forecast) * 1.8

                        injec_rejums = f"'{w.name}' WATER OPEN BHP {round(avg_wir_for_forecast, 2)} 1* {round(avg_bhp_for_forecast, 1)} /\n"
                        # injec_rejums = f"'{w.name}' WATER OPEN BHP 2* {round(avg_bhp_for_forecast, 1)} /\n"

                        f.writelines(injec_rejums)
                        print(injec_rejums)
    f.writelines("/")  # create rejims

with open("defines.txt", "w") as f:
    f.write("DEFINES\n")
    start_date = datetime.strptime(start, "%d.%m.%Y")
    last_date = get_all_timesteps()[-1].to_datetime() - start_date
    last_date = last_date.days
    for m in get_all_models():
        for t in get_all_timesteps():
            if t.to_datetime() == start_date:
                for w in get_all_wells():
                    if wwit[m, w].max(dates=get_all_timesteps()[-1]) > 0:
                        avg_wir_for_forecast = (
                            wwit[m, w].max(dates="all") - wwit[m, w, t]
                        ) / last_date
                        avg_wir_hist = (
                            wwith[m, w].max(dates="all") - wwith[m, w, t]
                        ) / last_date
                        match_coef = avg_wir_hist / avg_wir_for_forecast
                        last_inj = float(wwir[m, w].fix(date=get_all_timesteps()[-1]))
                        inj_min = np.quantile(np.array(wwir[m, w])[-36:-1], 0.00)
                        if last_inj < inj_min:
                            inj_min = last_inj
                        inj_max = np.quantile(np.array(wwir[m, w])[-36:-1], 0.9)
                        if last_inj > inj_max:
                            inj_max = last_inj
                        last_bhp = float(wbhp[m, w].fix(date=get_all_timesteps()[-1]))
                        if round(inj_max, 0) == 0:
                            continue
                        else:
                            injec_rejums = f"'W_{w.name}' {round(last_inj, 0)} {round(inj_min, 0)} {round(inj_max, 0)} INT/\n"
                            # injec_rejums = f"'{w.name}' WATER OPEN BHP 2* {round(avg_bhp_for_forecast, 1)} /\n"
                            f.writelines(injec_rejums)
                            print(injec_rejums)
    f.writelines("/")


with open("wconinj_defines.txt", "w") as f:
    f.write("WCONINJ\n")
    start_date = datetime.strptime(start, "%d.%m.%Y")
    last_date = get_all_timesteps()[-1].to_datetime() - start_date
    last_date = last_date.days
    for m in get_all_models():
        for t in get_all_timesteps():
            if t.to_datetime() == start_date:
                for w in get_all_wells():
                    if wwit[m, w].max(dates=get_all_timesteps()[-1]) > 0:
                        avg_wir_for_forecast = (
                            wwit[m, w].max(dates="all") - wwit[m, w, t]
                        ) / last_date
                        avg_wir_hist = (
                            wwith[m, w].max(dates="all") - wwith[m, w, t]
                        ) / last_date
                        match_coef = avg_wir_hist / avg_wir_for_forecast
                        last_inj = float(wwir[m, w].fix(date=get_all_timesteps()[-1]))
                        inj_min = np.quantile(np.array(wwir[m, w])[-36:-1], 0.00)
                        if last_inj < inj_min:
                            inj_min = last_inj
                        inj_max = np.quantile(np.array(wwir[m, w])[-36:-1], 0.9)
                        if last_inj > inj_max:
                            inj_max = last_inj
                        avg_bhp_for_forecast = wbhp[m, w].fix(
                            date=get_all_timesteps()[-1]
                        )
                        avg_bhp_for_forecast = float(avg_bhp_for_forecast)
                        if round(inj_max, 0) == 0:
                            continue
                        else:
                            injec_rejums = f"'{w.name}' WATER OPEN BHP @W_{w.name}@  1* {round(avg_bhp_for_forecast, 1)} /\n"
                            f.writelines(injec_rejums)
                            print(injec_rejums)
    f.writelines("/")

# Automaticaly recalculate=true
# Single model=false
# Automaticaly recalculate=true
# Single model=false
import sys

path = [
    "d:\\other\\my_software\\python\\python36.zip",
    "d:\\other\\my_software\\python\\DLLs",
    "d:\\other\\my_software\\python\\lib",
    "d:\\other\\my_software\\python",
    "",
    "C:\\Users\\VafinAR\\AppData\\Roaming\\Python\\Python36\\site-packages",
    "d:\\other\\my_software\\python\\lib\\site-packages",
    "d:\\other\\my_software\\python\\lib\\site-packages\\pip-21.0.1-py3.6.egg",
    "d:\\other\\my_software\\python\\lib\\site-packages\\win32",
    "d:\\other\\my_software\\python\\lib\\site-packages\\win32\\lib",
    "d:\\other\\my_software\\python\\lib\\site-packages\\Pythonwin",
    "d:\\other\\my_software\\python\\lib\\site-packages\\IPython\\extensions",
    "C:\\Users\\VafinAR\\.ipython",
]
for dir in path:
    if dir not in sys.path:
        sys.path.append(dir)

import datetime

# import pandas as pd
# import numpy as np
import h5py
import os


def __init_script__():
    create_graph(name="wells_BHP", type="well", default_value=0)
    create_graph(name="wells_GRP", type="well", default_value=0)


##


hdf5File = os.path.join(get_project_folder(), "reports", "FRACK", "wells_base.hdf5")

hdf5File = os.path.join(
    r"D:\project\Minnib_project\SCHED_PATTERNS", "reports", "FRACK", "wells_base.hdf5"
)


##
def connecter(hdf5File):
    def Hdf5File_connect(func):
        """TODO: Docstring for Hdf5File_connect."""

        def _connection(arg1, **kwarg):
            with h5py.File(hdf5File, "r+") as f:
                try:
                    res = func(f[arg1], **kwarg)
                    return res
                except KeyError:
                    pass
                    # print(f'База не содержит скважину {arg1}')

        return _connection

    return Hdf5File_connect


##


@connecter(hdf5File)
def get_well(name):
    work_list = []
    for plast in name.keys():
        works = schedule_frack(name, plast)
        if works != None:
            work_list.append(works)
        else:
            pass
    return work_list


##


@connecter(hdf5File)
def get_last_frack(name):
    return name.attrs["counter"], name.attrs["last"]


##


@connecter(hdf5File)
def conditions(name, new_date=1990, rewrite=False):
    if rewrite == False:
        name.attrs["counter"] = name.attrs["frack_counter"]
        if new_date - name.attrs["frack_year"] > 3.0:
            name.attrs["last"] = new_date
        else:
            name.attrs["last"] = name.attrs["frack_year"] + 3
    else:
        name.attrs["counter"] = name.attrs["counter"] + 1
        name.attrs["last"] = new_date + 3


def string_from_dataset(dataset, totype=int):
    dataset = dataset[:].astype(totype)
    dataset = [str(i) for i in dataset]
    return " ".join(dataset)


def schedule_frack(wellname, plast):
    """TODO: Docstring for function."""
    if wellname[plast].attrs.get("works") == "frack":
        param = "140 0 120 120 3 3 0.15 '630000.000000' '560.000000' TIME 1 3* 3* / "
        name = wellname.attrs.get("psevdo")
        ijk = string_from_dataset(wellname[plast]["coor"])
        to_model = f"'{name}' {ijk} {param}"
        # elif wellname.attrs.get('works') == perf:
        # to_model = f"{wellname.attrs.get('psevdonim')} 1* {self[plast]['top_bot']}	TVD	OPEN 2* 0.146 1* 0 1* 1 /"
        return to_model
    else:
        pass


def _extra_data():
    """TODO: Docstring for read_wells_frack.
    :file: file with frack param for take list of wellnames
    :returns: list of wellnames
    """
    curr = get_current_date()
    with h5py.File(hdf5File, "r+") as f:
        temp_dict = {}
        for i in f.keys():
            temp_dict[f[i].attrs.get("psevdo")] = i
    for w in get_all_wells():
        conditions(temp_dict.get(w.name, "999"), new_date=curr.year)
    script_off()


##


def frack_in_model(name):
    """TODO: Docstring for frack_in_model."""
    res = get_well(name)
    # print((res))
    if res != None and len(res) > 1:
        for x in res:
            add_keyword(
                """
                WFRACP
                """
                + x
                + """
                /
                """
            )
    elif res != None and len(res) > 0:
        add_keyword(
            """
                WFRACP
                """
            + res[0]
            + """
                /
                """
        )
    else:
        pass


def grp_control(well):
    if wlpr[well] > 0:
        lg = wlpr[well] * 1.5 if wlpr[well] * 1.5 < 25 else wlpr[well] + 20
        set_prod_limit(wells=well, lrat=lg)
        reset_prod_limit(wells=well, bhp=wbhp[well])
    else:
        add_keyword(
            """
                wconinje
                '"""
            + well.name
            + """'   WATER         OPEN   BHP     2*                """
            + str(wbhp[well])
            + """  /
                /
                """
        )


def read_wells_frack():
    """TODO: Docstring for read_wells_frack."""
    curr = get_current_date()
    with h5py.File(hdf5File, "r+") as f:
        temp_dict = {}
        for i in f.keys():
            temp_dict[f[i].attrs.get("psevdo")] = i
    if curr.year == 2034:
        script_off()
    else:
        for w in get_all_wells():
            name = temp_dict.get(w.name, "999")
            # print(w.name, name)
            # print(name, curr.month, curr.year)
            try:
                count, year = get_last_frack(name)
            except TypeError:
                count, year = 999, 3000
            if curr.day == 1 and curr.month == 6 and count <= 3 and curr.year == year:
                print(name, count, year, curr.year, curr.month)
                frack_in_model(name)
                grp_control(w)
                conditions(name, new_date=curr.year, rewrite=True)
            else:
                pass


##
def limited_wells_frack(frack_per_cycle):
    """TODO: Скрипт для проведения ГТМ в зависимости от количества выделенных бригад.
    Расчет исходя из того, что ПЗР к ГРП проводится 14 суток+1 на переезды.
    frack_per_cycle -  количество выделенных бригад для расчета
    """
    frack = 1
    curr = get_current_date()
    with h5py.File(hdf5File, "r+") as f:
        temp_dict = {}
        for i in f.keys():
            temp_dict[f[i].attrs.get("psevdo")] = i
    if curr.year == 2030:
        script_off()
    else:
        for w in get_all_wells():
            name = temp_dict.get(w.name, "999")
            # print(w.name, name)
            # print(name, curr.month, curr.year)
            try:
                count, year = get_last_frack(name)
            except TypeError:
                count, year = 999, 3000
            if count <= 3 and curr.year >= year and frack <= frack_per_cycle:
                print(
                    f"ГРП на скважине {name} в {count} раз на {curr} дату, а должен в {year}"
                )
                frack_in_model(name)
                grp_control(w)
                conditions(name, new_date=curr.year, rewrite=True)
                frack += 1
            else:
                pass
    script_set_options(min_interval=datetime.timedelta(days=15))


import pandas as pd


def frack_in_model(name):
    """TODO: Docstring for frack_in_model."""
    res = get_well(name)
    print(res, len(res))
    if res != None and len(res) > 1:
        for x in res:
            return x
    elif res != None and len(res) > 0:
        return res[0]
    else:
        pass


def well_frack(frack_per_cycle):
    t = pd.date_range(start="01.01.2023", end="01.02.2030", freq="M").tolist()
    with open("out.inc", "w") as r:
        with h5py.File(hdf5File, "r+") as f:
            for i in f.keys():
                # for i in ['20141', '10778']:
                conditions(i, new_date=2022)
            for cur_year in t:
                frack = 1
                for w in f.keys():
                    name = w
                    try:
                        count, year = get_last_frack(name)
                    except TypeError:
                        count, year = 999, 3000
                    if (
                        count <= 3
                        and cur_year.year >= year
                        and frack <= frack_per_cycle
                    ):
                        print(
                            f"ГРП на скважине {name}, дата {cur_year.date()}, {count} раз_{frack_in_model(name)}",
                            file=r,
                        )
                        conditions(name, new_date=cur_year.year, rewrite=True)
                        frack += 1
                    else:
                        pass

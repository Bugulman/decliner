#Automaticaly recalculate=true
#Single model=false
import pickle
import os
import pprint
import h5py
import numpy as np
import pandas as pd
import datetime


def __init_script__():
    create_graph(name="wells_BHP", type="well", default_value=0)
    create_graph(name="wells_GRP", type="well", default_value=0)


hdf5File = os.path.join(get_project_folder(), 'reports',
                        'FRACK', 'wells_base.hdf5')

def connecter(hdf5File):
    def Hdf5File_connect(func):
        """TODO: Docstring for Hdf5File_connect."""
        def _connection(arg1):
            with h5py.File(hdf5File, 'a') as f:
                try:
                    res = func(f[arg1])
                    return res
                except KeyError:
                    print(
                        f'База не содержит скважину {arg1}')
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


def string_from_dataset(dataset, totype=int):
    dataset = dataset[:].astype(totype)
    dataset = [str(i) for i in dataset]
    return " ".join(dataset)


def schedule_frack(wellname, plast):
    """TODO: Docstring for function."""
    if wellname[plast].attrs.get('works') == 'frack':
        param = "140 0 120 120 3 3 0.15 '630000.000000' '560.000000' TIME 1 3* 3* / "
        name = wellname.attrs.get('psevdo')
        ijk = string_from_dataset(wellname[plast]['coor'])
        to_model = f"'{name}' {ijk} {param}"
    # elif wellname.attrs.get('works') == perf:
        # to_model = f"{wellname.attrs.get('psevdonim')} 1* {self[plast]['top_bot']}	TVD	OPEN 2* 0.146 1* 0 1* 1 /"
        return to_model
    else:
        pass
##


def reset_to_bhp():
    """TODO: Docstring for reset_to_bhp.
    :returns: TODO
    """
    for w in get_all_wells():
        if wlpr[w] > 0:
            lg = wlpr[w]
            press = wbhp[w]
            set_prod_limit(wells=w, lrat=lg)
            reset_prod_limit(wells=w, bhp=press)
    script_off()


def reset_bhp_inj(choke_file, start_date="01.01.2018"):
    """generate rejums for inje wells with info and
    about choke

    :choke_file: TODO
    :returns: TODO

    """
    with open('wconinj.txt', 'w') as f:
        f.write('WCONINJ\n')
        start_date = datetime.strptime(start, '%d.%m.%Y')
        last_date = get_all_timesteps()[-1].to_datetime()-start_date
        last_date = last_date.days
        for m in get_all_models():
            for t in get_all_timesteps():
                if t.to_datetime() == start_date:
                    for w in get_all_wells():
                        if wwit[m, w].max(dates=get_all_timesteps()[-1]) > 0:
                            avg_wir_for_forecast = (wwit[m, w].max(
                                dates='all') - wwit[m, w, t])/last_date
                            avg_bhp_for_forecast = wbhp[m, w].fix(
                                date=get_all_timesteps()[-1])
                            avg_bhp_for_forecast = float(avg_bhp_for_forecast)
                            avg_wir_for_forecast = float(avg_wir_for_forecast)

                        injec_rejums = f"'{w.name}' WATER OPEN RATE {round(avg_wir_for_forecast, 2)} 1* {round(avg_bhp_for_forecast, 1)} /\n"
                        f.writelines(injec_rejums)
                        print(injec_rejums)
    f.writelines('/')

    pass


def shut_inj():
    """script stoped all injected wells"""
    for w in get_all_wells():
        if wwir[w] > 0:
            set_inj_limit(wells=w, fluid="water", rate=0)
    script_off()

def dobstop(lim):
    """script stoped all injected wells"""
    stoped_wells = {}
    for w in get_all_wells():
        if wwct[w] > lim:
            names=w.name
            print(names)
            stoped_wells[names]=float(wlpr[w])
            set_prod_limit(wells=w, lrat=0)
    with open(r"d:\project\Minnib_project\SCHED_PATTERNS\new_wells.pickle", 'wb') as target:
        pickle.dump(stoped_wells, target)
        print(stoped_wells)
    script_off()

def drilling_schedule(well_per_year):
    """open limit position of new wells for product or inject"""
    wlist =['P9598A', 'P3442A', 'P32005', 'P32000', 'P20534A', 'P474D', 'P472D', 'P471D', 'P3456D', 'P3456A', 'P3455D', 'P20682A', 'P20680', 'P20216A', 'P32664', 'P258A', 'P257D', 'P20630', 'P20350', 'P20277', 'P434D', 'P3486D', 'P3486B', 'P3486A', 'P32647', 'P32645A', 'P32022', 'P20132', 'P20120A', 'P32666', 'P178A', 'P10789A', 'P10753A', 'P9530A', 'P20158A', 'P20156A', 'P32754', 'P32751', 'P304D', 'P20581', 'P20221A', 'P10862A', 'P10861A', 'P467D', 'P464D', 'P32759', 'P20685', 'P20450B', 'P20181A', 'P32775', 'P20164', 'P32710', 'P3162A', 'P14987', 'P9541B', 'P442A', 'P20481A', 'P20127A', 'P20117', 'P484A', 'P3472A', 'P20559', 'P15713A', 'P1220A', 'P490D', 'P20596', 'P20540', 'P20526', 'P14963A', 'P3454A', 'P3453A', 'P32760', 'P20672', 'P20435', 'P20337A', 'P14983A', 'P3190A', 'P3189D', 'P20105A', 'P9635A', 'P32747', 'P229A', 'P10860A', 'P197A', 'P14993A', 'P10863A', 'P32725', 'P10767A', 'P32672A', 'P32672', 'P20622', 'P177A', 'P14918', 'P9501A', 'P9500A', 'P9555A', 'P3475A', 'P20378', 'P15672A', 'P9536A', 'P283A', 'P10841A', 'P9622A', 'P20149A', 'P196D', 'P3193A', 'P20518A', 'P10852A', 'P9626A', 'P203A', 'P14986', 'P32755', 'P10820D', 'P10819A', 'P20655', 'P32728A', 'P14974D', 'P1218D', 'P679A', 'P3167A', 'P3166A', 'P3139B', 'P20656A', 'P20692', 'P20176A', 'P10821A', 'P32763', 'P20646', 'P20492', 'P32799', 'P3199A', 'P20479A', 'P467A', 'P32758', 'P20186A', 'P32742', 'P32741', 'P20374A', 'P246D', 'P192D', 'P9585D', 'P9564A', 'P3695A', 'P32660A', 'P10769A', 'P9597A', 'P241D', 'P32767', 'P20997', 'P14931D', 'P10789B', 'P32703', 'P20590A', 'P15642A', 'P32715', 'P15639A', 'P3101A', 'P14938A', 'P3466A', 'P32736', 'P20327A', 'P504A', 'P32787A', 'P20519', 'P10825A', 'P32746A', 'P20455A', 'P20643', 'P20331A', 'P32766', 'P15782A', 'P20358A', 'P235A', 'P20461A', 'P10754A', 'P9621A', 'P3073A', 'P20546', 'P14966A', 'P20769', 'P20728', 'P32700', 'P532A', 'P9629A', 'P59A', 'P20697', 'P175A', 'P20388A', 'P3097A', 'P273D', 'P9545A', 'P9636A', 'P20324A', 'P20547', 'P10777A', 'P20D', 'P3696A', 'P10818A', 'P9649A', 'P20464', 'P10855A', 'P266D', 'P3188A', 'P20436A', 'P20365', 'P20554', 'P10847A', 'P20364A', 'P32790', 'P15720A', 'P20223A', 'P20217', 'P1968A']
    print(well_per_year)
    # for well in get_wells_by_mask ('P*'):
    #     wlist.append(well.name)
    # wlist =[]
    count = 1 
    for w in wlist:
        well = get_well_by_name(w)
        if wopt[well]==0 and count<=well_per_year:
            print(w, well_per_year, count)
            set_well_status(wells = w, status = 'open')
            set_prod_limit(wells=w,control_mode='LRAT', lrat=100, orat=15, bhp=70)
            # reset_prod_limit(wells=w, bhp=70)
            count+=1
        elif wdraw[well]<5 and wbhp[well]>50:
            press = wbhp[well]-5
            # set_prod_limit(wells=well, lrat=lg)
            reset_prod_limit(wells=well, bhp=press)
        else:
            lg = wlpr[well]
            press = wbhp[well]
            # set_prod_limit(wells=well, lrat=lg)
            reset_prod_limit(wells=well, bhp=press)
    script_set_options(min_interval=datetime.timedelta(days = 26))


def stopstart():
    """script for continue to prod stoped wells"""
    with open(r"d:\project\Minnib_project\SCHED_PATTERNS\new_wells.pickle", 'rb') as target:
        stoped_wells = pickle.load(target)
        print(stoped_wells)
        for key, values in stoped_wells.items():
            set_prod_limit(wells=key, lrat=values)
    script_off()

def inj_to_prod():
    """script for continue to prod stoped wells"""
    welllist = ['I4035D', 'I406D', 'I3112A', 'I32777', 'I3187A', 'I1974A', 'I32701', 'I20309', 'I32712', 'I20213A', 'I20227A', 'I20107', 'I20280', 'I20266', 'I9567A', 'I20510A', 'I32656', 'I3111D', 'I3140A', 'I3142D', 'I32769', 'I32771', 'I3487D', 'I20443A', 'I20584', 'I20584A', 'I20555', 'I32731', 'I485D', 'I3159A', 'I3166D', 'I681A', 'I10864A', 'I20239', 'I15612A', 'I20598', 'I20599', 'I20600', 'I32688', 'I32690', 'I9572A', 'I20197A', 'I20580', 'I32749', 'I20450A', 'I20681', 'I20686', 'I469D', 'I14937A', 'I14939A', 'I20349A', 'I20406A', 'I10827A', 'I20460', 'I32761', 'I20240', 'I20244', 'I32735', 'I3464D', 'I10896', 'I20369', 'I3116A', 'I32762', 'I32764', 'I32765', 'I20265', 'I20495', 'I20539', 'I20597', 'I32691', 'I20142', 'I32009', 'I9648D', 'I20242', 'I20562', 'I20565', 'I217A', 'I217D', 'I3466D']
    for w in get_all_wells():
        if w.name in welllist:
            print(w.name)
            set_prod_limit(wells=w, lrat=100)
            reset_prod_limit(wells=w, bhp=70)
    script_off()



def list_creater():
    with open(r"d:\project\Minnib_project\SCHED_PATTERNS\new_wells.pickle", "wb") as f:
        w = []
        pickle.dump(w, f)
    script_off()


def BHP_control():
    wg = get_global_graph(name="wells_BHP")
    with open(r"d:\project\Minnib_project\SCHED_PATTERNS\new_wells.pickle", "rb") as f:
        wells = pickle.load(f)
        print(wells)
        for w in get_wells_by_mask("P*"):
            if wlpt[w] > 0 and w.name not in wells:
                lg = wlpr[w] * 1
                wg[w] = wbhp[w]
                wells.append(w.name)
                set_prod_limit(wells=w, lrat=lg)
                reset_prod_limit(wells=w, bhp=wg[w])
                with open(
                    r"d:\project\Minnib_project\SCHED_PATTERNS\new_wells.pickle", "wb"
                ) as f:
                    pickle.dump(wells, f)
    script_off()


def read_wells_frack(file_name='wells_base.hdf5'):
    """TODO: Docstring for read_wells_frack.
    :file: file with frack param for take list of wellnames
    :returns: list of wellnames
    """
    hdf5File = os.path.join(get_project_folder(), 'reports', 'FRACK', file_name)
    for w in get_all_wells():
        res = hdf5.get_well(w.name)
        if len(res)>1:
            for x in res:
                add_keyword(f'WFRACP\n{x}')
        else:
            add_keyword(f'WFRACP\n{res}')


def grp_control(path):
    well_list = read_wells_frack(path)
    well_list_a = []
    wg = get_global_graph(name="wells_GRP")
    for w in get_all_wells():
        if w.name in well_list or w.name in well_list_a:
            lg = wlpr[w] * 1.5 if wlpr[w] * 1.5 < 25 else wlpr[w] + 20
            set_prod_limit(wells=w, lrat=lg)
            reset_prod_limit(wells=w, bhp=wbhp[w])
    script_off()


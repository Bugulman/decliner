import pickle
import datetime
from collections import OrderedDict

def list_creater():
    '''Вызываешь сперва эту функцию для формирования файла со списком проектных скважин'''
    with open(r"d:\project\Minnib_project\SCHED_PATTERNS\new_wells.pickle", "wb") as f:
        # тут задаешь полный список с бурением, он попадет в файл. Путь укажи какой нужен
        wells_dict = OrderedDict()
        wells = ['I4035D', 'I406D']
        for w in wells:
            wells_dict[w] = 0
        pickle.dump(wells_dict, f)
    script_off()


def drilling_schedule(well_per_year=1):
    """open limit position of new wells for product or inject"""
    with open(r"d:\project\Minnib_project\SCHED_PATTERNS\new_wells.pickle", "rb") as f:
        wells = pickle.load(f)
        wlist = wells.keys()
        print(well_per_year)
        count = 1
        for w in wlist:
            well = get_well_by_name(w)
            if wopt[well] == 0 and count <= well_per_year:
                # это блок включает скважины в добычу
                set_well_status(wells=w, status='open')
                add_keyword(
                    """
                    WECONPROD
                    """+well.name+""" STOP /
                    /
                    """)
                # set_prod_limit(wells=w, control_mode='LRAT',
                               # lrat=100, orat=15, bhp=70)
                count += 1
                wells[w] += 1
            elif wopt[well] > 0 and w.endswith('I') and wells[w] >= 5:
                # проверка для перевода в нагнетание
                add_keyword(
                    """
                    WECONINJ
                    """+well.name+""" STOP /
                    /
                    """)
            elif wopt[well] > 0:
                # счетчик месяцев работы скважин
                wells[w] += 1
            else:
                pass
        # переписываем файл
        pickle.dump(wells, f)
        # script_set_options(min_interval=datetime.timedelta(days=26))

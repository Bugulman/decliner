#Automaticaly recalculate=true
#Single model=false
# Automaticaly recalculate=true
# Single model=false
# Automaticaly recalculate=true
# Single model=false
import csv
import oily_report as olr
import os
import h5py

# скрипт сравнивает дополнительную добычу в двух моделях
# блок с формированием списка моделей
models = []
model_for_compare = get_model_by_name('MINN_FRACK')
model_to_compate = get_model_by_name('MINN_BASE')
models.append(model_for_compare)
models.append(model_to_compate)

# блок формирования даты для среза значений
data = ['01.08.2023', '01.01.2034']
step = []
for t in get_all_timesteps():
    if t.name in data:
        step.append(t)

hdf5File = os.path.join(get_project_folder(), 'reports',
                        'FRACK', 'wells_base.hdf5')

##
with h5py.File(hdf5File, 'r+') as f:
    temp_dict = []
    for wellname in f.keys():
        for plast in f[wellname].keys():
            if f[wellname][plast].attrs.get('works') == 'frack':
                temp_dict.append(f[wellname].attrs.get('psevdo'))
print(temp_dict)
##

olr.create_report_dir(path=get_project_folder())

with open('GRP_analitic.csv', "w", newline='') as csv_file:
    writer = csv.writer(csv_file, delimiter=',')
    writer.writerow(['well', 'oil+', 'wct+', 'oil_tot+', 'wat_tot+'])
    for w in get_all_wells():
        if w.name in temp_dict:
            dif = wopr[w, step[0], models[0]]-wopr[w, step[0], models[1]]
            dif_wct = wwct[w, step[0], models[0]]-wwct[w, step[0], models[1]]
            dif_o = wopt[w, step[1], models[0]]-wopt[w, step[1], models[1]]
            dif_w = wwpt[w, step[1], models[0]]-wwpt[w, step[1], models[1]]
            if dif != 0:
                writer.writerow([w, float(dif), float(
                    dif_wct), float(dif_o), float(dif_w)])

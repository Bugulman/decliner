# пишите здесь ваш код
import pandas as pd
import os
import pickle
import oily_report as olr

# for n, t in enumerate(get_all_timesteps( )[851:871]):
# print(n,t)
olr.create_report_dir(path=get_project_folder())
last_prod_period = get_all_timesteps()[-12:-1]
cells = {}
top_near_w = 5
cell_dim = 77

# формирование фрейма данных по всем скважинам
for w in get_all_wells():
    try:
        con = w.connections[0]
        cells[w.name] = {'i': con.i,
                         'j': con.j,
                         'opr': float(wopr[w].avg(dates=last_prod_period)),
                         'lpr': float(wlpr[w].avg(dates=last_prod_period)),
                         }
    except:
        print(f'Скважина {w.name} без перфораций')
wells = pd.DataFrame(cells)
wells = wells.T.reset_index()
wells.columns = ['well', 'x', 'y', 'oil', 'liq']


# Обработка показателей по ближайшим точкам
for i, j in wells.groupby(by='well'):
    x = float(wells.loc[wells['well'] == i, 'x'].values)
    y = float(wells.loc[wells['well'] == i, 'y'].values)
    wells['sum'] = ((wells['x']-x)**2+(wells['y']-y)**2)**0.5
    wells.loc[wells['well'] == i,
              'Расстояние'] = wells[(wells['oil'] > 0) & (wells['sum'] > 0)]['sum'].min()*cell_dim
    a = wells[(wells['oil'] > 0) & (wells['sum'] > 0)].sort_values(by='sum', ascending=True)[
        'well'].head(5).to_list()

    nearest_wells = ', '.join([str(elem) for elem in a])
    wells.loc[wells['well'] == i,
              'Ближайшие скважины'] = nearest_wells
    wells.loc[wells['well'] == i, 'oil_near'] = wells[wells['oil'] > 0].sort_values(
        by='sum', ascending=True)['oil'].head(top_near_w).mean()
    wells.loc[wells['well'] == i, 'liq_near'] = wells[wells['oil'] > 0].sort_values(
        by='sum', ascending=True)['liq'].head(top_near_w).mean()

# Блок экспорта данных
with open('some.pickle', 'wb') as file:
    pickle.dump(wells, file)
# print(os.getcwd())
# wells.to_excel('remove.xlsx')

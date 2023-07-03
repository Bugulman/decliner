

#пишите здесь ваш код
import datetime
import oily_report as olr
import pandas as pd
import pickle
olr.create_report_dir(path=get_project_folder())
import math
from itertools import accumulate

# исходные данные для проведения экономического расчета
depreciation_year = 8  # year
imushes_tax = 2.2  # %
prib_tax = 20  # %
oil_price = 17259  # rub/t.tonn
opex_oil = 29.29  # rub/tonn
opex_liq = 73.25  # rub/tonn
ndpi = 9980
capex = 20637  # t.rub
k_disk = 10  # t.rub
m = get_all_models ()[0]


# показатели для расчета
oil_prod_gr = graph(type='field', default_value=0)
liq_prod_gr = graph(type='field', default_value=0)
cash_gr = graph(type='field', default_value=0)
tot_opex_gr = graph(type='field', default_value=0)
deprec_gr = graph(type='field', default_value=0)
val_profit_gr = graph(type='field', default_value=0)
imushes_tax_gr = graph(type='field', default_value=0)
prib_tax_gr = graph(type='field', default_value=0)
dry_prib_gr = graph(type='field', default_value=0)
saldo_cashflow_gr = graph(type='field', default_value=0)
disk_saldo_gr = graph(type='field', default_value=0)
disk_prof_gr = graph(type='field', default_value=0)
disk_losses_gr = graph(type='field', default_value=0)
npv_gr = graph(type='field', default_value=0)
iddz_gr = graph(type='field', default_value=0)
temp = graph(type='field', default_value=0)

start = 2021  # дата начала прогноза
end = 2024  # дата окончания прогноза
den = 1

olr.create_report_dir(path=get_project_folder())

# Блок для анализа продолжательности прогноза
colls = [(x.to_datetime().year-start) for x in get_all_timesteps()]
colls = max(colls)+1
print(f'Анализ прогноза на {colls} лет с {start} по {end} год')

# Блок выборки целевых временных шагов на начало года.
# WARN: ВАЖНО чтобы шаги были заказаны в модели!
steps = []
for t in get_all_timesteps():
    if t.to_datetime().day == 1 and t.to_datetime().month == 1\
            and t.to_datetime().year >= start and t.to_datetime().year <= end:
        steps.append(t)

# Считаем количество новых скважин
new_well_quant = []
added_pwells = if_then_else (diff(fmwpr)>0 ,diff(fmwpr), 0)
added_iwells = if_then_else (diff(fmwin)>0 ,diff(fmwin), 0)

for t in steps:
	from_model = shift_t (graph=added_pwells,shift=-12, default=0).aggregate_by_time_interval (interval = 'year', type = 'sum')[m,t]+\
	shift_t (graph=added_iwells,shift=-12, default=0).aggregate_by_time_interval (interval = 'year', type = 'sum')[m,t]
	new_well_quant.append(float(from_model))


# Блок рассчета амортизации
# WARN: Функцию нужно бы переписать не рекурсивную, так как не учитывается ввод последовательно в несколько лет
depreciation = [0]*colls
cum_new_well_quant = list(accumulate(new_well_quant))
if colls>=depreciation_year:
    for i in range(depreciation_year):
        #print(i, depreciation)
        depreciation[i] = capex*cum_new_well_quant[i]/depreciation_year
else:
    for i in range(colls):
        #print(i, depreciation)
        depreciation[i] = capex*cum_new_well_quant[i]/depreciation_year
print(new_well_quant, depreciation)

for t in steps:
    print(t.name)


df = []
# Блок расчета и вывода данных годовой добыче нефти и жидкости по скважинам
amort = (a for a in depreciation)
drill_capex = (cap*capex for cap in new_well_quant)
new_wells = (wells for wells in new_well_quant)
diskont = ((1/(1+k_disk/100))**x for x in range(colls))
for t in steps:
    if t.to_datetime().year == start:
        oil_old = float(fopt[m, t]/1000)
        liq_old = float(flpt[m, t]/1000)
        well = next(new_wells)
        a = next(amort)
        tot_capex = next(drill_capex)
    else:
        a = next(amort)
        k = next(diskont)
        tot_capex = next(drill_capex)
        well = next(new_wells)
        year_oil = float(fopt[m, t]/1000)-oil_old
        year_liq = float(flpt[m, t]/1000)-liq_old
        cash_gr[t] = year_oil*oil_price
        tot_opex_gr[t] = (year_oil*(ndpi+opex_oil) + \
                             (year_liq*opex_liq))*(-1)
        deprec_gr[t] = -a
        val_profit_gr[t] = cash_gr[t] + \
            tot_opex_gr[t]+deprec_gr[t]
        imushes_tax_gr = (-1)*(2*capex+shift_t(graph=cum_sum(temp),
                                                  shift=12, default=0)+deprec_gr)/2*imushes_tax/100
        temp[t] = -2*a
        prib_tax_gr[t] = -prib_tax/100.0 * (val_profit_gr[t]+imushes_tax_gr[t])
        dry_prib_gr[t] = val_profit_gr[t] + \
            imushes_tax_gr[t]+prib_tax_gr[t]
        saldo_cashflow_gr[t] = -capex - deprec_gr[t]+dry_prib_gr[t] \
            if t.to_datetime().year == start+1 \
            else (-1)*deprec_gr[t]+dry_prib_gr[t]
        disk_saldo_gr[t] = k*saldo_cashflow_gr[t]
        disk_prof_gr[t] = cash_gr[t]*k
        disk_losses_gr[t] = (-capex + tot_opex_gr[t]+imushes_tax_gr[t]+prib_tax_gr[t])*k \
            if t.to_datetime().year == start+1 \
            else (tot_opex_gr[t]+imushes_tax_gr[t]+prib_tax_gr[t])*k
        oil_prod_gr[t] = year_oil
        liq_prod_gr[t] = year_liq
        npv_gr = cum_sum(disk_saldo_gr)
        iddz_gr = (-1)*cum_sum(disk_prof_gr) / \
            cum_sum(disk_losses_gr)
        
        print(t.name, a, k, tot_capex, well, year_oil, year_liq)
        oil_old = float(fopt[m, t]/1000)
        liq_old = float(flpt[m, t]/1000)
#

export(oil_prod_gr, name='Year_oil_production', units='liquid_surface_volume')
export(liq_prod_gr, name='Year_liq_production', units='liquid_surface_volume')
export(cash_gr, name='Выручка', units='diametr')
export(tot_opex_gr, name='Затраты на добычу',
       units='diametr')
export(deprec_gr, name='Амортизация', units='diametr')
export(val_profit_gr, name='Валовая прибыль', units='diametr')
export(imushes_tax_gr, name='Имущественный налог', units='diametr')
export(prib_tax_gr, name='Налог на прибыль', units='diametr')
export(dry_prib_gr, name='Чистая прибыль', units='diametr')
export(saldo_cashflow_gr, name='Сальдо суммарного потока', units='diametr')
export(npv_gr, name='ЧДД', units='diametr')
export(disk_prof_gr, name='Дисконтированные притоки', units='diametr')
export(disk_losses_gr, name='Дисконтированные оттоки', units='diametr')
export(iddz_gr, name='ИДДЗ', units='diametr')


# df.append([t.name, well, round(float(wopt[w, steps[-1]]), 0),
              # round(float(npv_gr[w, steps[-1]]), 0), round(float(iddz_gr[w, steps[-1]]), 2)])



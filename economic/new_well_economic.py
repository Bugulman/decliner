# Automaticaly recalculate=true
# Single model=false
# пишите здесь ваш код
# пишите здесь ваш кодdate="01.07.2019"
##################################################
################ Script Section ##################
##################################################

import datetime
import oily_report as olr

# исходные данные для проведения экономического расчета
depreciation_year = 8  # year
imushes_tax = 2.2  # %
prib_tax = 20  # %
oil_price = 17259  # rub/t.tonn
opex_oil = 29.29  # rub/tonn
opex_liq = 73.25  # rub/tonn
ndpi = 9980
capex = 31637  # t.rub
k_disk = 10  # t.rub

# показатели для расчета
oil_prod_gr = graph(type='well', default_value=0)
liq_prod_gr = graph(type='well', default_value=0)
cash_gr = graph(type='well', default_value=0)
tot_opex_gr = graph(type='well', default_value=0)
deprec_gr = graph(type='well', default_value=0)
val_profit_gr = graph(type='well', default_value=0)
imushes_tax_gr = graph(type='well', default_value=0)
prib_tax_gr = graph(type='well', default_value=0)
dry_prib_gr = graph(type='well', default_value=0)
saldo_cashflow_gr = graph(type='well', default_value=0)
disk_saldo_gr = graph(type='well', default_value=0)
disk_prof_gr = graph(type='well', default_value=0)
disk_losses_gr = graph(type='well', default_value=0)
npv_gr = graph(type='well', default_value=0)
iddz_gr = graph(type='well', default_value=0)
temp = graph(type='well', default_value=0)


start = 2021  # дата начала прогноза
end = 2037  # дата окончания прогноза
den = 1

olr.create_report_dir(path=get_project_folder())

# Блок для анализа продолжательности прогноза
colls = [(x.to_datetime().year-start) for x in get_all_timesteps()]
colls = max(colls)
print(colls)

depreciation = [0]*colls
for i in range(depreciation_year):
    depreciation[i] = capex/depreciation_year

for i in range(depreciation_year):
    depreciation[i] = capex/depreciation_year


steps = []
for t in get_all_timesteps():
    if t.to_datetime().day == 1 and t.to_datetime().month == 1\
            and t.to_datetime().year >= start:
        steps.append(t)


# Блок для анализа даты ввода скважины
drill_date = {}

for m in get_all_models():
    for w in get_all_wells():
        for t in get_all_timesteps():
            if wstat[m, w, t] == 1 or wstat[m, w, t] == 2:
                drill_date[str(w)] = t.to_datetime()
                break
# print(drill_date)


# Блок расчета и вывода данных годовой добыче нефти и жидкости по скважинам
for m in get_all_models():
    for w in get_all_wells():
        amort = (a for a in depreciation)
        diskont = ((1/(1+k_disk/100))**x for x in range(colls))
        for t in steps:
            if t.to_datetime().year == start:
                oil_old = float(wopt[m, w, t]/1000)
                liq_old = float(wlpt[m, w, t]/1000)
            else:
                a = next(amort)
                k = next(diskont)
                year_oil = float(wopt[m, w, t]/1000)-oil_old
                year_liq = float(wlpt[m, w, t]/1000)-liq_old
                cash_gr[w, t] = year_oil*oil_price
                tot_opex_gr[w, t] = (year_oil*(ndpi+opex_oil) +
                                     (year_liq*opex_liq))*(-1)
                deprec_gr[w, t] = -a
                val_profit_gr[w, t] = cash_gr[w, t] + \
                    tot_opex_gr[w, t]+deprec_gr[w, t]
                imushes_tax_gr[w] = (-1)*(2*capex+shift_t(graph = cum_sum(temp[w]), shift=12, default=0)+deprec_gr[w])/2*imushes_tax/100
                temp[w, t] = -2*a
                prib_tax_gr[w, t] = -prib_tax/100.0*(val_profit_gr[w, t]+imushes_tax_gr[w, t])
                dry_prib_gr[w, t] = val_profit_gr[w,t]+imushes_tax_gr[w,t]+prib_tax_gr[w, t]
                saldo_cashflow_gr[w, t] = -capex - deprec_gr[w,t]+dry_prib_gr[w,t] \
                        if t.to_datetime().year == start+1 \
                        else (-1)*deprec_gr[w,t]+dry_prib_gr[w,t]
                disk_saldo_gr[w, t] = k*saldo_cashflow_gr[w, t] 
                disk_prof_gr[w, t] = cash_gr[w, t]*k
                disk_losses_gr[w, t] = (-capex + tot_opex_gr[w, t]+imushes_tax_gr[w, t]+prib_tax_gr[w, t])*k \
                        if t.to_datetime().year == start+1 \
                        else (tot_opex_gr[w, t]+imushes_tax_gr[w, t]+prib_tax_gr[w, t])*k                 
                oil_prod_gr[w, t] = year_oil
                liq_prod_gr[w, t] = year_liq
                npv_gr[w] = cum_sum(disk_saldo_gr[w])
                iddz_gr[w] = cum_sum(disk_prof_gr[w])/cum_sum(disk_losses_gr[w])
                oil_old = float(wopt[m, w, t]/1000)
                liq_old = float(wlpt[m, w, t]/1000)
        print(f' скважина {w.name} ЧДД {round(float(npv_gr[w, steps[-1]]),0)} \
                ИДДЗ {round(float(iddz_gr[w, steps[-1]]),2)}')

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

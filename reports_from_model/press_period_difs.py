#Automaticaly recalculate=true
#Single model=false
from datetime import datetime

inj_period = graph(type='well', default_value=0)
press_dif = graph(type='well', default_value=0)


start = '01.01.2001'

start_date = datetime.strptime(start, '%d.%m.%Y')
for m in get_all_models():
	for t in get_all_timesteps():
		if t.to_datetime() >= start_date:
			for w in get_all_wells():
				inj_period[m,w,t] = wwir[m,w,t]
				if wthph[m,w,t] > 0 and wlpr[m,w,t]>0:
					press_dif[w, t] = wbp9[w,t]-wthph[w,t]

export(cum_sum (inj_period), name='inj_period', units='liquid_surface_rate')
export(cum_sum (press_dif), name='dif_press', units='pressure')

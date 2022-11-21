#Automaticaly recalculate=false
#Single model=false
import time
start_time = time.time()

#MODEL_CELLS = {1: [1,11],2: [14,24], 3: [25,31],4:[32,39],5:[40,48],6:[49,56],7:[57,65],8:[66,81],9:[82,96],10:[97,104],11:[105,110]}
MODEL_CELLS = {1: [1,25],2: [26,43], 3: [45,54], 4:[55,75],5:[76,92],6:[93,125],7:[129,200]}
GOR_NAME = {1: 'd0',2: 'a,b1,b2', 3: 'b3', 4:'v',5:'g1',6:'g2+',7:'d'}

zone = dict()

for k, v in MODEL_CELLS.items():
    zone[k] = graph (type = 'well', default_value = 0)

for m in get_all_models():
    if flpth[m].max(dates='all') > 0:
        for w in get_all_wells():
            if wlpth[m,w].max(dates='all') > 0 or wwith[m,w].max(dates='all') > 0:
                for t in get_all_timesteps():
#                    d_inter = dict()
                    for key,v in MODEL_CELLS.items():
                        for c in w.connections:
                            if (clpr[m,c,t].to_list()[0] != 0 or cwir[m,c,t].to_list()[0] != 0) and v[0] <= int(c.k) <= v[1]:
                                zone[key][m,w,t] = key
                                break

for k, v in GOR_NAME.items():
    export(zone[k], name = str(v))

print('Время выполнения программы',round((time.time() - start_time)/60,1),sep='\t')

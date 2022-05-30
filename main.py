from files_func import hist_table_prepare
from smoother import histor_smoothing
import pandas as pd
import logging
import pickle
from oily_report import interpolate_press_by_sipy
from DCA import prod_predict, declane_fit, predict_viz
from tqdm import tqdm

logging.basicConfig(level=logging.DEBUG,format = "%(asctime)s - %(levelname)s - %(message)s")

# prod =pd.read_excel(r'data/Свод.xlsx', usecols="B:N")
# press =pd.read_excel(r'data/ГДИ.xlsx', usecols = "F:M")
# print(prod['Горизонт'].unique())
# keyword = {'hist_file':[prod, press], 'gor_num':[476]}
# result = hist_table_prepare(**keyword)
# smooth_res = histor_smoothing(result)
# logging.info(smooth_res.head(4))
# # locals = result.loc[result['№ скваж']=='1100']
# with open(r'data/onewell.pickle','wb') as f:
#     pickle.dump(smooth_res, f)

with open(r'data/onewell.pickle','rb') as f:
    df=pickle.load(f)

names = df.loc[(df.status == 'prod') & (df['date'] > '2010'), 'well'].unique()
# predict=pd.DataFrame(columns=['well', 'date', 'SOIL', 'QOIL', 'Time_x', 'Time_y', 'rate', 'month_prod'])
dca_full=pd.DataFrame(columns=['well', 'first_date', 'qi', 'Di', 'bi', 'Dterm'])
for name, fr in tqdm(df.loc[df.well.isin(names)].groupby('well')):
    dca_param= declane_fit(fr)
    dca_full = pd.concat([dca_full, dca_param], ignore_index=True)

# for name, fr in tqdm(df.loc[df.well.isin(names)].groupby('well')):
dca_full.index=dca_full.well
t = dca_full.loc['975'].values
f=df.loc[df['well']=='975']
date = t[1]
params = t[2]
rate = prod_predict(date, params)
__import__('pdb').set_trace()
predict_viz(f, date , params)
print(rate)

# predict.to_csv(f'decline_M.csv')


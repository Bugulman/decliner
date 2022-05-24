from files_func import hist_table_prepare
from smoother import histor_smoothing
import pandas as pd
import logging
import pickle
from oily_report import interpolate_press_by_sipy
from DCA import dec_predict
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
predict=pd.DataFrame(columns=['well', 'date', 'SOIL', 'QOIL', 'Time_x', 'Time_y', 'rate', 'month_prod'])
for name, fr in tqdm(df.loc[df.well.isin(names)].groupby('well')):
    well_predict = dec_predict(fr)
    predict = pd.concat([predict, well_predict], ignore_index=True)
predict.to_csv(f'decline_M.csv')


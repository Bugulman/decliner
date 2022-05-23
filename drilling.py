from files_func import hist_table_prepare
from smoother import histor_smoothing
import pandas as pd
import logging
import pickle
from oily_report import interpolate_press_by_sipy

logging.basicConfig(level=logging.DEBUG,format = "%(asctime)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s")

# prod =pd.read_excel(r'data/Свод.xlsx', usecols="B:N")
# press =pd.read_excel(r'data/ГДИ.xlsx', usecols = "F:M")
# print(prod['Горизонт'].unique())
# keyword = {'hist_file':[prod, press], 'gor_num':[476]}
# result = hist_table_prepare(**keyword)
# smooth_res = histor_smoothing(result)

# locals = result.loc[result['№ скваж']=='1100']
# with open(r'data/onewell.pickle','wb') as f:
#     pickle.dump(locals, f)

with open(r'data/onewell.pickle','rb') as f:
    result=pickle.load(f)

logging.info(f'done {result.columns}')
interpolate_press_by_sipy(result)


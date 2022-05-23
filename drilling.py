from files_func import hist_table_prepare
from smoother import histor_smoothing
import pandas as pd
import logging
import pickle
from oily_report import interpolate_press_by_sipy

logging.basicConfig(level=logging.DEBUG,format = "%(asctime)s - %(levelname)s - %(message)s")

prod =pd.read_excel(r'data/Свод.xlsx', usecols="B:N")
press =pd.read_excel(r'data/ГДИ.xlsx', usecols = "F:M")
print(prod['Горизонт'].unique())
keyword = {'hist_file':[prod, press], 'gor_num':[476]}
result = hist_table_prepare(**keyword)
smooth_res = histor_smoothing(result)
logging.info(smooth_res.head(4))
# locals = result.loc[result['№ скваж']=='1100']
with open(r'data/onewell.pickle','wb') as f:
    pickle.dump(smooth_res, f)

# with open(r'data/onewell.pickle','rb') as f:
#     result=pickle.load(f)

# histor_smoothing(result)


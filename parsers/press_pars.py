# %%
from support_func import file_runer, convert_excel_KVD, convert_csv_KVD
from pathlib import Path
from tqdm import tqdm
from sqlalchemy import create_engine
import warnings
import sys
sys.path.append('/home/albert.vafin/Documents/python_proj/decliner/parsers')
warnings.filterwarnings('ignore')

# NOTE: подключение к базе sqllite
engine = create_engine('sqlite:///press.db')

# %%

# Перечень файлов паспортов скважин
# WARN: запускается единожды!
p = Path(r'/cluster3/public/2023/UNGKM/Data Achimgas/Замеры забойных давлений')


# %%
csv_files = file_runer(p, 'CSV', regex_file='GA.*') + \
    file_runer(p, 'csv', regex_file='GA.*')
excel_files = file_runer(p, 'xls') + \
    file_runer(p, 'XLS')
# %%
convert_excel_KVD(excel_files[1])
# %%
# NOTE: ИМПОРТ исхдников из экселей в базу данных
with open('zaboi_excel.txt', 'w') as f:
    for n in tqdm(excel_files):
        try:
            df = convert_excel_KVD(n)
            df.to_sql('zaboi_excel', con=engine, if_exists='append')
        except:
            f.write(f'{n}\n')
            print(n)


# %% NOTE: ИМПОРТ исхдников из csv в базу данных
for n in tqdm(csv_files):
    try:
        df = convert_csv_KVD(n)
        df.to_sql('zaboi_csv', con=engine, if_exists='append')
    except:
        print(f'not{n}')
    # df.to_sql('zaboi_csv', con=engine, if_exists='append')

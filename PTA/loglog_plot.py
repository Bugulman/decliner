from pta_learn.tpmr import *
from pta_learn.lmir import *
from pta_learn.ti_misc import *
from pta_learn.ti_workflow import *
from pta_learn.superposition_calculation import *
from pta_learn.bourdet_derivative import *
from pta_learn.normalization import *
import os
import warnings

warnings.filterwarnings("ignore")

df = pd.read_csv("test.csv", parse_dates=True)
df["Timestamp"] = pd.to_datetime(df["Timestamp"])
# df.index = df["Timestamp"]
df["Time"] = (df["Timestamp"] - df["Timestamp"].min()) / pd.Timedelta(hours=1)
df_bhp = df.loc[:, ["Pressure", "Time", "Timestamp"]]
df_rate = df.loc[:, ["Rate", "Time", "Timestamp"]]

# %%
# plot_whole(df_bhp, df_rate)
# %%

# p is the relative pressure drop in a shut-in transient
p = 0.1
# order (int, optional): The number of adjacent points on each side of a data point to compare when identifying local minima.
order = 50
# interval_shutin is the minimum time duration in a shut-in transient in hours
interval_shutin = 10
# interval_flowing is the minimum time duration in a flowing transient in hours
interval_flowing = 30
# %%
# PTA_f = detect_bottombp(df_bhp, p)
# split_df = split_dataframe(df_bhp, PTA_f)
# PTA_s = detect_topbp(split_df)
# PTA = detect_PTA(df_bhp, PTA_f, PTA_s)
# TI = detect_TI(PTA_f, PTA_s, interval_shutin)
# %%
shutin_bp_all, PTA_f, PTA_s, shutin_bp_interval = detect_breakps(
    df_bhp, p, interval_shutin
)
shutin_bp_all
# %%

def get_shutin_bps(PTA):
    """
    Returns: all detected shut-in transients without interval limitation
    """

    if PTA.empty:
        shutin_breakpoints = pd.DataFrame()
    
    else:
        # select row with shutin label
        PTA_shutin = PTA.loc[PTA['label'] == 'shutin']
        # select the column Time
        PTA_shutin_start = PTA_shutin[['Timestamp','Time']].reset_index(drop=True)
        print(PTA_shutin_start)

        # select row with flow label
        PTA_flow = PTA.loc[PTA['label'].isin(['flowing', 'end'])]
        # select the column Time 
        PTA_flow_end = PTA_flow[['Timestamp','Time']].reset_index(drop=True)
        print(PTA_flow_end)
        # make a new dataframe with the start and end times
        shutin_breakpoints = pd.DataFrame({'start/hr': PTA_flow_end.Time, 'end/hr': PTA_shutin_start.Time, 
                            'duration/hr': PTA_flow_end.Time - PTA_shutin_start.Time,
        'start/timestamp': PTA_shutin_start.Timestamp, 'end/timestamp': PTA_flow_end.Timestamp})

        # add each row a new column with the status of "shutin"
        shutin_breakpoints['status'] = 'shutin'

    return shutin_breakpoints
# %%

# %%
shutin_transient_all = get_shutin_bps(shutin_bp_all)
shutin_transient_all.T
# %%
injection_periods = create_injection_periods(shutin_transient_all, df_bhp)
injection_periods
# %%

shutin, flowing, TI, TI_ft, all_breakpoints, w_rate, para = ti_workflow(
    df_bhp, df_rate, p, interval_shutin, interval_flowing, order=order
)

flowing
# %%
plot_target(df_bhp, df_rate, shutin, flowing)

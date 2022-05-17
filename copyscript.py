#Automaticaly recalculate=true
#Single model=false
import shutil
import os
import schedule
import time

# for direc, some, file in os.walk(r"m:\dell-3x36-gpu\cc02\MINN_15.12_SCH\RESULTS"):
def copyfiles(from_filepath, to_filepath):
    """copy files for schedule

    :from_filepath: TODO
    :to_filepath: TODO
    :returns: TODO

    """
    for direc, some, file in os.walk(from_filepath):
        for files in file:
            print(direc, files)
            from_filepath = direc + "/" + files
            to_file = to_filepath + files
            print(from_filepath)
            shutil.copyfile(from_filepath, to_file)


schedule.every().day.at("05:00").do(
    copyfiles,
    from_filepath="m:/dell-3x36-gpu/cc02/MINN_15.12_SCH/RESULTS/",
    to_filepath="D:/project/Minnib_project/SCHED_PATTERNS/RESULTS/",
)

while True:
    schedule.run_pending()
    time.sleep(60)

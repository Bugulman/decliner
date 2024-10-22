#  Этот файл был сгенерирован тНавигатор v24.2-3873-ga13217a7bed6.
#  Copyright (C) Рок Флоу Динамикс 2005-2024.
#  Все права защищены.

# This file is MACHINE GENERATED! Do not edit.

#api_version=v0_0_145

from __main__.tnav.workflow import *
from tnav_debug_utilities import *
from datetime import datetime, timedelta


declare_workflow (workflow_name="multibranch_well",
      variables=[{"name" : "T2", "type" : "real", "min" : 1612, "max" : 1620, "values" : [], "distribution_type" : "Uniform", "discrete_distr_values" : [], "discrete_distr_probabilities" : [], "initial_distribution" : [], "truncated_mean" : 0, "truncated_sigma" : 0, "mode" : 0}, {"name" : "LEN1", "type" : "real", "min" : 300, "max" : 1500, "values" : [], "distribution_type" : "Uniform", "discrete_distr_values" : [], "discrete_distr_probabilities" : [], "initial_distribution" : [], "truncated_mean" : 0, "truncated_sigma" : 0, "mode" : 0}, {"name" : "LEN2", "type" : "real", "min" : 300, "max" : 1500, "values" : [], "distribution_type" : "Uniform", "discrete_distr_values" : [], "discrete_distr_probabilities" : [], "initial_distribution" : [], "truncated_mean" : 0, "truncated_sigma" : 0, "mode" : 0}, {"name" : "LEN3", "type" : "real", "min" : 300, "max" : 1500, "values" : [], "distribution_type" : "Uniform", "discrete_distr_values" : [], "discrete_distr_probabilities" : [], "initial_distribution" : [], "truncated_mean" : 0, "truncated_sigma" : 0, "mode" : 0}, {"name" : "H1", "type" : "real", "min" : 0, "max" : 50, "values" : [], "distribution_type" : "Uniform", "discrete_distr_values" : [], "discrete_distr_probabilities" : [], "initial_distribution" : [], "truncated_mean" : 0, "truncated_sigma" : 0, "mode" : 0}, {"name" : "H3", "type" : "real", "min" : 0, "max" : 20, "values" : [], "distribution_type" : "Uniform", "discrete_distr_values" : [], "discrete_distr_probabilities" : [], "initial_distribution" : [], "truncated_mean" : 0, "truncated_sigma" : 0, "mode" : 0}, {"name" : "H2", "type" : "real", "min" : 0, "max" : 30, "values" : [], "distribution_type" : "Uniform", "discrete_distr_values" : [], "discrete_distr_probabilities" : [], "initial_distribution" : [], "truncated_mean" : 0, "truncated_sigma" : 0, "mode" : 0}, {"name" : "BASE_AZ", "type" : "real", "min" : 0, "max" : 90, "values" : [], "distribution_type" : "Uniform", "discrete_distr_values" : [], "discrete_distr_probabilities" : [], "initial_distribution" : [], "truncated_mean" : 0, "truncated_sigma" : 0, "mode" : 0}, {"name" : "DELTA_AZ_3", "type" : "real", "min" : 5, "max" : 30, "values" : [], "distribution_type" : "Uniform", "discrete_distr_values" : [], "discrete_distr_probabilities" : [], "initial_distribution" : [], "truncated_mean" : 0, "truncated_sigma" : 0, "mode" : 0}, {"name" : "DELTA_AZ_2", "type" : "real", "min" : 10, "max" : 15, "values" : [], "distribution_type" : "Uniform", "discrete_distr_values" : [], "discrete_distr_probabilities" : [], "initial_distribution" : [], "truncated_mean" : 0, "truncated_sigma" : 0, "mode" : 0}, {"name" : "AZ_1_1", "type" : "real", "min" : 0, "max" : 10, "values" : [], "distribution_type" : "Uniform", "discrete_distr_values" : [], "discrete_distr_probabilities" : [], "initial_distribution" : [], "truncated_mean" : 0, "truncated_sigma" : 0, "mode" : 0}, {"name" : "AZ_2_1", "type" : "real", "min" : 0, "max" : 10, "values" : [], "distribution_type" : "Uniform", "discrete_distr_values" : [], "discrete_distr_probabilities" : [], "initial_distribution" : [], "truncated_mean" : 0, "truncated_sigma" : 0, "mode" : 0}, {"name" : "AZ_3_1", "type" : "real", "min" : 0, "max" : 10, "values" : [], "distribution_type" : "Uniform", "discrete_distr_values" : [], "discrete_distr_probabilities" : [], "initial_distribution" : [], "truncated_mean" : 0, "truncated_sigma" : 0, "mode" : 0}, {"name" : "AZ_1_2", "type" : "real", "min" : 0, "max" : 10, "values" : [], "distribution_type" : "Uniform", "discrete_distr_values" : [], "discrete_distr_probabilities" : [], "initial_distribution" : [], "truncated_mean" : 0, "truncated_sigma" : 0, "mode" : 0}, {"name" : "AZ_2_2", "type" : "real", "min" : 0, "max" : 10, "values" : [], "distribution_type" : "Uniform", "discrete_distr_values" : [], "discrete_distr_probabilities" : [], "initial_distribution" : [], "truncated_mean" : 0, "truncated_sigma" : 0, "mode" : 0}, {"name" : "AZ_3_2", "type" : "real", "min" : 0, "max" : 10, "values" : [], "distribution_type" : "Uniform", "discrete_distr_values" : [], "discrete_distr_probabilities" : [], "initial_distribution" : [], "truncated_mean" : 0, "truncated_sigma" : 0, "mode" : 0}, {"name" : "AZ_1_3", "type" : "real", "min" : 0, "max" : 10, "values" : [], "distribution_type" : "Uniform", "discrete_distr_values" : [], "discrete_distr_probabilities" : [], "initial_distribution" : [], "truncated_mean" : 0, "truncated_sigma" : 0, "mode" : 0}, {"name" : "AZ_2_3", "type" : "real", "min" : 0, "max" : 10, "values" : [], "distribution_type" : "Uniform", "discrete_distr_values" : [], "discrete_distr_probabilities" : [], "initial_distribution" : [], "truncated_mean" : 0, "truncated_sigma" : 0, "mode" : 0}, {"name" : "AZ_3_3", "type" : "real", "min" : 0, "max" : 10, "values" : [], "distribution_type" : "Uniform", "discrete_distr_values" : [], "discrete_distr_probabilities" : [], "initial_distribution" : [], "truncated_mean" : 0, "truncated_sigma" : 0, "mode" : 0}, {"name" : "ZEN_1_1", "type" : "real", "min" : -10, "max" : 12, "values" : [], "distribution_type" : "Uniform", "discrete_distr_values" : [], "discrete_distr_probabilities" : [], "initial_distribution" : [], "truncated_mean" : 0, "truncated_sigma" : 0, "mode" : 0}, {"name" : "ZEN_2_1", "type" : "real", "min" : -10, "max" : 12, "values" : [], "distribution_type" : "Uniform", "discrete_distr_values" : [], "discrete_distr_probabilities" : [], "initial_distribution" : [], "truncated_mean" : 0, "truncated_sigma" : 0, "mode" : 0}, {"name" : "ZEN_3_1", "type" : "real", "min" : -10, "max" : 12, "values" : [], "distribution_type" : "Uniform", "discrete_distr_values" : [], "discrete_distr_probabilities" : [], "initial_distribution" : [], "truncated_mean" : 0, "truncated_sigma" : 0, "mode" : 0}, {"name" : "ZEN_1_2", "type" : "real", "min" : -10, "max" : 12, "values" : [], "distribution_type" : "Uniform", "discrete_distr_values" : [], "discrete_distr_probabilities" : [], "initial_distribution" : [], "truncated_mean" : 0, "truncated_sigma" : 0, "mode" : 0}, {"name" : "ZEN_2_2", "type" : "real", "min" : -10, "max" : 12, "values" : [], "distribution_type" : "Uniform", "discrete_distr_values" : [], "discrete_distr_probabilities" : [], "initial_distribution" : [], "truncated_mean" : 0, "truncated_sigma" : 0, "mode" : 0}, {"name" : "ZEN_3_2", "type" : "real", "min" : -10, "max" : 12, "values" : [], "distribution_type" : "Uniform", "discrete_distr_values" : [], "discrete_distr_probabilities" : [], "initial_distribution" : [], "truncated_mean" : 0, "truncated_sigma" : 0, "mode" : 0}, {"name" : "ZEN_1_3", "type" : "real", "min" : -10, "max" : 12, "values" : [], "distribution_type" : "Uniform", "discrete_distr_values" : [], "discrete_distr_probabilities" : [], "initial_distribution" : [], "truncated_mean" : 0, "truncated_sigma" : 0, "mode" : 0}, {"name" : "ZEN_2_3", "type" : "real", "min" : -10, "max" : 12, "values" : [], "distribution_type" : "Uniform", "discrete_distr_values" : [], "discrete_distr_probabilities" : [], "initial_distribution" : [], "truncated_mean" : 0, "truncated_sigma" : 0, "mode" : 0}, {"name" : "ZEN_3_3", "type" : "real", "min" : -10, "max" : 10, "values" : [], "distribution_type" : "Uniform", "discrete_distr_values" : [], "discrete_distr_probabilities" : [], "initial_distribution" : [], "truncated_mean" : 0, "truncated_sigma" : 0, "mode" : 0}])


multibranch_well_variables = {
"T2" : 1613,
"LEN1" : 500,
"LEN2" : 500,
"LEN3" : 300,
"H1" : 50,
"H3" : 20,
"H2" : 30,
"BASE_AZ" : 50,
"DELTA_AZ_3" : 15,
"DELTA_AZ_2" : 10,
"AZ_1_1" : 0,
"AZ_2_1" : 0,
"AZ_3_1" : 0,
"AZ_1_2" : 1,
"AZ_2_2" : 1,
"AZ_3_2" : 1,
"AZ_1_3" : 1,
"AZ_2_3" : 1,
"AZ_3_3" : 1,
"ZEN_1_1" : 5,
"ZEN_2_1" : -10,
"ZEN_3_1" : 5,
"ZEN_1_2" : 1,
"ZEN_2_2" : -4,
"ZEN_3_2" : 1,
"ZEN_1_3" : 1,
"ZEN_2_3" : 1,
"ZEN_3_3" : -10
}

def multibranch_well (variables = multibranch_well_variables):
    pass
    check_launch_method ()

    T2 = variables["T2"]
    LEN1 = variables["LEN1"]
    LEN2 = variables["LEN2"]
    LEN3 = variables["LEN3"]
    H1 = variables["H1"]
    H3 = variables["H3"]
    H2 = variables["H2"]
    BASE_AZ = variables["BASE_AZ"]
    DELTA_AZ_3 = variables["DELTA_AZ_3"]
    DELTA_AZ_2 = variables["DELTA_AZ_2"]
    AZ_1_1 = variables["AZ_1_1"]
    AZ_2_1 = variables["AZ_2_1"]
    AZ_3_1 = variables["AZ_3_1"]
    AZ_1_2 = variables["AZ_1_2"]
    AZ_2_2 = variables["AZ_2_2"]
    AZ_3_2 = variables["AZ_3_2"]
    AZ_1_3 = variables["AZ_1_3"]
    AZ_2_3 = variables["AZ_2_3"]
    AZ_3_3 = variables["AZ_3_3"]
    ZEN_1_1 = variables["ZEN_1_1"]
    ZEN_2_1 = variables["ZEN_2_1"]
    ZEN_3_1 = variables["ZEN_3_1"]
    ZEN_1_2 = variables["ZEN_1_2"]
    ZEN_2_2 = variables["ZEN_2_2"]
    ZEN_3_2 = variables["ZEN_3_2"]
    ZEN_1_3 = variables["ZEN_1_3"]
    ZEN_2_3 = variables["ZEN_2_3"]
    ZEN_3_3 = variables["ZEN_3_3"]

    begin_user_imports ()
    import numpy as np
    import time
    import math
    from datetime import datetime as dt
    end_user_imports ()

    begin_wf_item (index = 1)
    comment_text ("""

Варианты моделей->заказанные графики->список
В поле мнемоники пишем \'WLEN\'(лучше с сохранением регистра). И нажимаем применить(зеленый треугольник)

Скрипт по умолчание ставит забойное давление на скважину 50 на прогноз
""")
    end_wf_item (index = 1)


    begin_wf_item (index = 2, name = "Вносим данные по скважине сюда")
    wellname = 'test2'
    set_var_type (n = "wellname", t = "STRING", it = "PY_EXPR", val = wellname)
    variables["WELLNAME"] = wellname
    strategy_name = 'MODELUP'
    set_var_type (n = "strategy_name", t = "STRING", it = "PY_EXPR", val = strategy_name)
    variables["STRATEGY_NAME"] = strategy_name
    perf_table_name = 'Well Structure (MODELUP)'
    set_var_type (n = "perf_table_name", t = "STRING", it = "PY_EXPR", val = perf_table_name)
    variables["PERF_TABLE_NAME"] = perf_table_name
    start_date = '01.03.2009'
    set_var_type (n = "start_date", t = "STRING", it = "PY_EXPR", val = start_date)
    variables["START_DATE"] = start_date

    end_wf_item (index = 2)


    begin_wf_item (index = 3, name = "Вспомогательные переменные")
    point = T2
    set_var_type (n = "point", t = "REAL", it = "PY_EXPR", val = point)
    variables["POINT"] = point
    T3 = T2+LEN1
    set_var_type (n = "T3", t = "REAL", it = "PY_EXPR", val = T3)
    variables["T3"] = T3
    T3_2 = T2+LEN2
    set_var_type (n = "T3_2", t = "REAL", it = "PY_EXPR", val = T3_2)
    variables["T3_2"] = T3_2
    T3_3 = T2+LEN3
    set_var_type (n = "T3_3", t = "REAL", it = "PY_EXPR", val = T3_3)
    variables["T3_3"] = T3_3
    AZ_2 = BASE_AZ+DELTA_AZ_2
    set_var_type (n = "AZ_2", t = "REAL", it = "PY_EXPR", val = AZ_2)
    variables["AZ_2"] = AZ_2
    AZ_3 = BASE_AZ-DELTA_AZ_3
    set_var_type (n = "AZ_3", t = "REAL", it = "PY_EXPR", val = AZ_3)
    variables["AZ_3"] = AZ_3
    base_zen = math. degrees(math.acos(H1/LEN1))
    set_var_type (n = "base_zen", t = "REAL", it = "PY_EXPR", val = base_zen)
    variables["BASE_ZEN"] = base_zen
    base_zen2 = math. degrees(math.acos(H2/LEN2))
    set_var_type (n = "base_zen2", t = "REAL", it = "PY_EXPR", val = base_zen2)
    variables["BASE_ZEN2"] = base_zen2
    base_zen3 = math. degrees(math.acos(H3/LEN3))
    set_var_type (n = "base_zen3", t = "REAL", it = "PY_EXPR", val = base_zen3)
    variables["BASE_ZEN3"] = base_zen3
    wellname2 = wellname+":1"
    set_var_type (n = "wellname2", t = "STRING", it = "PY_EXPR", val = wellname2)
    variables["WELLNAME2"] = wellname2
    wellname3 = wellname+":2"
    set_var_type (n = "wellname3", t = "STRING", it = "PY_EXPR", val = wellname3)
    variables["WELLNAME3"] = wellname3
    branch_1 = [(AZ_1_1,ZEN_1_1),(AZ_2_1,ZEN_2_1),(AZ_3_1,ZEN_3_1)]
    set_var_type (n = "branch_1", t = "PY_EXPR", it = "PY_EXPR", val = branch_1)
    branch_2 =  [(AZ_1_2,ZEN_1_2),(AZ_2_2,ZEN_2_2),(AZ_3_2,ZEN_3_2)]
    set_var_type (n = "branch_2", t = "PY_EXPR", it = "PY_EXPR", val = branch_2)
    branch_3 = [(AZ_1_3,ZEN_1_3),(AZ_2_3,ZEN_2_3),(AZ_3_3,ZEN_3_3)]
    set_var_type (n = "branch_3", t = "PY_EXPR", it = "PY_EXPR", val = branch_3)
    branchs = {wellname:branch_1,wellname2:branch_2,wellname3:branch_3}
    set_var_type (n = "branchs", t = "PY_EXPR", it = "PY_EXPR", val = branchs)

    end_wf_item (index = 3)


    begin_wf_item (index = 4)
    wells_remove (remove_options="remove_fully",
          filter_or_select_wells_mode="selected_wells",
          well_filter=find_object (name="Import Model Well Filter(MODELUP)",
          type="WellFilter"),
          table=[{"well_name" : "test2"}])
    end_wf_item (index = 4)


    begin_wf_item (index = 5, is_custom_code = True, name = "Группировка переменных")
    branch_1 = [(AZ_1_1,ZEN_1_1),(AZ_2_1,ZEN_2_1),(AZ_3_1,ZEN_3_1)]
    branch_2 = [(AZ_1_2,ZEN_1_2),(AZ_2_2,ZEN_2_2),(AZ_3_2,ZEN_3_2)]
    branch_3 = [(AZ_1_3,ZEN_1_3),(AZ_2_3,ZEN_2_3),(AZ_3_3,ZEN_3_3)]

    well = {wellname:branch_1,wellname2:branch_2,wellname3:branch_3}
    end_wf_item (index = 5)


    begin_wf_item (index = 6)
    wells_create (well_name=resolve_variables_in_string (string_with_variables="@WELLNAME@",
          variables=variables),
          remove_existing_main_branch=False,
          branch_num=0,
          trajectory_table=[{"md" : arithmetic (expression="T2",
          variables=variables), "x" : 21176.447, "y" : 30833.427, "z" : arithmetic (expression="T2",
          variables=variables)}, {"md" : arithmetic (expression="T3",
          variables=variables), "x" : 21176.447, "y" : 30833.427, "z" : arithmetic (expression="T3",
          variables=variables)}],
          date=datetime (year=2009,
          month=3,
          day=1,
          hour=0,
          minute=0,
          second=0),
          table=None,
          perforations_table=[{"state" : "Perforation", "from" : 0, "to" : 3000, "diameter" : 0.3048, "skin" : 0, "mult" : 1, "d_factor" : 0, "depth_type" : "MD"}])
    end_wf_item (index = 6)


    begin_wf_item (index = 7)
    wells_trajectory_correction (wells=find_object (name="Wells",
          type="gt_wells_entity"),
          trajectories=find_object (name="Trajectories",
          type="Trajectories"),
          well_filter_struct=WellFilterParameters (well_filter_type="single_well",
          well_filter_selector=find_object (name="",
          type=""),
          single_well_selector=resolve_variables_in_string (string_with_variables="@WELLNAME@",
          variables=variables)),
          correction_point_type="md",
          use_current_marker_set=False,
          current_marker_set=find_object (name="Default Set",
          type="MarkerSet"),
          marker_md=find_object (name="",
          type="WellMarker"),
          md_point=arithmetic (expression="T2",
          variables=variables),
          azimuth=arithmetic (expression="base_az",
          variables=variables),
          dip=arithmetic (expression="base_zen",
          variables=variables))
    end_wf_item (index = 7)


    begin_wf_item (index = 8)
    wells_create (well_name=resolve_variables_in_string (string_with_variables="@WELLNAME@",
          variables=variables),
          remove_existing_main_branch=False,
          branch_num=0,
          trajectory_table=[{"md" : arithmetic (expression="T2",
          variables=variables), "x" : 21176.447, "y" : 30833.427, "z" : arithmetic (expression="T2",
          variables=variables)}, {"md" : arithmetic (expression="T3_2",
          variables=variables), "x" : 21176.447, "y" : 30833.427, "z" : arithmetic (expression="T3_2",
          variables=variables)}],
          date=datetime (year=2009,
          month=3,
          day=1,
          hour=0,
          minute=0,
          second=0),
          table=None,
          perforations_table=[{"state" : "Perforation", "from" : 0, "to" : 3000, "diameter" : 0.3048, "skin" : 0, "mult" : 1, "d_factor" : 0, "depth_type" : "MD"}])
    end_wf_item (index = 8)


    begin_wf_item (index = 9)
    wells_trajectory_correction (wells=find_object (name="Wells",
          type="gt_wells_entity"),
          trajectories=find_object (name="Trajectories",
          type="Trajectories"),
          well_filter_struct=WellFilterParameters (well_filter_type="single_well",
          well_filter_selector=find_object (name="",
          type=""),
          single_well_selector=resolve_variables_in_string (string_with_variables="@WELLNAME2@",
          variables=variables)),
          correction_point_type="md",
          use_current_marker_set=False,
          current_marker_set=find_object (name="Default Set",
          type="MarkerSet"),
          marker_md=find_object (name="",
          type="WellMarker"),
          md_point=arithmetic (expression="T2",
          variables=variables),
          azimuth=arithmetic (expression="AZ_2",
          variables=variables),
          dip=arithmetic (expression="base_zen",
          variables=variables))
    end_wf_item (index = 9)


    begin_wf_item (index = 10)
    wells_create (well_name=resolve_variables_in_string (string_with_variables="@WELLNAME@",
          variables=variables),
          remove_existing_main_branch=False,
          branch_num=0,
          trajectory_table=[{"md" : arithmetic (expression="T2",
          variables=variables), "x" : 21176.447, "y" : 30833.427, "z" : arithmetic (expression="T2",
          variables=variables)}, {"md" : arithmetic (expression="T3_3",
          variables=variables), "x" : 21176.447, "y" : 30833.427, "z" : arithmetic (expression="T3_3",
          variables=variables)}],
          date=datetime (year=2009,
          month=3,
          day=1,
          hour=0,
          minute=0,
          second=0),
          table=None,
          perforations_table=[{"state" : "Perforation", "from" : 0, "to" : 3000, "diameter" : 0.3048, "skin" : 0, "mult" : 1, "d_factor" : 0, "depth_type" : "MD"}])
    end_wf_item (index = 10)


    begin_wf_item (index = 11)
    wells_trajectory_correction (wells=find_object (name="Wells",
          type="gt_wells_entity"),
          trajectories=find_object (name="Trajectories",
          type="Trajectories"),
          well_filter_struct=WellFilterParameters (well_filter_type="single_well",
          well_filter_selector=find_object (name="",
          type=""),
          single_well_selector=resolve_variables_in_string (string_with_variables="@WELLNAME3@",
          variables=variables)),
          correction_point_type="md",
          use_current_marker_set=False,
          current_marker_set=find_object (name="Default Set",
          type="MarkerSet"),
          marker_md=find_object (name="",
          type="WellMarker"),
          md_point=arithmetic (expression="T2",
          variables=variables),
          azimuth=arithmetic (expression="AZ_3",
          variables=variables),
          dip=arithmetic (expression="base_zen",
          variables=variables))
    end_wf_item (index = 11)


    begin_wf_item (index = 12)
    for bran in [wellname, wellname2, wellname3]:
        pass
        set_var_type (n = "bran", t = "STRING", it = "PY_EXPR", val = bran)
        variables["BRAN"] = bran
        point = T2
        set_var_type (n = "point", t = "REAL", it = "PY_EXPR", val = point)
        variables["POINT"] = point
        begin_loop_iteration (info = "bran = " + str (bran))



        begin_wf_item (index = 13)
        for coord in branchs[bran]:
            pass
            set_var_type (n = "coord", t = "PY_EXPR", it = "PY_EXPR", val = coord)
            begin_loop_iteration (info = "coord = " + str (coord))



            begin_wf_item (index = 14, is_custom_code = True, name = "Кривим стволы")
            #print(point,T2)
            #az = np.random.triangular(-25,3,25)
            #incl = np.random.triangular(-12,2,12)
            az = coord[0]
            incl = coord[1]

            print(point, az, incl)

            wells_trajectory_correction (wells=find_object (name="Wells",
                  type="gt_wells_entity"),
                  trajectories=find_object (name="Trajectories",
                  type="Trajectories"),
                  well_filter_struct=WellFilterParameters (well_filter_type="single_well",
                  well_filter_selector=find_object (name="",
                  type=""),
                  single_well_selector=bran),
                  correction_point_type="md",
                  use_current_marker_set=False,
                  current_marker_set=find_object (name="Default Set",
                  type="MarkerSet"),
                  marker_md=find_object (name="",
                  type="WellMarker"),
                  md_point=point,
                  azimuth=az,
                  dip=incl)
            time.sleep(0.5)

            point=point+LEN1/4
            end_wf_item (index = 14)


            end_loop_iteration ()

        end_wf_item (index = 13)


        begin_wf_item (index = 16)
        wells_resample (wells=find_object (name="Wells",
              type="gt_wells_entity"),
              trajectories=find_object (name="Trajectories",
              type="Trajectories"),
              type="md",
              step=5,
              create_new_vers=False,
              ver_name="new_version",
              smooth=True,
              add_only=False,
              well_filter_struct=WellFilterParameters (well_filter_type="single_well",
              well_filter_selector=find_object (name="",
              type=""),
              single_well_selector=resolve_variables_in_string (string_with_variables="@BRAN@",
              variables=variables)))
        end_wf_item (index = 16)


        end_loop_iteration ()

    end_wf_item (index = 12)


    begin_wf_item (index = 18, is_custom_code = True, name = "Добавляем скрипт с  длиной стволов")
    sc_t = f"def __init_script__():\n    create_graph(name=\"WLEN\", type=\"well\", default_value=0, export=True)\n\n\ndef drilling_calc():\n    if not is_report_step():\n        return\n    gor_len = get_global_graph(name=\"WLEN\")\n    well = get_well_by_name(str('{wellname}'))\n    gor_len[well] = {LEN1+LEN2+LEN3}\n    export(gor_len, name=\'WLEN\')\n    script_off()"

    date = dt.strptime(start_date, '%d.%m.%Y')

    schedule_rule_add_apply_script (schedule_strategy=find_object (name=strategy_name,
          type="gt_schedule_rules_data"),
          date_time=datetime (year=date.year,
          month=date.month,
          day=date.day,
          hour=0,
          minute=0,
          second=0),
          use_rule_name=True,
          rule_name="Применить скрипт",
          file_name="python",
          function_name="drilling_calc",
          variables_table=[],
          script_text=sc_t)
    end_wf_item (index = 18)


    begin_wf_item (index = 19, is_custom_code = True, name = "Добавляем перфорации")

    perf_dict={'event':'Perforation', 
    'top_depth':0, 
    'bottom_depth':3000, 
    'depth_type':'MD', 
    'diameter_in':0.28, 
    'skin':0, 
    'comment':'added with script. Created by VAR'}

    date = dt.strptime(start_date, '%d.%m.%Y')


    perf = get_wells_structure_table_by_name (name=perf_table_name)
    #print(perf.get_date())
    n=get_well_by_name (name=wellname)
    for w in n.get_wellbores ():
    	perf.add_record (well=w, date = date)
    	st = perf.get_records (well=w, date=date)
    	for t, v in perf_dict.items():
    		st[0].set_value (type=t, value=v)

    schedule_rule_add_prod_well_limits_forecast (schedule_strategy=find_object (name=strategy_name,
          type="gt_schedule_rules_data"),
          date=datetime (year=date.year,
          month=date.month,
          day=date.day,
          hour=0,
          minute=0,
          second=0),
          use_rule_name=False,
          rule_name="Управление добывающими скважинами (прогноз)",
          params_table=[{"well" : wellname, "well_status" : "open", "control_mode" : "BHP", "oil_rate" : None, "water_rate" : None, "gas_rate" : None, "liquid_rate" : None, "resv_rate" : None, "bhp" : 50, "thp" : None, "lift" : None, "wgra" : None, "tmra" : None, "stra" : None, "satt" : None, "satp" : None, "cval" : None, "ngl" : None, "vfp_table" : 0}])
    end_wf_item (index = 19)



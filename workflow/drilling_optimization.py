#  Этот файл был сгенерирован тНавигатор v22.4-4286-gd6e009802829.
#  Copyright (C) Рок Флоу Динамикс 2005-2023.
#  Все права защищены.

# This file is MACHINE GENERATED! Do not edit.

#api_version=v0.0.83

from __main__.tnav.workflow import *
from tnav_debug_utilities import *
from datetime import datetime, timedelta


declare_workflow (workflow_name="drilling_optimization",
      variables=[{"name" : "B1", "type" : "real", "min" : 0, "max" : 500, "values" : [], "distribution_type" : "Uniform", "discrete_distr_values" : [], "discrete_distr_probabilities" : [], "initial_distribution" : [], "truncated_mean" : 0, "truncated_sigma" : 0}, {"name" : "B2", "type" : "real", "min" : 0, "max" : 500, "values" : [], "distribution_type" : "Uniform", "discrete_distr_values" : [], "discrete_distr_probabilities" : [], "initial_distribution" : [], "truncated_mean" : 0, "truncated_sigma" : 0}, {"name" : "LEN", "type" : "real", "min" : 0, "max" : 250, "values" : [], "distribution_type" : "Uniform", "discrete_distr_values" : [], "discrete_distr_probabilities" : [], "initial_distribution" : [], "truncated_mean" : 0, "truncated_sigma" : 0}, {"name" : "AZ", "type" : "real", "min" : 0, "max" : 27, "values" : [], "distribution_type" : "Uniform", "discrete_distr_values" : [], "discrete_distr_probabilities" : [], "initial_distribution" : [], "truncated_mean" : 0, "truncated_sigma" : 0}, {"name" : "DT", "type" : "real", "min" : 0, "max" : 2, "values" : [], "distribution_type" : "Uniform", "discrete_distr_values" : [], "discrete_distr_probabilities" : [], "initial_distribution" : [], "truncated_mean" : 0, "truncated_sigma" : 0}, {"name" : "DB", "type" : "real", "min" : 0, "max" : 0, "values" : [], "distribution_type" : "Uniform", "discrete_distr_values" : [], "discrete_distr_probabilities" : [], "initial_distribution" : [], "truncated_mean" : 0, "truncated_sigma" : 0}, {"name" : "SKIN", "type" : "real", "min" : 0, "max" : 0, "values" : [], "distribution_type" : "Uniform", "discrete_distr_values" : [], "discrete_distr_probabilities" : [], "initial_distribution" : [], "truncated_mean" : 0, "truncated_sigma" : 0}, {"name" : "MULT", "type" : "real", "min" : 0, "max" : 1, "values" : [], "distribution_type" : "Uniform", "discrete_distr_values" : [], "discrete_distr_probabilities" : [], "initial_distribution" : [], "truncated_mean" : 0, "truncated_sigma" : 0}])


drilling_optimization_variables = {
"B1" : 500,
"B2" : 500,
"LEN" : 250,
"AZ" : 27,
"DT" : 2,
"DB" : 0,
"SKIN" : 0,
"MULT" : 1
}

def drilling_optimization (variables = drilling_optimization_variables):
    pass
    check_launch_method ()

    B1 = variables["B1"]
    B2 = variables["B2"]
    LEN = variables["LEN"]
    AZ = variables["AZ"]
    DT = variables["DT"]
    DB = variables["DB"]
    SKIN = variables["SKIN"]
    MULT = variables["MULT"]

    begin_user_imports ()
    import pandas as pd
    end_user_imports ()

    begin_wf_item (index = 1)
    B1 = 200
    set_var_type (n = "B1", t = "REAL", it = "PY_EXPR", val = B1)
    variables["B1"] = B1
    B2 = 200
    set_var_type (n = "B2", t = "REAL", it = "PY_EXPR", val = B2)
    variables["B2"] = B2
    LEN = 250
    set_var_type (n = "LEN", t = "REAL", it = "PY_EXPR", val = LEN)
    variables["LEN"] = LEN
    AZ = 0
    set_var_type (n = "AZ", t = "REAL", it = "PY_EXPR", val = AZ)
    variables["AZ"] = AZ
    DT = 2
    set_var_type (n = "DT", t = "REAL", it = "PY_EXPR", val = DT)
    variables["DT"] = DT
    DB = -2
    set_var_type (n = "DB", t = "REAL", it = "PY_EXPR", val = DB)
    variables["DB"] = DB
    SKIN = 0
    set_var_type (n = "SKIN", t = "REAL", it = "PY_EXPR", val = SKIN)
    variables["SKIN"] = SKIN
    MULT = 1
    set_var_type (n = "MULT", t = "REAL", it = "PY_EXPR", val = MULT)
    variables["MULT"] = MULT

    end_wf_item (index = 1)


    if False:
        begin_wf_item (index = 2)
        grid_3d_geomerty_properties_calculate (mesh=find_object (name="SARAI",
              type="Grid3d"),
              use_calculate_block_sizes_dx_name=False,
              calculate_block_sizes_dx_name=find_object (name="Property1",
              type="Grid3dProperty"),
              use_calculate_block_sizes_dy_name=False,
              calculate_block_sizes_dy_name=find_object (name="Property1",
              type="Grid3dProperty"),
              use_calculate_block_sizes_dz_name=False,
              calculate_block_sizes_dz_name=find_object (name="Property1",
              type="Grid3dProperty"),
              use_calculate_depth_name=True,
              calculate_depth_name=find_object (name="depth",
              type="Grid3dProperty"),
              use_calculate_tops_name=False,
              calculate_tops_name=find_object (name="Property1",
              type="Grid3dProperty"),
              use_calculate_block_max_z_edge_name=False,
              calculate_block_max_z_edge_name=find_object (name="Property1",
              type="Grid3dProperty"))
        end_wf_item (index = 2)


    if False:
        begin_wf_item (index = 3)
        map_2d_create_by_grid_property (grid=find_object (name="SARAI",
              type="Grid3d"),
              use_user_cut=True,
              user_cut=find_object (name="Net to Gross Ratio",
              type="Grid3dProperty"),
              comparator=Comparator (rule="greater",
              value=0),
              use_user_cut_second=False,
              user_cut_second=find_object (name="ACTNUM",
              type="Grid3dProperty"),
              comparator_second=Comparator (rule="not_equals",
              value=0),
              use_zone=True,
              zone=find_object (name="zones",
              type="Grid3dProperty"),
              continuous_properties=True,
              continues_cube_and_map_table=[],
              discrete_properties=True,
              discrete_cube_and_map_table=[{"use" : True, "cube" : find_object (name="zones",
              type="Grid3dProperty"), "code_value" : 1, "map_2d" : find_object (name="TOP",
              type="Map2d"), "zone_id" : 1, "method" : "top", "smooth" : False, "blocked_wells" : None}, {"use" : True, "cube" : find_object (name="zones",
              type="Grid3dProperty"), "code_value" : 1, "map_2d" : find_object (name="BOT",
              type="Map2d"), "zone_id" : 1, "method" : "bottom", "smooth" : False, "blocked_wells" : None}],
              smoothing_radius=10,
              ignore_faults=True,
              set_na_instead_of_zero=True,
              grid_2d_source="custom",
              subdivision=3,
              grid_2d_settings=Grid2DSettings (grid_2d_settings_shown=True,
              autodetect_box=True,
              min_x=969.5529542408896,
              min_y=-3194.418601157831,
              length_x=3656.3444321935294,
              length_y=2729.5701638189403,
              margin_x=0,
              margin_y=0,
              consider_blank_nodes=False,
              autodetect_angle=True,
              angle=1.1773115870678362,
              autodetect_grid=False,
              grid_adjust_mode="step",
              step_x=100,
              step_y=100,
              counts_x=0,
              counts_y=0,
              ignore_steps=False,
              sample_object=absolute_object_name (name=None,
              typed_names=[typed_object_name (obj_name="SARAI",
              obj_type="Grid3d")]),
              autodetect_during_wf_calculation=True))
        end_wf_item (index = 3)


    if False:
        begin_wf_item (index = 4)
        horizon_calculator (result_horizon=find_object (name="Top_prod_hor",
              type="Horizon"),
              use_polygon=False,
              polygon=find_object (name="polygon",
              type="Curve3d"),
              use_initial_geometry=False,
              grid_2d_settings=Grid2DSettings (grid_2d_settings_shown=True,
              autodetect_box=True,
              min_x=953.6041422452422,
              min_y=-3130.531318250196,
              length_x=3625.485106092224,
              length_y=2712.8987298772236,
              margin_x=0,
              margin_y=0,
              consider_blank_nodes=False,
              autodetect_angle=True,
              angle=0,
              autodetect_grid=True,
              grid_adjust_mode="step",
              step_x=26.082626662533987,
              step_y=27.128987298772235,
              counts_x=0,
              counts_y=0,
              ignore_steps=False,
              sample_object=absolute_object_name (name=None,
              typed_names=[typed_object_name (obj_name="TOP",
              obj_type="Map2d")]),
              autodetect_during_wf_calculation=True),
              formula="map_2d (\"TOP\")",
              variables=variables)
        end_wf_item (index = 4)


    if False:
        begin_wf_item (index = 5, name = "BOT_HORIZON")
        horizon_calculator (result_horizon=find_object (name="Bot_prod_hor",
              type="Horizon"),
              use_polygon=False,
              polygon=find_object (name="polygon",
              type="Curve3d"),
              use_initial_geometry=False,
              grid_2d_settings=Grid2DSettings (grid_2d_settings_shown=True,
              autodetect_box=True,
              min_x=2329721.800136588,
              min_y=6159595.742698023,
              length_x=4800.000000000466,
              length_y=14800.000000000931,
              margin_x=0,
              margin_y=0,
              consider_blank_nodes=False,
              autodetect_angle=True,
              angle=-19.999999822589698,
              autodetect_grid=True,
              grid_adjust_mode="step",
              step_x=100,
              step_y=100,
              counts_x=0,
              counts_y=0,
              ignore_steps=False,
              sample_object=absolute_object_name (name=None,
              typed_names=[typed_object_name (obj_name="BOT",
              obj_type="Map2d")]),
              autodetect_during_wf_calculation=True),
              formula="map_2d (\"BOT\")",
              variables=variables)
        end_wf_item (index = 5)


    if False:
        begin_wf_item (index = 6)
        timestep_add (schedule_strategy_name=find_object (name="Development Strategy",
              type="gt_schedule_rules_data"),
              first_date=datetime (year=2023,
              month=3,
              day=24,
              hour=0,
              minute=0,
              second=0),
              last_date=datetime (year=2023,
              month=3,
              day=23,
              hour=0,
              minute=0,
              second=0),
              step_length="Custom",
              custom_step_length=1,
              custom_step_type="Second")
        end_wf_item (index = 6)


    begin_wf_item (index = 7)
    for lens in [300, 400, 500]:
        pass
        set_var_type (n = "lens", t = "PY_EXPR", it = "PY_EXPR", val = lens)
        x = lens
        set_var_type (n = "x", t = "REAL", it = "PY_EXPR", val = x)
        variables["X"] = x
        y = lens
        set_var_type (n = "y", t = "REAL", it = "PY_EXPR", val = y)
        variables["Y"] = y
        mod_name = 'mod_'+str(lens)
        set_var_type (n = "mod_name", t = "PY_EXPR", it = "PY_EXPR", val = mod_name)
        begin_loop_iteration (info = "lens = " + str (lens))



        if False:
            begin_wf_item (index = 8, is_custom_code = True)
            print(mod_name)
            end_wf_item (index = 8)


        begin_wf_item (index = 9)
        well_placement (pattern="Пятиточечная с горизонт. доб. скважиной",
              curve=find_object (name="target",
              type="Curve3d"),
              development_strategy=find_object (name="SARAI_FORECAST",
              type="gt_schedule_rules_data"),
              structure_table=find_object (name="forecast",
              type="gt_wells_events_data"),
              grid=find_object (name="SARAI",
              type="Grid3d"),
              well_filter=find_object (name="Расстановка скважин",
              type="WellFilter"),
              define_drilling_rig=False,
              vars_table=[{"Variable" : "B1", "Value" : arithmetic (expression="x",
              variables=variables)}, {"Variable" : "B2", "Value" : arithmetic (expression="y",
              variables=variables)}, {"Variable" : "LEN", "Value" : arithmetic (expression="LEN",
              variables=variables)}, {"Variable" : "AZ", "Value" : arithmetic (expression="AZ",
              variables=variables)}, {"Variable" : "DT", "Value" : arithmetic (expression="DT",
              variables=variables)}, {"Variable" : "DB", "Value" : arithmetic (expression="DB",
              variables=variables)}, {"Variable" : "SKIN", "Value" : arithmetic (expression="SKIN",
              variables=variables)}, {"Variable" : "MULT", "Value" : arithmetic (expression="MULT",
              variables=variables)}])
        end_wf_item (index = 9)


        begin_wf_item (index = 10)
        open_or_reload_dynamic_model (use_model=True,
              model=find_object (name="SARAI_FORECAST1",
              type="Model_ex"),
              result_name="SARAI_FORECAST1")
        end_wf_item (index = 10)


        begin_wf_item (index = 11)
        run_dynamic_model_calculations (is_go_to_step=True,
              go_to_step_number=388)
        end_wf_item (index = 11)


        begin_wf_item (index = 12, name = "Анализ результатов ГДМ")
        workflow_folder ()
        if True:
            pass



            if False:
                begin_wf_item (index = 13, name = "Анализ скважин")
                run_graph_calculator (gc_code="import pandas as pd\nimport os\nimport pickle\nimport oily_report as olr\n\n\nolr.create_report_dir(path=get_project_folder())\nlast_prod_period = get_all_timesteps()[-12:-1]\ncells = {}\ntop_near_w = 5\ncell_dim = 77\n\n# формирование фрейма данных по\nfor w in get_all_wells():\n    try:\n        con = w.connections[0]\n        cells[w.name] = {\'i\': con.i,\n                         \'j\': con.j,\n                         \'opr\': float(wopr[w].avg(dates=last_prod_period)),\n                         \'lpr\': float(wlpr[w].avg(dates=last_prod_period)),\n                         }\n    except:\n        print(f\'Скважина {w.name} без перфораций\')\nwells = pd.DataFrame(cells)\nwells = wells.T.reset_index()\nwells.columns = [\'well\', \'x\', \'y\', \'oil\', \'liq\']\n\n\nprint(wells)\n\nfor i, j in wells.groupby(by=\'well\'):\n    x = float(wells.loc[wells[\'well\'] == i, \'x\'].values)\n    y = float(wells.loc[wells[\'well\'] == i, \'y\'].values)\n    wells[\'sum\'] = ((wells[\'x\']-x)**2+(wells[\'y\']-y)**2)**0.5\n    wells.loc[wells[\'well\'] == i,\n              \'Расстояние\'] = wells[(wells[\'oil\'] > 0) & (wells[\'sum\'] > 0)][\'sum\'].min()*cell_dim\n    a = wells[(wells[\'oil\'] > 0) & (wells[\'sum\'] > 0)].sort_values(by=\'sum\', ascending=True)[\n        \'well\'].head(5).to_list()\n\n    nearest_wells = \', \'.join([str(elem) for elem in a])\n    wells.loc[wells[\'well\'] == i,\n              \'Ближайшие скважины\'] = nearest_wells\n    wells.loc[wells[\'well\'] == i, \'oil_near\'] = wells[wells[\'oil\'] > 0].sort_values(\n        by=\'sum\', ascending=True)[\'oil\'].head(top_near_w).mean()\n    wells.loc[wells[\'well\'] == i, \'liq_near\'] = wells[wells[\'oil\'] > 0].sort_values(\n        by=\'sum\', ascending=True)[\'liq\'].head(top_near_w).mean()\n\nwith open(\'wells_risk.pickle\', \'wb\') as file:\n    pickle.dump(wells, file)\n# print(os.getcwd())\n#",
                      font="Consolas,8,-1,5,50,0,0,0,0,0",
                      models=["Result_1"],
                      variables=variables)
                end_wf_item (index = 13)


            begin_wf_item (index = 14, name = "Экономика по скважинам")
            run_graph_calculator (gc_code="# Automaticaly recalculate=true\n# Single model=false\n# пишите здесь ваш код\n# пишите здесь ваш кодdate=\"01.07.2019\"\n##################################################\n################ Script Section ##################\n##################################################\n\nimport datetime\nimport oily_report as olr\nimport pandas as pd\nimport pickle\n\nolr.create_report_dir(path=get_project_folder())\n\n\n# исходные данные для проведения экономического расчета\ndepreciation_year = 8  # year\nimushes_tax = 2.2  # %\nprib_tax = 20  # %\noil_price = 17259  # rub/t.tonn\nopex_oil = 29.29  # rub/tonn\nopex_liq = 73.25  # rub/tonn\nndpi = 9980\ncapex = 31637  # t.rub\nk_disk = 10  # t.rub\nm = get_model_by_name(\'SARAI_FORECAST1\')\nprefix = \'G\'\n\nproject_wells = [w for w in get_all_wells() if w.name.startswith(prefix)]\n\n\n# показатели для расчета\noil_prod_gr = graph(type=\'well\', default_value=0)\nliq_prod_gr = graph(type=\'well\', default_value=0)\ncash_gr = graph(type=\'well\', default_value=0)\ntot_opex_gr = graph(type=\'well\', default_value=0)\ndeprec_gr = graph(type=\'well\', default_value=0)\nval_profit_gr = graph(type=\'well\', default_value=0)\nimushes_tax_gr = graph(type=\'well\', default_value=0)\nprib_tax_gr = graph(type=\'well\', default_value=0)\ndry_prib_gr = graph(type=\'well\', default_value=0)\nsaldo_cashflow_gr = graph(type=\'well\', default_value=0)\ndisk_saldo_gr = graph(type=\'well\', default_value=0)\ndisk_prof_gr = graph(type=\'well\', default_value=0)\ndisk_losses_gr = graph(type=\'well\', default_value=0)\nnpv_gr = graph(type=\'well\', default_value=0)\niddz_gr = graph(type=\'well\', default_value=0)\ntemp = graph(type=\'well\', default_value=0)\n\n\nstart = 2021  # дата начала прогноза\nend = 2025  # дата окончания прогноза\nden = 1\n\nolr.create_report_dir(path=get_project_folder())\n\n# Блок для анализа продолжательности прогноза\ncolls = [(x.to_datetime().year-start) for x in get_all_timesteps()]\ncolls = max(colls)\nprint(colls)\n\ndepreciation = [0]*colls\nfor i in range(depreciation_year):\n    depreciation[i] = capex/depreciation_year\n\nfor i in range(depreciation_year):\n    depreciation[i] = capex/depreciation_year\n\n\nsteps = []\nfor t in get_all_timesteps():\n    if t.to_datetime().day == 1 and t.to_datetime().month == 1\\\n            and t.to_datetime().year >= start:\n        steps.append(t)\n\n\n# Блок для анализа даты ввода скважины\ndrill_date = {}\n\nfor w in get_all_wells():\n    for t in get_all_timesteps():\n        if wstat[m, w, t] == 1 or wstat[m, w, t] == 2:\n            drill_date[w.name] = t.to_datetime()\n            break\n        else:\n            drill_date[w.name] = \'dont_work\'\n# print(drill_date)\n\ndf = []\n# Блок расчета и вывода данных годовой добыче нефти и жидкости по скважинам\nfor w in project_wells:\n    amort = (a for a in depreciation)\n    diskont = ((1/(1+k_disk/100))**x for x in range(colls))\n    for t in steps:\n        if t.to_datetime().year == start:\n            oil_old = float(wopt[m, w, t]/1000)\n            liq_old = float(wlpt[m, w, t]/1000)\n        else:\n            a = next(amort)\n            k = next(diskont)\n            year_oil = float(wopt[m, w, t]/1000)-oil_old\n            year_liq = float(wlpt[m, w, t]/1000)-liq_old\n            cash_gr[w, t] = year_oil*oil_price\n            tot_opex_gr[w, t] = (year_oil*(ndpi+opex_oil) +\n                                 (year_liq*opex_liq))*(-1)\n            deprec_gr[w, t] = -a\n            val_profit_gr[w, t] = cash_gr[w, t] + \\\n                tot_opex_gr[w, t]+deprec_gr[w, t]\n            imushes_tax_gr[w] = (-1)*(2*capex+shift_t(graph=cum_sum(temp[w]),\n                                                      shift=12, default=0)+deprec_gr[w])/2*imushes_tax/100\n            temp[w, t] = -2*a\n            prib_tax_gr[w, t] = -prib_tax/100.0 * \\\n                (val_profit_gr[w, t]+imushes_tax_gr[w, t])\n            dry_prib_gr[w, t] = val_profit_gr[w, t] + \\\n                imushes_tax_gr[w, t]+prib_tax_gr[w, t]\n            saldo_cashflow_gr[w, t] = -capex - deprec_gr[w, t]+dry_prib_gr[w, t] \\\n                if t.to_datetime().year == start+1 \\\n                else (-1)*deprec_gr[w, t]+dry_prib_gr[w, t]\n            disk_saldo_gr[w, t] = k*saldo_cashflow_gr[w, t]\n            disk_prof_gr[w, t] = cash_gr[w, t]*k\n            disk_losses_gr[w, t] = (-capex + tot_opex_gr[w, t]+imushes_tax_gr[w, t]+prib_tax_gr[w, t])*k \\\n                if t.to_datetime().year == start+1 \\\n                else (tot_opex_gr[w, t]+imushes_tax_gr[w, t]+prib_tax_gr[w, t])*k\n            oil_prod_gr[w, t] = year_oil\n            liq_prod_gr[w, t] = year_liq\n            npv_gr[w] = cum_sum(disk_saldo_gr[w])\n            iddz_gr[w] = (-1)*cum_sum(disk_prof_gr[w]) / \\\n                cum_sum(disk_losses_gr[w])\n            oil_old = float(wopt[m, w, t]/1000)\n            liq_old = float(wlpt[m, w, t]/1000)\n    df.append([w.name, drill_date[w.name], round(float(wopt[w, steps[-1]]), 0),\n                  round(float(npv_gr[w, steps[-1]]), 0), round(float(iddz_gr[w, steps[-1]]), 2)])\n    print(f\' скважина {w.name} ЧДД {round(float(npv_gr[w, steps[-1]]),0)} \\\n                ИДДЗ {round(float(iddz_gr[w, steps[-1]]),2)}\')\n\nexport(oil_prod_gr, name=\'Year_oil_production\', units=\'liquid_surface_volume\')\nexport(liq_prod_gr, name=\'Year_liq_production\', units=\'liquid_surface_volume\')\nexport(cash_gr, name=\'Выручка\', units=\'diametr\')\nexport(tot_opex_gr, name=\'Затраты на добычу\',\n       units=\'diametr\')\nexport(deprec_gr, name=\'Амортизация\', units=\'diametr\')\nexport(val_profit_gr, name=\'Валовая прибыль\', units=\'diametr\')\nexport(imushes_tax_gr, name=\'Имущественный налог\', units=\'diametr\')\nexport(prib_tax_gr, name=\'Налог на прибыль\', units=\'diametr\')\nexport(dry_prib_gr, name=\'Чистая прибыль\', units=\'diametr\')\nexport(saldo_cashflow_gr, name=\'Сальдо суммарного потока\', units=\'diametr\')\nexport(npv_gr, name=\'ЧДД\', units=\'diametr\')\nexport(disk_prof_gr, name=\'Дисконтированные притоки\', units=\'diametr\')\nexport(disk_losses_gr, name=\'Дисконтированные оттоки\', units=\'diametr\')\nexport(iddz_gr, name=\'ИДДЗ\', units=\'diametr\')\n\n\ndf = pd.DataFrame(\n    df, columns=[\'скважина\', \'Дата_бурения\', \'Накопленная добыча\', \'ЧДД\', \'ИДДЗ\'])\nwith open(\'wells_economic.pickle\', \'wb\') as file:\n    pickle.dump(df, file)",
                  font="Consolas,8,-1,5,50,0,0,0,0,0",
                  models=["SARAI_FORECAST1"],
                  variables=variables)
            end_wf_item (index = 14)



        end_wf_item (index = 12)


        begin_wf_item (index = 16, is_custom_code = True, name = "Экспорт таблиц")
        import pandas as pd
        import oily_report as olr
        import pickle
        import os

        olr.create_report_dir(path=get_project_folder())

        print(os.getcwd())
        with open('wells_risk.pickle', 'rb') as file:
            df = pickle.load(file)
        with open('wells_economic.pickle', 'rb') as file:
            df2 = pickle.load(file)

        def df_to_table(df, name='from_df'):
            create_table(name=name, overwrite_existing=True)
            print(df.shape)
            rows, cols = df.shape
            get_table_by_name(name=name).set_size(
                r_count=rows, c_count=cols)
            for n, col_name in enumerate(df.columns):
                get_table_by_name(name=name).set_column_header (column=n+1, text=col_name)
            for row_n, row in enumerate(df.iterrows()):
                for col_n, col in enumerate(row[1]):
                    print(f'row {row_n+1} col {col_n+1} данные {df.iloc[row_n,col_n]}')#, col)
                    get_table_by_name(name=name).set_data(row=row_n+1, column=col_n+1, data=str(df.iloc[row_n,col_n]))


        df_to_table(df, name = 'risk')
        df_to_table(df2, name='economic')
        #df2.loc[df2['ИДДЗ']<1.1, 'скважина'].values()
        names = list(df2.loc[df2['ИДДЗ']<0.9, 'скважина'].values)



        wells = [w.name for w in get_all_wells ()]

        for w in wells:
        	if w in names:
        		print(w)
        		delete_well (name=w)
        end_wf_item (index = 16)


        end_loop_iteration ()

    end_wf_item (index = 7)


    if False:
        begin_wf_item (index = 18, is_custom_code = True, name = "Удаление скважин")
        wells = [w.name for w in get_all_wells ()]

        for w in wells:
        	if w.startswith('G'):
        		print(w)
        		delete_well (name=w)
        end_wf_item (index = 18)



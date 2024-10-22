#  Этот файл был сгенерирован тНавигатор v24.2-4325-ga170e3ea.
#  Copyright (C) Рок Флоу Динамикс 2005-2024.
#  Все права защищены.

# This file is MACHINE GENERATED! Do not edit.

#api_version=v0_0_145

from __main__.tnav.workflow import *
from tnav_debug_utilities import *
from datetime import datetime, timedelta


declare_workflow (workflow_name="prognoz_maps",
      variables=[])


prognoz_maps_variables = {

}

def prognoz_maps (variables = prognoz_maps_variables):
    pass
    check_launch_method ()


    begin_user_imports ()
    end_user_imports ()

    if False:
        begin_wf_item (index = 1)
        create_screenshot (window_name="Гео_карты",
              extension="jpg",
              filename="../../../Документы/UNGKM/UNGKM_RES_ENG2/UNGKM_RES_ENG2.snf/Screenshots/2D_3.JPG",
              pagesize="A3",
              orientation="Portrait",
              layout_type="Best Fit",
              units="pixels",
              width=1920,
              height=1200,
              add_date_to_filename=False,
              add_date_to_filename_method="add_date_from_time_step",
              create_screenshots_pack=False,
              first_step_number=0,
              last_step_number=190,
              add_step_number_to_filename=True,
              date_format="DD-MM-YYYY",
              font="Noto Sans,24,-1,5,75,0,1,0,0,0,Bold",
              caption_position="Above",
              caption_alignment="Center",
              use_default_name=False,
              default_name=None,
              caption="Выкопировка карты")
        end_wf_item (index = 1)


    if False:
        begin_wf_item (index = 2)
        grid_property_create_by_zones (mesh=find_object (name="Grid_up_short_alt",
              type="Grid3d"),
              result_grid_property=find_object (name="object_zone",
              type="Grid3dProperty"),
              zones_table=[{"use" : True, "zone_string" : "1", "zone_code" : 1, "zone_k1" : 1, "zone_k2" : 68}])
        end_wf_item (index = 2)


    begin_wf_item (index = 3)
    grid_property_calculator (mesh=find_object (name="Results (FORECAST: UNGKM_AD_restart)",
          type="gt_ecl_grid_3d_data"),
          result_grid_property=find_object (name="gas_filter",
          type="Grid3dProperty"),
          discrete_output_new="discrete",
          use_filter=False,
          user_cut_for_filter=find_object (name="DOIL",
          type="Grid3dProperty"),
          filter_comparator=Comparator (rule="not_equals",
          value=0),
          formula="result_property (\"Gas Saturation\")>0",
          variables=variables)
    end_wf_item (index = 3)


    if False:
        begin_wf_item (index = 4)
        grid_3d_geomerty_properties_calculate (mesh=find_object (name="Grid_up_short_alt",
              type="Grid3d"),
              use_calculate_block_sizes_dx_name=False,
              calculate_block_sizes_dx_name=find_object (name="Property1",
              type="Grid3dProperty"),
              use_calculate_block_sizes_dy_name=False,
              calculate_block_sizes_dy_name=find_object (name="Property1",
              type="Grid3dProperty"),
              use_calculate_block_sizes_dz_name=True,
              calculate_block_sizes_dz_name=find_object (name="DZ",
              type="Grid3dProperty"),
              use_calculate_depth_name=False,
              calculate_depth_name=find_object (name="Property1",
              type="Grid3dProperty"),
              use_calculate_tops_name=False,
              calculate_tops_name=find_object (name="Property1",
              type="Grid3dProperty"),
              use_calculate_block_max_z_edge_name=False,
              calculate_block_max_z_edge_name=find_object (name="Property1",
              type="Grid3dProperty"))
        end_wf_item (index = 4)


    begin_wf_item (index = 5)
    folder_create (parent_folder=absolute_object_name (name=None,
          typed_names=[typed_object_name (obj_name="2D-Maps",
          obj_type="TypedFolder")]),
          folder_name="prognoz_maps",
          ignore_if_exists=True)
    end_wf_item (index = 5)


    if False:
        begin_wf_item (index = 6)
        folder_create (parent_folder=absolute_object_name (name=None,
              typed_names=[typed_object_name (obj_name="2D-Maps",
              obj_type="TypedFolder")]),
              folder_name="res_eng_maps",
              ignore_if_exists=False)
        end_wf_item (index = 6)


    begin_wf_item (index = 7)
    set_local_vars_table ()
    objects = ["Ach3", "Arg1", "Ach4", "Arg2", "Ach51", "Arg3", "Ach523", "Ach523-Bazhen"]
    set_var_type (n = "objects", t = "PY_EXPR", it = "STRING_VECTOR", val = objects)

    end_wf_item (index = 7)


    begin_wf_item (index = 8)
    date_dict = {}
    set_var_type (n = "date_dict", t = "PY_EXPR", it = "PY_EXPR", val = date_dict)

    end_wf_item (index = 8)


    begin_wf_item (index = 9, is_custom_code = True, name = "Создаем ключевые даты")

    for n, t in enumerate(get_all_timesteps ()):
    	if t.month==1 and t.day==1 and t.year>2023:
    		date_dict[t]=n
    		print(n, t)
    end_wf_item (index = 9)


    begin_wf_item (index = 10)
    for date in date_dict.keys():
        pass
        set_var_type (n = "date", t = "PY_EXPR", it = "PY_EXPR", val = date)
        begin_loop_iteration (info = "date = " + str (date))



        begin_wf_item (index = 11, is_custom_code = True)
        print(date)
        switch_time_step (step_number=date_dict[date])
        end_wf_item (index = 11)


        begin_wf_item (index = 12)
        for obj in range(0,len(objects)):
            pass
            set_var_type (n = "obj", t = "INTEGER", it = "PY_EXPR", val = obj)
            variables["OBJ"] = obj
            OBJ_NAME = objects[obj]
            set_var_type (n = "OBJ_NAME", t = "STRING", it = "PY_EXPR", val = OBJ_NAME)
            variables["OBJ_NAME"] = OBJ_NAME
            obj_num = obj+1
            set_var_type (n = "obj_num", t = "INTEGER", it = "PY_EXPR", val = obj_num)
            variables["OBJ_NUM"] = obj_num
            PORO_MAP = "Пористость " + OBJ_NAME
            set_var_type (n = "PORO_MAP", t = "STRING", it = "PY_EXPR", val = PORO_MAP)
            variables["PORO_MAP"] = PORO_MAP
            Heff_MAP = "Эффективная толщина" + OBJ_NAME
            set_var_type (n = "Heff_MAP", t = "STRING", it = "PY_EXPR", val = Heff_MAP)
            variables["HEFF_MAP"] = Heff_MAP
            KGL_MAP = "KGL_" + OBJ_NAME
            set_var_type (n = "KGL_MAP", t = "STRING", it = "PY_EXPR", val = KGL_MAP)
            variables["KGL_MAP"] = KGL_MAP
            PERMX_MAP = "Проницаемость " + OBJ_NAME
            set_var_type (n = "PERMX_MAP", t = "STRING", it = "PY_EXPR", val = PERMX_MAP)
            variables["PERMX_MAP"] = PERMX_MAP
            Sgas = "Насыщение_газом_" + OBJ_NAME
            set_var_type (n = "Sgas", t = "STRING", it = "PY_EXPR", val = Sgas)
            variables["SGAS"] = Sgas
            PS = "Содержание С5+_" + OBJ_NAME
            set_var_type (n = "PS", t = "STRING", it = "PY_EXPR", val = PS)
            variables["PS"] = PS
            Perm_mult = "Множители_прониц_" + OBJ_NAME
            set_var_type (n = "Perm_mult", t = "STRING", it = "PY_EXPR", val = Perm_mult)
            variables["PERM_MULT"] = Perm_mult
            PRESS = "Изобары пласта_" + OBJ_NAME+"_"+date.strftime("%d.%m.%Y")
            set_var_type (n = "PRESS", t = "STRING", it = "PY_EXPR", val = PRESS)
            variables["PRESS"] = PRESS
            begin_loop_iteration (info = "obj = " + str (obj))



            if obj in [0,2,4,6]:
                if_statement_contents ()
                begin_wf_item (index = 13)


                begin_wf_item (index = 14)
                map_2d_create_by_grid_property (grid=find_object (name="Results (FORECAST: UNGKM_AD_restart)",
                      type="gt_ecl_grid_3d_data"),
                      use_user_cut=True,
                      user_cut=find_object (name="Equilibration Regions (INIT)",
                      type="gt_ecl_cube_3d_data"),
                      comparator=Comparator (rule="equals",
                      value=arithmetic (expression="OBJ_NUM",
                      variables=variables)),
                      use_user_cut_second=True,
                      user_cut_second=find_object (name="gas_filter",
                      type="Grid3dProperty"),
                      comparator_second=Comparator (rule="greater",
                      value=0),
                      use_zone=False,
                      zone=find_object (name="Facies_SGS",
                      type="Grid3dProperty"),
                      continuous_properties=True,
                      continues_cube_and_map_table=[{"use" : True, "cube" : find_object (name="Pressure",
                      type="gt_ecl_cube_3d_data"), "map_2d" : find_object (name=resolve_variables_in_string (string_with_variables="@PRESS@",
                      variables=variables),
                      type="Map2d"), "zone_id" : 0, "method" : "average", "smooth" : True, "blocked_wells" : None}],
                      discrete_properties=False,
                      discrete_cube_and_map_table=[],
                      smoothing_radius=100,
                      ignore_faults=False,
                      set_na_instead_of_zero=False,
                      compatibility_options=False,
                      set_na_outside_filter=False,
                      grid_2d_source="custom",
                      add_half_cell_offset=False,
                      subdivision=3,
                      grid_2d_settings=Grid2DSettings (grid_2d_settings_shown=True,
                      autodetect_box=False,
                      min_x=573689.9113854518,
                      min_y=7351605.6597503679,
                      length_x=29142.25841935794,
                      length_y=61384.94747591857,
                      margin_x=0,
                      margin_y=0,
                      consider_blank_nodes=False,
                      autodetect_angle=False,
                      angle=6.679886063221846,
                      autodetect_grid=False,
                      grid_adjust_mode="step",
                      step_x=100,
                      step_y=100,
                      counts_x=0,
                      counts_y=0,
                      sample_object=absolute_object_name (name=None,
                      typed_names=[typed_object_name (obj_name="Cuted",
                      obj_type="Grid3d")]),
                      autodetect_during_wf_calculation=True))
                end_wf_item (index = 14)


                if False:
                    begin_wf_item (index = 15)
                    object_move (object=absolute_object_name (name=None,
                          typed_names=[typed_object_name (obj_name=resolve_variables_in_string (string_with_variables="@PORO_MAP@",
                          variables=variables),
                          obj_type="Map2d")]),
                          destination_folder=absolute_object_name (name=None,
                          typed_names=[typed_object_name (obj_name="2D-Maps",
                          obj_type="TypedFolder"), typed_object_name (obj_name="res_eng_maps",
                          obj_type="UserFolder")]),
                          ignore_if_not_exists=False)
                    end_wf_item (index = 15)


                if False:
                    begin_wf_item (index = 16)
                    object_move (object=absolute_object_name (name=None,
                          typed_names=[typed_object_name (obj_name=resolve_variables_in_string (string_with_variables="@HEFF_MAP@",
                          variables=variables),
                          obj_type="Map2d")]),
                          destination_folder=absolute_object_name (name=None,
                          typed_names=[typed_object_name (obj_name="2D-Maps",
                          obj_type="TypedFolder"), typed_object_name (obj_name="res_eng_maps",
                          obj_type="UserFolder")]),
                          ignore_if_not_exists=False)
                    end_wf_item (index = 16)


                if False:
                    begin_wf_item (index = 17)
                    object_move (object=absolute_object_name (name=None,
                          typed_names=[typed_object_name (obj_name=resolve_variables_in_string (string_with_variables="@PERMX_MAP@",
                          variables=variables),
                          obj_type="Map2d")]),
                          destination_folder=absolute_object_name (name=None,
                          typed_names=[typed_object_name (obj_name="2D-Maps",
                          obj_type="TypedFolder"), typed_object_name (obj_name="res_eng_maps",
                          obj_type="UserFolder")]),
                          ignore_if_not_exists=False)
                    end_wf_item (index = 17)


                if False:
                    begin_wf_item (index = 18)
                    object_move (object=absolute_object_name (name=None,
                          typed_names=[typed_object_name (obj_name=resolve_variables_in_string (string_with_variables="@SGAS@",
                          variables=variables),
                          obj_type="Map2d")]),
                          destination_folder=absolute_object_name (name=None,
                          typed_names=[typed_object_name (obj_name="2D-Maps",
                          obj_type="TypedFolder"), typed_object_name (obj_name="res_eng_maps",
                          obj_type="UserFolder")]),
                          ignore_if_not_exists=False)
                    end_wf_item (index = 18)


                if False:
                    begin_wf_item (index = 19)
                    object_move (object=absolute_object_name (name=None,
                          typed_names=[typed_object_name (obj_name=resolve_variables_in_string (string_with_variables="@PS@",
                          variables=variables),
                          obj_type="Map2d")]),
                          destination_folder=absolute_object_name (name=None,
                          typed_names=[typed_object_name (obj_name="2D-Maps",
                          obj_type="TypedFolder"), typed_object_name (obj_name="res_eng_maps",
                          obj_type="UserFolder")]),
                          ignore_if_not_exists=False)
                    end_wf_item (index = 19)


                begin_wf_item (index = 20)
                object_move (object=absolute_object_name (name=None,
                      typed_names=[typed_object_name (obj_name=resolve_variables_in_string (string_with_variables="@PRESS@",
                      variables=variables),
                      obj_type="Map2d")]),
                      destination_folder=absolute_object_name (name=None,
                      typed_names=[typed_object_name (obj_name="2D-Maps",
                      obj_type="TypedFolder"), typed_object_name (obj_name="prognoz_maps",
                      obj_type="UserFolder")]),
                      ignore_if_not_exists=False)
                end_wf_item (index = 20)


                if False:
                    begin_wf_item (index = 21)
                    object_move (object=absolute_object_name (name=None,
                          typed_names=[typed_object_name (obj_name=resolve_variables_in_string (string_with_variables="@Perm_mult@",
                          variables=variables),
                          obj_type="Map2d")]),
                          destination_folder=absolute_object_name (name=None,
                          typed_names=[typed_object_name (obj_name="2D-Maps",
                          obj_type="TypedFolder"), typed_object_name (obj_name="res_eng_maps",
                          obj_type="UserFolder")]),
                          ignore_if_not_exists=False)
                    end_wf_item (index = 21)


                end_wf_item (index = 13)


            end_loop_iteration ()

        end_wf_item (index = 12)


        end_loop_iteration ()

    end_wf_item (index = 10)


    if False:
        begin_wf_item (index = 25, is_custom_code = True, name = "выгрузка карт в папку")
        maps = get_all_maps_2d_in_folder (folder='prognoz_maps', recursive=False)

        for map in maps:
        	print(map.name)
        	select_geometry_object (window_name="Гео_карты",\
              action="show",\
              object=absolute_object_name (name=None,\
              typed_names=[typed_object_name (obj_name=map.name,\
              obj_type="Map2d")])) 
        	create_screenshot (window_name="Гео_карты",\
              extension="jpg",\
              filename=f"/home/albert.vafin/My_documents/UNGKM/UNGKM_RES_ENG2/UNGKM_RES_ENG2.snf/Screenshots/{map.name}.jpg",\
              pagesize="A3",\
              orientation="Portrait",\
              layout_type="Best Fit",\
              units="pixels",\
              width=1920,\
              height=1200,\
              add_date_to_filename=False,\
              add_date_to_filename_method="add_date_from_time_step",\
              create_screenshots_pack=False,\
              first_step_number=0,\
              last_step_number=1181,\
              add_step_number_to_filename=True,\
              date_format="DD-MM-YYYY",\
              font="Noto Sans,24,-1,5,75,0,1,0,0,0,Bold",\
              caption_position="Above",\
              caption_alignment="Center",\
              use_default_name=False,\
              default_name=None,\
              caption=f"Выкопировка карты {map.name.lower()}")
        	select_geometry_object (window_name="Гео_карты",\
              action="hide",\
              object=absolute_object_name (name=None,\
              typed_names=[typed_object_name (obj_name=map.name,\
              obj_type="Map2d")])) 
        end_wf_item (index = 25)


    if False:
        begin_wf_item (index = 26)
        map_2d_create_by_grid_property (grid=find_object (name="SHORT_AREA (Dynamic Model)",
              type="gt_tnav_grid_3d_data"),
              use_user_cut=False,
              user_cut=find_object (name="SGAS",
              type="gt_tnav_cube_3d_data"),
              comparator=Comparator (rule="greater",
              value=0),
              use_user_cut_second=True,
              user_cut_second=find_object (name="SGAS",
              type="gt_tnav_cube_3d_data"),
              comparator_second=Comparator (rule="greater",
              value=0),
              use_zone=False,
              zone=find_object (name="Facies_SGS",
              type="Grid3dProperty"),
              continuous_properties=True,
              continues_cube_and_map_table=[{"use" : True, "cube" : find_object (name="CALC_PRESSURE",
              type="gt_tnav_cube_3d_data"), "map_2d" : find_object (name=" Изобары",
              type="Map2d"), "zone_id" : 0, "method" : "average", "smooth" : True, "blocked_wells" : None}],
              discrete_properties=False,
              discrete_cube_and_map_table=[],
              smoothing_radius=100,
              ignore_faults=False,
              set_na_instead_of_zero=False,
              compatibility_options=False,
              set_na_outside_filter=False,
              grid_2d_source="custom",
              add_half_cell_offset=False,
              subdivision=3,
              grid_2d_settings=Grid2DSettings (grid_2d_settings_shown=True,
              autodetect_box=False,
              min_x=573689.9113854518,
              min_y=7351605.6597503679,
              length_x=29142.25841935794,
              length_y=61384.94747591857,
              margin_x=0,
              margin_y=0,
              consider_blank_nodes=False,
              autodetect_angle=False,
              angle=6.679886063221846,
              autodetect_grid=False,
              grid_adjust_mode="step",
              step_x=100,
              step_y=100,
              counts_x=0,
              counts_y=0,
              sample_object=absolute_object_name (name=None,
              typed_names=[typed_object_name (obj_name="Cuted",
              obj_type="Grid3d")]),
              autodetect_during_wf_calculation=True))
        end_wf_item (index = 26)



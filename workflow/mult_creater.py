#  Этот файл был сгенерирован тНавигатор v22.4-3544-g24519bd52cae.
#  Copyright (C) Рок Флоу Динамикс 2005-2023.
#  Все права защищены.

# This file is MACHINE GENERATED! Do not edit.

#api_version=v0.0.80

from __main__.tnav.workflow import *
from tnav_debug_utilities import *
from datetime import datetime, timedelta


declare_workflow (workflow_name="mult_creater",
      variables=[])


mult_creater_variables = {

}

def mult_creater (variables = mult_creater_variables):
    pass
    check_launch_method ()


    begin_user_imports ()
    end_user_imports ()

    begin_wf_item (index = 1, name = "Блок для формирования куба мультов")
    comment_text ("""



""")
    end_wf_item (index = 1)


    begin_wf_item (index = 2)
    MUTL_TABLE_NAME = 'MULT_OFP'
    set_var_type (n = "MUTL_TABLE_NAME", t = "STRING", it = "PY_EXPR", val = MUTL_TABLE_NAME)
    variables["MUTL_TABLE_NAME"] = MUTL_TABLE_NAME

    end_wf_item (index = 2)


    if well_log_exists(name=MUTL_TABLE_NAME):
        if_statement_contents ()
        begin_wf_item (index = 3)


        begin_wf_item (index = 4)
        object_delete (object=absolute_object_name (name=None,
              typed_names=[typed_object_name (obj_name=resolve_variables_in_string (string_with_variables="@MUTL_TABLE_NAME@",
              variables=variables),
              obj_type="WellLog")]),
              ignore_if_not_exists=False)
        end_wf_item (index = 4)


        end_wf_item (index = 3)


    if False:
        begin_wf_item (index = 6)
        wells_log_remove_by_well (wells=find_object (name="Wells",
              type="gt_wells_entity"),
              trajectories=find_object (name="Trajectories",
              type="Trajectories"),
              log=find_object (name=resolve_variables_in_string (string_with_variables="@MUTL_TABLE_NAME@",
              variables=variables),
              type="WellLog"),
              use_well_filter=False,
              result_well_filter=find_object (name="Well Filter 1",
              type="WellFilter"))
        end_wf_item (index = 6)


    begin_wf_item (index = 7, is_custom_code = True, name = "Create_melted_df")
    import pandas as pd
    import os

    os.chdir(get_project_folder ())
    df = pd.DataFrame(get_table_by_name (name=MUTL_TABLE_NAME).get_all_data())
    df.columns = ['WELL', "ZONE", "TOP", "BOT", "MULT"]
    df.drop(labels = [0],axis = 0, inplace=True)
    df=df.melt(["WELL","ZONE","MULT"]).sort_values(by=['WELL','ZONE','value'])
    df.replace('-', '-999.25', inplace=True)
    print(df)
    df.to_csv(f'{MUTL_TABLE_NAME}.txt')
    end_wf_item (index = 7)


    if False:
        begin_wf_item (index = 8, name = "DONT_WORK!")
        for B in range(2,get_table_by_name (name="MULT").get_row_count (),1):
            pass
            set_var_type (n = "B", t = "INTEGER", it = "PY_EXPR", val = B)
            variables["B"] = B
            begin_loop_iteration (info = "B = " + str (B))



            if False:
                begin_wf_item (index = 9, is_custom_code = True, name = "Populate table")
                import numpy as np

                WELL_NAME = get_table_by_name (name="MULT").get_data (row=B, column=1)
                MULT = float(get_table_by_name (name="MULT").get_data (row=B, column=5))
                TOP = float(get_table_by_name (name="MULT").get_data (row=B, column=3))
                BOT = float(get_table_by_name (name="MULT").get_data (row=B, column=4))

                calc = f"if (MD>={TOP}&MD<={BOT},{MULT},MULT)"
                print(calc)

                wells_filter_create (output_well_filter=find_object (name="Temp_filter",
                      type="WellFilter"),
                      use_parent_well_filter=False,
                      parent_well_filter=find_object (name="Import Model Well Filter(BLACK_OIL_DEMO)",
                      type="WellFilter"),
                      included_well_names=[WELL_NAME])
                      
                      
                wells_log_calculator (result_well_log=find_object (name="MULT",
                      type="WellLog"),
                      trajectories=find_object (name="Trajectories",
                      type="Trajectories"),
                      wells_log_grid_mode="well_log",
                      well_log=find_object (name="ZONES",
                      type="WellLog"),
                      use_log_domain=True,
                      use_well_filter=True,
                      well_filter=find_object (name="Temp_filter",
                      type="WellFilter"),
                      uniform_grid_step=0.1,
                      use_interpolation_mode=False,
                      interpolation_mode="linear",
                      formula=calc,
                      variables=variables)


                COUNTER += 1 
                end_wf_item (index = 9)


            end_loop_iteration ()

        end_wf_item (index = 8)


    if False:
        begin_wf_item (index = 11, is_custom_code = True, name = "DONT_WORK!")
        import numpy as np

        for key, value in MULTS.items():
        	#get_well_log_by_name (name='MULT').clear (well=key)
        	get_well_log_by_name (name='MULT').set_np_array (values=value, well=key)

        end_wf_item (index = 11)


    begin_wf_item (index = 12, is_custom_code = True, name = "Импорт кривых ГИС в формате ASCII таблица")
    wells_log_import_table_format (wells=find_object (name="Wells",
          type="gt_wells_entity"),
          trajectories=find_object (name="Trajectories",
          type="Trajectories"),
          use_tags_to_assign=False,
          tags_to_assign=[],
          use_folder=False,
          folder="",
          splitter=True,
          well_log_files_table=[{"file_name" : f"{MUTL_TABLE_NAME}.txt", "uname" : find_object (name=resolve_variables_in_string (string_with_variables="@MUTL_TABLE_NAME@",
          variables=variables),
          type="WellLog")}],
          splitter2=True,
          tabulator=TableFormat (separator="comma",
          comment="#",
          skip_lines=1,
          columns=["skip", "Well", "skip", "Log Data", "skip", "MD"]),
          splitter3=True,
          well_choosing_type="from_column",
          use_user_well_name=False,
          user_well_name="Well_1",
          is_log_name_from_file=True,
          logs_table=[],
          clear_same_name=False,
          use_oem_encoding=False,
          use_novalue=False,
          novalue=-999.25,
          elongate_traj=False)
    end_wf_item (index = 12)


    if False:
        begin_wf_item (index = 13)
        wells_log_import_table_format (wells=find_object (name="Wells",
              type="gt_wells_entity"),
              trajectories=find_object (name="Trajectories",
              type="Trajectories"),
              use_tags_to_assign=False,
              tags_to_assign=[],
              use_folder=False,
              folder="",
              splitter=True,
              well_log_files_table=[{"file_name" : "test.txt", "uname" : find_object (name=resolve_variables_in_string (string_with_variables="@MUTL_TABLE_NAME@",
              variables=variables),
              type="WellLog")}],
              splitter2=True,
              tabulator=TableFormat (separator="comma",
              comment="#",
              skip_lines=1,
              columns=["skip", "Well", "skip", "Log Data", "skip", "MD"]),
              splitter3=True,
              well_choosing_type="from_column",
              use_user_well_name=False,
              user_well_name="Well_1",
              is_log_name_from_file=True,
              logs_table=[],
              clear_same_name=False,
              use_oem_encoding=False,
              use_novalue=False,
              novalue=-999.25,
              elongate_traj=False)
        end_wf_item (index = 13)


    begin_wf_item (index = 14)
    wells_log_set_interpolation_mode (interpolation_mode="discrete",
          wells_logs=[{"wells_log" : find_object (name=resolve_variables_in_string (string_with_variables="@MUTL_TABLE_NAME@",
          variables=variables),
          type="WellLog")}])
    end_wf_item (index = 14)


    begin_wf_item (index = 15)
    wells_log_resample (wells=find_object (name="Wells",
          type="gt_wells_entity"),
          use_well_filter=False,
          well_filter=find_object (name="Import Model Well Filter(BLACK_OIL_DEMO)",
          type="WellFilter"),
          source_log=find_object (name=resolve_variables_in_string (string_with_variables="@MUTL_TABLE_NAME@",
          variables=variables),
          type="WellLog"),
          target_log=find_object (name=resolve_variables_in_string (string_with_variables="@MUTL_TABLE_NAME@",
          variables=variables),
          type="WellLog"),
          step=1)
    end_wf_item (index = 15)


    begin_wf_item (index = 16)
    create_blocked_well_log (mesh=find_object (name="BLACK_OIL_DEMO",
          type="Grid3d"),
          BlockedWells=find_object (name=resolve_variables_in_string (string_with_variables="@MUTL_TABLE_NAME@",
          variables=variables),
          type="BlockedWells"),
          use_well_filter=False,
          well_filter=find_object (name="Import Model Well Filter(BLACK_OIL_DEMO)",
          type="WellFilter"),
          use_filter=False,
          user_cut=find_object (name="ACTNUM",
          type="Grid3dProperty"),
          comparator=Comparator (rule="not_equals",
          value=0),
          input_log=find_object (name=resolve_variables_in_string (string_with_variables="@MUTL_TABLE_NAME@",
          variables=variables),
          type="WellLog"),
          use_override_discreteness=True,
          override_discreteness="discrete",
          averaging_method="minimum",
          averaging_power=0,
          random_seed=0,
          kernel_bandwidth=0.5,
          treat_log_as="points",
          use_min_points_in_block=False,
          min_points_in_block=3,
          use_bias=False,
          bias_blocked_wells=find_object (name="MULT",
          type="BlockedWells"),
          bias_log_data=find_object (name="ZONES",
          type="WellLog"),
          wells=find_object (name="Wells",
          type="gt_wells_entity"))
    end_wf_item (index = 16)


    begin_wf_item (index = 17)
    grid_property_interpolate_by_blocked_wells_trivial_3d (mesh=find_object (name="BLACK_OIL_DEMO",
          type="Grid3d"),
          blocked_wells=find_object (name="MULT",
          type="BlockedWells"),
          clear_values=True,
          use_default_value=False,
          default_value=0,
          result_grid_property=find_object (name="MULT",
          type="Grid3dProperty"))
    end_wf_item (index = 17)


    begin_wf_item (index = 18)
    grid_property_interpolate_by_wells_log_3d (wells=find_object (name="Wells",
          type="gt_wells_entity"),
          mesh=find_object (name="BLACK_OIL_DEMO",
          type="Grid3d"),
          input_data_type="blocked_wells",
          input_partial_cube=find_object (name=resolve_variables_in_string (string_with_variables="@MUTL_TABLE_NAME@",
          variables=variables),
          type="InitialBlocks"),
          blocked_wells=find_object (name=resolve_variables_in_string (string_with_variables="@MUTL_TABLE_NAME@",
          variables=variables),
          type="BlockedWells"),
          not_use_blocked_wells=False,
          statistics=find_object (name="Statistics",
          type="BlockedWellsStatistics"),
          result_grid_property=find_object (name=resolve_variables_in_string (string_with_variables="@MUTL_TABLE_NAME@",
          variables=variables),
          type="Grid3dProperty"),
          use_kriging_variance=False,
          kriging_variance_grid_property=find_object (name="ACTNUM",
          type="Grid3dProperty"),
          space_type="ijk",
          use_filter=False,
          user_cut=find_object (name="ACTNUM",
          type="Grid3dProperty"),
          comparator=Comparator (rule="not_equals",
          value=0),
          fade_to_border=False,
          use_global_random_seed=False,
          global_random_seed=0,
          advanced_options=False,
          with_lgr=False,
          clear_values=True,
          compatibility_options=False,
          whole_grid_random=True,
          use_random_process=True,
          use_compatibility_sum_in_sgs=False,
          i3_params=Interpolation3dParameters (zone_region_filter=ZoneRegionFilterInfo (use_zone=False,
          use_region=False,
          zone=find_object (name="",
          type=""),
          region=find_object (name="",
          type="")),
          zone_region_filter_args=ZoneRegionFilter (zone=None,
          region=None),
          ZoneRegionParameters=[ZoneRegionParameters (use=True,
          zone=None,
          region=None,
          facies_order=[],
          current_facies=None,
          restrict=ContactParameters (restriction_type="none",
          secondary_attribute=find_object (name="",
          type=""),
          m_use_da_cond_distr=False,
          use_contact_restriction=False,
          contact=find_object (name="",
          type=""),
          use_contact_horizon=False,
          contact_horizon=find_object (name="",
          type=""),
          contact_map_total=find_object (name="",
          type="")),
          parameters=[ZoneRegionFaciesParameters (facies=None,
          params=InterpolationParametersItem (use=True,
          interpolator_type="sgs",
          kriging_params=KrigingParameters (kriging_type="simple",
          global_mean=0,
          use_global_mean=False,
          use_kriging_points=True,
          kriging_points=50,
          random_seed=0),
          cokriging_params=CokrigingParameters (use_cokriging=False,
          collocated_coeff=0.5,
          source_type="none",
          source_3d=find_object (name="",
          type=""),
          source_2d=find_object (name="",
          type=""),
          source_1d=find_object (name="",
          type="")),
          trend=TrendParameters (use_da_transformations=False,
          trend_type="none",
          trend_3d=find_object (name="",
          type=""),
          trend_2d=find_object (name="",
          type=""),
          vpc_source="recalc",
          do_normalize=False,
          smooth_cutoff_maps=False,
          cutoff_maps_smooth_radius=0),
          variogram=VariogramParameters (variogram_type="exponential",
          sill=1,
          nugget_effect=0,
          range_main=100,
          range_normal=100,
          range_vertical=10,
          azimuth=0,
          dip=0,
          azimuth_map=find_object (name="",
          type="Map2d"),
          use_azimuth_map=False,
          external_source=False,
          space_type="xyz"),
          distribution=DistributionParameters (use_da=False,
          distribution_type="none",
          well_log=find_object (name="",
          type="WellLog"),
          log_from_blocked_wells=True,
          declustering_weights=find_object (name=resolve_variables_in_string (string_with_variables="@MUTL_TABLE_NAME@",
          variables=variables),
          type="BlockedWellsAttribute"),
          use_declustering_weights=True,
          mean_normal=0,
          mean_log_normal=0,
          mean_beta=1,
          sdev_normal=1,
          sdev_log_normal=1,
          sdev_beta=1,
          adjust_type_continuous="cut_by_bounds",
          input_trunc_use_min=False,
          input_trunc_use_max=False,
          input_trunc_min=0,
          input_trunc_max=0,
          input_trunc_type="clamp",
          output_trunc_use_min=True,
          output_trunc_use_max=False,
          output_trunc_min=1,
          output_trunc_max=0,
          output_trunc_type="clamp"),
          fraction=FractionParameters (fraction_source="none",
          fraction_value=0,
          is_fraction_freezed=False,
          use_declustering_weights=False,
          weights_uid=find_object (name="",
          type=""),
          use_distribution_fitting=False),
          restrictions=RestrictionsParameters (contact_restriction_map=find_object (name="",
          type=""),
          restriction_map=find_object (name="",
          type=""),
          vpc_source="recalc"),
          amazonas=AmazonasParameters (major_axis_src_type="value",
          major_semi_axis=250,
          major_semi_axis_blocks=5,
          major_semi_axis_map=find_object (name="",
          type=""),
          major_minor_src_type="value",
          major_minor_ratio=1,
          major_minor_ratio_map=find_object (name="",
          type=""),
          azimuth_src_type="value",
          azimuth=0,
          azimuth_map=find_object (name="",
          type=""),
          vertical_axis_src_type="map",
          vertical_semi_axis=5,
          vertical_semi_axis_blocks=2,
          random_seed=0,
          aposteriori_drift_src_type="value",
          aposteriori_drift=0.0001,
          noise_map=find_object (name="",
          type=""),
          axis_units_src_type="length",
          use_apriori_drift=False,
          apriori_drift=0,
          min_threshold=5,
          src_points_weight=5,
          amazonas_stat_type="median",
          kernel_bandwidth=0.5)))],
          use_trend_from_da=False,
          smooth_da_trend=False,
          smooth_step_cnt=10,
          smooth_alpha=0.5)],
          apply_to_all_zr=False,
          apply_to_all_f=False))
    end_wf_item (index = 18)



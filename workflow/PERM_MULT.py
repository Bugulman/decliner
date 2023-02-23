#  Этот файл был сгенерирован тНавигатор v22.4-3544-g24519bd52cae.
#  Copyright (C) Рок Флоу Динамикс 2005-2023.
#  Все права защищены.

# This file is MACHINE GENERATED! Do not edit.

#api_version=v0.0.80

from __main__.tnav.workflow import *
from tnav_debug_utilities import *
from datetime import datetime, timedelta


declare_workflow (workflow_name="PERM_MULT",
      variables=[])


PERM_MULT_variables = {

}

def PERM_MULT (variables = PERM_MULT_variables):
    pass
    check_launch_method ()


    begin_user_imports ()
    end_user_imports ()

    begin_wf_item (index = 1, is_custom_code = True)
    table=get_table_by_name (name='PERM_MULT')
    for row in range(0,table.get_row_count ()):
      well=table.get_data (row=row+1, column=1)
      mult=table.get_data (row=row+1, column=2)
      wells_filter_create (output_well_filter=find_object (name="WellFilter1",
          type="WellFilter"),
          use_parent_well_filter=False,
          parent_well_filter=find_object (name="",
          type="WellFilter"),
          included_well_names=[well])
      blocked_well_log_calculator (mesh=find_object (name="main_grid",
          type="Grid3d"),
          BlockedWells=find_object (name="PERM_MULT",
          type="BlockedWells"),
          use_well_filter=True,
          well_filter=find_object (name="WellFilter1",
          type="WellFilter"),
          formula=mult,
          variables=variables)

    end_wf_item (index = 1)


    begin_wf_item (index = 2)
    grid_property_interpolate_by_wells_log_idw_multilayer (mesh=find_object (name="main_grid",
          type="Grid3d"),
          result_grid_property=find_object (name="PERM_MULT",
          type="Grid3dProperty"),
          wells=find_object (name="Wells",
          type="gt_wells_entity"),
          cut_by_bounds=True,
          use_filter=False,
          user_cut=find_object (name="регионы",
          type="Grid3dProperty"),
          comparator=Comparator (rule="equals",
          value=1),
          fade_to_border=True,
          use_trend=False,
          trend_property_type="arbitrary",
          trend_grid_property=find_object (name="Property1",
          type="Grid3dProperty"),
          use_trend_vpc_map_2d=False,
          trend_vpc_map_2d=find_object (name="",
          type="Map2d"),
          use_well_filter=False,
          well_filter=find_object (name="Well Filter 1",
          type="WellFilter"),
          input_data_type="blocked_wells",
          well_log=find_object (name="",
          type="WellLog"),
          blocked_wells=find_object (name="PERM_MULT",
          type="BlockedWells"),
          discrete_interpolation=False,
          interpolate_log=True,
          use_empty_layer_value=True,
          empty_layer_value=1,
          power_parameter=2,
          idw_azimuth=0,
          idw_axis_ratio=1)
    end_wf_item (index = 2)


    begin_wf_item (index = 3)
    grid_property_calculator (mesh=find_object (name="main_grid",
          type="Grid3d"),
          result_grid_property=find_object (name="Проницаемость X МОД 3",
          type="Grid3dProperty"),
          discrete_output=False,
          use_filter=False,
          user_cut_for_filter=find_object (name="Property1",
          type="Grid3dProperty"),
          filter_comparator=Comparator (rule="not_equals",
          value=0),
          formula="if(k<5&k>2,grid_property (\"Проницаемость X МОД\")*PERM_MULT,grid_property (\"Проницаемость X МОД\"))",
          variables=variables)
    end_wf_item (index = 3)


    begin_wf_item (index = 4)
    grid_property_calculator_block (mesh=find_object (name="main_grid",
          type="Grid3d"),
          result_grid_property=find_object (name="Property1",
          type="Grid3dProperty"),
          use_filter=False,
          user_cut_for_filter=find_object (name="Property1",
          type="Grid3dProperty"),
          filter_comparator=Comparator (rule="not_equals",
          value=0),
          i_start=1,
          i_end=1,
          j_start=1,
          j_end=0,
          k_start=1,
          k_end=0,
          formula="",
          variables=variables)
    end_wf_item (index = 4)



#  Этот файл был сгенерирован тНавигатор v23.2-3636-gbbb9c7349176.
#  Copyright (C) Рок Флоу Динамикс 2005-2023.
#  Все права защищены.

# This file is MACHINE GENERATED! Do not edit.

#api_version=v0.0.94a

from __main__.tnav.workflow import *
from tnav_debug_utilities import *
from datetime import datetime, timedelta


declare_workflow (workflow_name="poligon_extension",
      variables=[])


poligon_extension_variables = {

}

def poligon_extension (variables = poligon_extension_variables):
    pass
    check_launch_method ()


    begin_user_imports ()
    end_user_imports ()

    begin_wf_item (index = 1)
    shifted_value = 70
    set_var_type (n = "shifted_value", t = "INTEGER", it = "PY_EXPR", val = shifted_value)
    variables["SHIFTED_VALUE"] = shifted_value
    base_poligon = 'some'
    set_var_type (n = "base_poligon", t = "STRING", it = "PY_EXPR", val = base_poligon)
    variables["BASE_POLIGON"] = base_poligon
    final_name = base_poligon+'_extended'
    set_var_type (n = "final_name", t = "PY_EXPR", it = "PY_EXPR", val = final_name)

    end_wf_item (index = 1)


    begin_wf_item (index = 2, is_custom_code = True, name = "Создаем лист со сдвижками многоугольника")
    from itertools import permutations



    shifts = list(permutations([-shifted_value, 0, shifted_value],2))
    shifts.append((shifted_value, shifted_value))
    shifts.append((-shifted_value, -shifted_value))

    print(shifts)
    end_wf_item (index = 2)


    begin_wf_item (index = 3)
    for sh in enumerate(shifts):
        pass
        set_var_type (n = "sh", t = "PY_EXPR", it = "PY_EXPR", val = sh)
        begin_loop_iteration (info = "sh = " + str (sh))



        begin_wf_item (index = 4, is_custom_code = True, name = "Создаем вспомагательные полигоны со сдвижками")
        print(f'Poligon {sh[0]} has coord {sh[1]}')
        new_poligon_name = f'Polygon{sh[0]+1}'
        coord = sh[1]

        polygon_transform (result_polygon=find_object (name=new_poligon_name,
              type="Curve3d"),
              source_polygon=find_object (name='some',
              type="Curve3d"),
              transform_type=" shift",
              x_shift=coord[0],
              y_shift=coord[1],
              z_shift=0,
              center_x=0,
              center_y=0,
              angle=0,
              scale=1,
              scale_center_x=0,
              scale_center_y=0)
        end_wf_item (index = 4)


        end_loop_iteration ()

    end_wf_item (index = 3)


    begin_wf_item (index = 6, is_custom_code = True, name = "Соединяем многоугольники в один")
    polygon_create_by_merged_polygons (result_polygon=find_object (name=final_name,
          type="Curve3d"),
          polygons_table=[{"use" : True, "polygon" : find_object (name="Polygon1",
          type="Curve3d")}, {"use" : True, "polygon" : find_object (name="Polygon2",
          type="Curve3d")}, {"use" : True, "polygon" : find_object (name="Polygon3",
          type="Curve3d")}, {"use" : True, "polygon" : find_object (name="Polygon4",
          type="Curve3d")}, {"use" : True, "polygon" : find_object (name="Polygon5",
          type="Curve3d")}, {"use" : True, "polygon" : find_object (name="Polygon6",
          type="Curve3d")}, {"use" : True, "polygon" : find_object (name="Polygon7",
          type="Curve3d")}, {"use" : True, "polygon" : find_object (name="Polygon8",
          type="Curve3d")}])
    end_wf_item (index = 6)


    begin_wf_item (index = 7)
    for name in enumerate(shifts):
        pass
        set_var_type (n = "name", t = "PY_EXPR", it = "PY_EXPR", val = name)
        rem_poly = f'Polygon{name[0]+1}'
        set_var_type (n = "rem_poly", t = "PY_EXPR", it = "PY_EXPR", val = rem_poly)
        begin_loop_iteration (info = "name = " + str (name))



        begin_wf_item (index = 8, is_custom_code = True, name = "Удаление промежуточных многоугольников")

        object_delete (object=absolute_object_name (name=None,
              typed_names=[typed_object_name (obj_name=rem_poly,
              obj_type="Curve3d")]),
              ignore_if_not_exists=False)
        end_wf_item (index = 8)


        end_loop_iteration ()

    end_wf_item (index = 7)



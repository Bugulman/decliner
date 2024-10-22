#  Этот файл был сгенерирован тНавигатор v24.2-4325-ga170e3ea.
#  Copyright (C) Рок Флоу Динамикс 2005-2024.
#  Все права защищены.

# This file is MACHINE GENERATED! Do not edit.

#api_version=v0_0_145

from __main__.tnav.workflow import *
from tnav_debug_utilities import *
from datetime import datetime, timedelta


declare_workflow (workflow_name="wells_screen",
      variables=[])


wells_screen_variables = {

}

def wells_screen (variables = wells_screen_variables):
    pass
    check_launch_method ()


    begin_user_imports ()
    end_user_imports ()

    begin_wf_item (index = 1, name = "Прочти меня")
    comment_text ("""
Данный workflow выполняет экспорт графиков в формате pdf из модели.
При этом в папке с проектом создается отдельная папка repotr, в которую производится импорт
В локальных переменных нужно задать название вкладки с графиками, которые будут экспортироваться в pdf.

При этом необходимо предварительно настроить сами графики по макркерам, цветам и т.д.

""")
    end_wf_item (index = 1)


    begin_wf_item (index = 2, name = "Задать имя рабочего окна для экспорта")
    window_name = 'Отчетные'
    set_var_type (n = "window_name", t = "STRING", it = "PY_EXPR", val = window_name)
    variables["WINDOW_NAME"] = window_name

    end_wf_item (index = 2)


    if False:
        begin_wf_item (index = 3, name = "Сохранить график")
        create_screenshot (window_name="Отчетные",
              extension="pdf",
              filename="../../../Изображения/Участок4_вода.PDF",
              pagesize="A3",
              orientation="Landscape",
              layout_type="Best Fit",
              units="pixels",
              width=1920,
              height=1200,
              add_date_to_filename=True,
              add_date_to_filename_method="add_current_calendar_date",
              create_screenshots_pack=False,
              first_step_number=0,
              last_step_number=190,
              add_step_number_to_filename=True,
              date_format="DD-MM-YYYY",
              font="Arial,24,-1,5,50,0,0,0,0,0",
              caption_position="Above",
              caption_alignment="Left",
              use_default_name=False,
              default_name=None,
              caption=None)
        end_wf_item (index = 3)


    if False:
        begin_wf_item (index = 4)
        graph_template_object (window_type="Graph Templates",
              window_name="Отчетные",
              objects_table=[{"object_type" : "Well", "object_name" : "4A142"}],
              clear_selection=False)
        end_wf_item (index = 4)


    begin_wf_item (index = 5, is_custom_code = True, name = "Графики по скважинам")
    from pathlib import Path
    import os


    path = Path(get_project_folder ())


    print(path)

    def save_pic(w, win_name, path=path):
    	path = path.joinpath('reports', w+'.PDF')
    	create_screenshot (window_name=win_name,
          extension="pdf",
          filename=str(path),
          pagesize="A3",
          orientation="Landscape",
          layout_type="Best Fit",
          units="pixels",
          width=1920,
          height=1300,
          add_date_to_filename=True,
          add_date_to_filename_method="add_current_calendar_date",
          create_screenshots_pack=False,
          first_step_number=0,
          last_step_number=190,
          add_step_number_to_filename=True,
          date_format="DD-MM-YYYY",
          font="Arial,24,-1,5,50,0,0,0,0,0",
          caption_position="Above",
          caption_alignment="Left",
          use_default_name=False,
          default_name=None,
          caption=None)

    def graph_change(well, win_name):
    	graph_template_object (window_type="Graph Templates",
          window_name=win_name,
          objects_table=[{"object_type" : "Well", "object_name" : well}],
          clear_selection=True)

    for w in get_all_wells ():
    	graph_change(w.name, win_name=window_name)
    	save_pic(w.name, win_name=window_name)
    	print(w.name)
    end_wf_item (index = 5)



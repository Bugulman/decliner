import PySimpleGUI as sg
from files_func import hist_table_prepare
from smoother import histor_smoothing
import pandas as pd
import logging
import pickle
from oily_report import interpolate_press_by_sipy
from DCA import dec_predict
import random, string
from tqdm import tqdm


logging.basicConfig(level=logging.DEBUG,format = "%(asctime)s - %(levelname)s - %(message)s")
data = []
headings = ['well', 'first_date', 'qi', 'Di', 'bi', 'Dterm']

def make_window(theme):
    sg.theme(theme)
    menu_def = [['&Application', ['E&xit']],
                ['&Help', ['&About']] ]
    right_click_menu_def = [[], ['Edit Me', 'Versions', 'Nothing','More Nothing','Exit']]
    # graph_right_click_menu_def = [[], ['Erase','Draw Line', 'Draw',['Circle', 'Rectangle', 'Image'], 'Exit']]

    input_layout =  [                # [sg.Menu(menu_def, key='-MENU-')],
                [sg.Text('Anything that requires user-input is in this tab!')], 
                [sg.Input(key='-INPUT-')],
                [sg.Text('Добыча', size=(13, 1)),sg.InputText(key='-file1-'), sg.FileBrowse()],
                [sg.Text('Давление', size=(13, 1)), sg.InputText(key='-file2-'),sg.FileBrowse(target='-file2-')],
                [sg.Listbox(key='-GORIZON-',values=('Listbox Item 1', 'Listbox Item 2', 'Listbox Item 3'),
                      select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, size=(20, 3))],
                # [sg.FileBrowse('Файл с добычей')],
                # [sg.Slider(orientation='h', key='-SKIDER-')],
                 # sg.Image(data=sg.DEFAULT_BASE64_LOADING_GIF, enable_events=True, key='-GIF-IMAGE-'),],
                # [sg.Checkbox('Checkbox', default=True, k='-CB-')],
                # [sg.Radio('Radio1', "RadioDemo", default=True, size=(10,1), k='-R1-'), sg.Radio('Radio2', "RadioDemo", default=True, size=(10,1), k='-R2-')],
                # [sg.Combo(values=('Combo 1', 'Combo 2', 'Combo 3'), default_value='Combo 1', readonly=True, k='-COMBO-'),
                 # sg.OptionMenu(values=('Option 1', 'Option 2', 'Option 3'),  k='-OPTION MENU-'),],
                # [sg.Spin([i for i in range(1,11)], initial_value=10, k='-SPIN-'), sg.Text('Spin')],
                # [sg.Multiline('Demo of a Multi-Line Text Element!\nLine 2\nLine 3\nLine 4\nLine 5\nLine 6\nLine 7\nYou get the point.', size=(45,5), expand_x=True, expand_y=True, k='-MLINE-')],
        [sg.Button('IMPORT', key='-IMPORT-'),  sg.Button(image_data=sg.DEFAULT_BASE64_ICON, key='-logo-')]]

    data_preparation = [[sg.T('Теммп падения скважин')],
               [sg.Image(data=sg.DEFAULT_BASE64_ICON,  k='-IMAGE-'),sg.Button('Подготовка данных', key='-PREPARE-')],
               [sg.ProgressBar(100, orientation='h', size=(20, 20), key='-PROGRESS BAR-'), sg.Button('Test Progress bar')],
                [sg.Table(values=data, headings=headings, max_col_width=5,
                    auto_size_columns=False,
                    display_row_numbers=True,
                    justification='right',
                    num_rows=20,
                    alternating_row_color='lightyellow',
                    key='-TABLE-',
                    selected_row_colors='red on yellow',
                    enable_events=True,
                    expand_x=True,
                    expand_y=True,
                    enable_click_events=True,           # Comment out to not enable header and other clicks
                    tooltip='This is a table')],
                ]

    logging_layout = [[sg.Text("Anything printed will display here!")],
                      [sg.Multiline(size=(60,15), font='Courier 8', expand_x=True, expand_y=True, write_only=True,
                                    reroute_stdout=True, reroute_stderr=True, echo_stdout_stderr=True, autoscroll=True, auto_refresh=True)]
                      # [sg.Output(size=(60,15), font='Courier 8', expand_x=True, expand_y=True)]
                      ]
    
    # graphing_layout = [[sg.Text("Anything you would use to graph will display here!")],
    #                   [sg.Graph((200,200), (0,0),(200,200),background_color="black", key='-GRAPH-', enable_events=True,
    #                             right_click_menu=graph_right_click_menu_def)],
    #                   [sg.T('Click anywhere on graph to draw a circle')],
    #                   [sg.Table(values=data, headings=headings, max_col_width=25,
    #                             background_color='black',
    #                             auto_size_columns=True,
    #                             display_row_numbers=True,
    #                             justification='right',
    #                             num_rows=2,
    #                             alternating_row_color='black',
    #                             key='-TABLE-',
    #                             row_height=25)]]

    # popup_layout = [[sg.Text("Popup Testing")],
    #                 [sg.Button("Open Folder")],
    #                 [sg.Button("Open File")]]
    
    theme_layout = [[sg.Text("See how elements look under different themes by choosing a different theme here!")],
                    [sg.Listbox(values = sg.theme_list(), 
                      size =(20, 12), 
                      key ='-THEME LISTBOX-',
                      enable_events = True)],
                      [sg.Button("Set Theme")]]
    
    layout = [ [sg.MenubarCustom(menu_def, key='-MENU-', font='Courier 15', tearoff=True)],
                    [sg.Text('DCA', size=(38, 1), justification='center', font=("Helvetica", 16), relief=sg.RELIEF_RIDGE, k='-TEXT HEADING-', enable_events=True)]]
    layout +=[[sg.TabGroup([[  sg.Tab('Ввод данных', input_layout),
                               sg.Tab('Темп падения', data_preparation),
                               # sg.Tab('Graphing', graphing_layout),
                               # sg.Tab('Popups', popup_layout),
                               sg.Tab('Theming', theme_layout),
                               sg.Tab('Output', logging_layout)]], key='-TAB GROUP-', expand_x=True, expand_y=True),

               ]]
    layout[-1].append(sg.Sizegrip())
    window = sg.Window('DCA by VAR', layout, right_click_menu=right_click_menu_def, right_click_menu_tearoff=True, grab_anywhere=True, resizable=True, margins=(0,0), use_custom_titlebar=True, finalize=True, keep_on_top=True,
                       # scaling=2.0,
                       )
    window.set_min_size(window.size)
    return window

def main():
    window = make_window(sg.theme())
    
    # This is an Event Loop 
    while True:
        event, values = window.read(timeout=100)
        # keep an animation running so show things are happening
        # window['-GIF-IMAGE-'].update_animation(sg.DEFAULT_BASE64_LOADING_GIF, time_between_frames=100)
        if event not in (sg.TIMEOUT_EVENT, sg.WIN_CLOSED):
            print('============ Event = ', event, ' ==============')
            print('-------- Values Dictionary (key=value) --------')
            for key in values:
                print(key, ' = ',values[key])
        if event in (None, 'Exit'):
            print("[LOG] Clicked Exit!")
            break
        elif event == 'About':
            print("[LOG] Clicked About!")
            sg.popup('PySimpleGUI Demo All Elements',
                     'Right click anywhere to see right click menu',
                     'Visit each of the tabs to see available elements',
                     'Output of event and values can be see in Output tab',
                     'The event and values dictionary is printed after every event', keep_on_top=True)

        if event == '-IMPORT-':
            try:
                prod = pd.read_excel(values['-file1-'], usecols="B:N")
                press = pd.read_excel(values['-file2-'], usecols = "F:M")
                window['-GORIZON-'].update(prod['Горизонт'].unique())
                print(prod['Горизонт'].unique())
            except Exception as e:
                raise e
        elif event == '-PREPARE-':
            prod = pd.read_excel(values['-file1-'], usecols="B:N")
            press = pd.read_excel(values['-file2-'], usecols = "F:M")
            keyword = {'hist_file':[prod, press], 'gor_num':values['-GORIZON-']}
            result = hist_table_prepare(**keyword)
            df = histor_smoothing(result)
        # elif event == 'Popup':
        #     print("[LOG] Clicked Popup Button!")
        #     sg.popup("You pressed a button!", keep_on_top=True)
        #     print("[LOG] Dismissing Popup!")
        elif event == 'Test Progress bar':
            print("[LOG] Clicked Test Progress Bar!")
            names = df.loc[(df.status == 'prod') & (df['date'] > '2010'), 'well'].unique()
            predict=pd.DataFrame(columns=['well', 'date', 'SOIL', 'QOIL', 'Time_x', 'Time_y', 'rate', 'month_prod'])

            to_table=pd.DataFrame(columns=['well', 'first_date', 'qi', 'Di', 'bi', 'Dterm'])
            progress_bar = window['-PROGRESS BAR-']
            progress_bar.update(0, len(names))
            i=0
            for name, fr in df.loc[df.well.isin(names)].groupby('well'):
                well_predict, dca_param= dec_predict(fr)
                # predict = pd.concat([predict, well_predict], ignore_index=True)
                to_table = pd.concat([to_table, dca_param], ignore_index=True)
                progress_bar.update(current_count=i + 1)
                i+=1
            data = to_table.values.tolist()
            window['-TABLE-'].update(values=data)
            print("[LOG] Progress bar complete!")
        # elif event == "-GRAPH-":
        #     graph = window['-GRAPH-']       # type: sg.Graph
        #     graph.draw_circle(values['-GRAPH-'], fill_color='yellow', radius=20)
        #     print("[LOG] Circle drawn at: " + str(values['-GRAPH-']))
        # elif event == "Open Folder":
        #     print("[LOG] Clicked Open Folder!")
        #     folder_or_file = sg.popup_get_folder('Choose your folder', keep_on_top=True)
        #     sg.popup("You chose: " + str(folder_or_file), keep_on_top=True)
        #     print("[LOG] User chose folder: " + str(folder_or_file))
        # # elif event == "Open File":
        #     print("[LOG] Clicked Open File!")
        #     folder_or_file = sg.popup_get_file('Choose your file', keep_on_top=True)
        #     sg.popup("You chose: " + str(folder_or_file), keep_on_top=True)
        #     print("[LOG] User chose file: " + str(folder_or_file))
        # elif event == "Set Theme":
        #     print("[LOG] Clicked Set Theme!")
        #     theme_chosen = values['-THEME LISTBOX-'][0]
        #     print("[LOG] User Chose Theme: " + str(theme_chosen))
        #     window.close()
        #     window = make_window(theme_chosen)
        # elif event == 'Edit Me':
        #     sg.execute_editor(__file__)
        # elif event == 'Versions':
        #     sg.popup(sg.get_versions(), keep_on_top=True)

    window.close()
    exit(0)

if __name__ == '__main__':
    sg.theme('black')
    sg.theme('dark red')
    sg.theme('dark green 7')
    # sg.theme('DefaultNoMoreNagging')
    main()

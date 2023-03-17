import PySimpleGUI as sg

sg.theme('DarkBlue')


def custom_meter_example():
    # layout the form
    layout = [[sg.Text('Progress_bar')],
              [sg.ProgressBar(1, orientation='h', size=(
                  20, 20), key='progress')],
              [sg.Cancel()]]

    # create the form`
    window = sg.Window('Выполение кода', layout)
    progress_bar = window['progress']
    # loop that would normally do something useful
    for i in range(10000):
        # check to see if the cancel button was clicked and exit loop if clicked
        event, values = window.read(timeout=0)
        if event == 'Cancel' or event == None:
            break
        # update bar with loop value +1 so that bar eventually reaches the maximum
        progress_bar.update_bar(i+1, 10000)
    # done with loop... need to destroy the window as it's still open
    window.close()


c = 0
for i in get_all_wells():
    sg.one_line_progress_meter(
        'My Meter', c+1, len(get_all_wells()), 'key', 'Optional message')
    c += 1

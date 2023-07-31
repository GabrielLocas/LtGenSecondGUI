
import PySimpleGUI as sg
import threading
import time

from comm import sendStartPacket, sendStopPacket
from layout import stimulation_column, light_column, sound_column, control_column, check_values

def checkIfInRange(value, min, max):
    print("Value is not comprised within {} and {}", min, max)
    return value >= min and value <= max

running = False
image_path = 'falloutGuyRescaled.png'
app_image_path = 'falloutComputerTrimmed.ico'

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    layout = [
        [control_column],
        [sg.HorizontalSeparator()],
        [stimulation_column],
        [sg.HorizontalSeparator()],
        [sound_column],
        [sg.HorizontalSeparator()],
        [light_column]
    ]

    fallout_3_terminal_theme = {
        'BACKGROUND': '#000000',
        'TEXT': '#00FF00',
        'INPUT': '#00FF00',
        'TEXT_INPUT': '#000000',
        'SCROLL': '#00FF00',
        'BUTTON': ('black', '#00FF00'),
        'PROGRESS': ('#00FF00', '#000000'),
        'BORDER': 1, 'SLIDER_DEPTH': 0, 'PROGRESS_DEPTH': 0,
    }

    sg.theme_add_new('Fallout 3 Terminal', fallout_3_terminal_theme)
    sg.theme('Fallout 3 Terminal')
    sg.set_options(font=('Courier New', 14))
    # Create the window
    window = sg.Window("LightCore Tone Generator", layout, icon=app_image_path)


    def timer_thread(values):
        stim_time = int(values['-STIM_TIME-'])
        rest_time = int(values['-REST_TIME-'])
        repetitions = int(values['-REPETITIONS-'])
        running = True

        print("Start of stimulation...")
        while(repetitions > 0 and running):
            print("START!")
            start_time = time.time()
            sendStartPacket(values)
            while (time.time() - start_time < stim_time and running):
                event, values = window.read(timeout=100)
                if event == sg.WIN_CLOSED or event == 'Stop':
                    running = False

            print("Stimulation cycle finished! Time elapsed : ", time.time() - start_time)
            start_time = time.time()
            sendStopPacket(values)
            while (time.time() - start_time < rest_time and running):
                event, values = window.read(timeout=100)
                if event == sg.WIN_CLOSED or event == 'Stop':
                    running = False

            print("Rest cycle finished! Time elapsed : ", time.time() - start_time)
            repetitions = repetitions -1
            event, values = window.read(timeout=100)
            if event == sg.WIN_CLOSED or event == 'Stop':
                running = False

        print("...end of stimulation")
        return
    # Create an event loop
    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break
        if event == "Start":
            if check_values(values):
                t1 = threading.Thread(target=timer_thread(values), daemon=True)
                t1.start()

    window.close()

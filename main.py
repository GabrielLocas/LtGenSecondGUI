
import PySimpleGUI as sg
import threading
import time

from comm import sendStartPacket, sendStopPacket
from layout import stimulation_column, light_column, sound_column, control_column
#from timer import timer_thread

def checkIfInRange(value, min, max):
    print("Value is not comprised within {} and {}", min, max)
    return value >= min and value <= max

def timer_thread(stim_time, rest_time, repetitions):
    start_time = time.time()
    running = True

    while running:
        event, values = window.read(timeout=100)  # Check for button events every 100ms


        if event == sg.WIN_CLOSED or event == 'Exit':
            running = False
        elif event == 'Stop':
            running = False


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    layout = [control_column, [sg.VSeparator()], stimulation_column,
              [sg.VSeperator()], sound_column,
              [sg.VSeperator()], light_column]

    # Create the window
    window = sg.Window("LightCore Tone Generator", layout, size=(900,500))

    # Create an event loop
    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break
        if event == "Start":
            threading.Thread(target=timer_thread(int(values['-STIM_TIME-']), int(values['-REST_TIME-']),
                                                     int(values['-REPETITIONS-'])), daemon=True).start()
            sendStartPacket(values)
        if event == "Stop":
            sendStopPacket(values)

    window.close()

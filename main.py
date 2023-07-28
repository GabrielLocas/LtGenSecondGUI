
import PySimpleGUI as sg
import threading
import time

from comm import sendStartPacket, sendStopPacket
from layout import stimulation_column, light_column, sound_column, control_column
#from timer import timer_thread

def checkIfInRange(value, min, max):
    print("Value is not comprised within {} and {}", min, max)
    return value >= min and value <= max

running = False

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    layout = [control_column, [sg.VSeparator()], stimulation_column,
              [sg.VSeperator()], sound_column,
              [sg.VSeperator()], light_column]

    # Create the window
    window = sg.Window("LightCore Tone Generator", layout, size=(900,500))

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
                print("stim time!")
            print("STOP!")
            start_time = time.time()
            sendStopPacket(values)
            while (time.time() - start_time < rest_time and running):
                event, values = window.read(timeout=100)

                if event == sg.WIN_CLOSED or event == 'Stop':
                    running = False
                print("rest time!")
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
            t1 = threading.Thread(target=timer_thread(values), daemon=True)
            t1.start()

    window.close()

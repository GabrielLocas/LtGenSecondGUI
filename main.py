

import PySimpleGUI as sg
import time
import serial
import glob
import sys

def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


# Setup configuration of display

control_column = [

    #[sg.Combo([])]

    [sg.Button("Start")],

    [sg.Button("Stop")],

    [sg.Checkbox("Random")]
]

stimulation_column = [
    [sg.Text("Stimulation time (s)"), sg.InputText()],

    [sg.Text("Rest time (s)"), sg.InputText()],

    [sg.Text("Repetitions"), sg.InputText()],
]

sound_column = [
    #[sg.Combo([])],

    [sg.Text("Pitch (Hz)"), sg.InputText()],

    [sg.Text("Volume Intensity (%)"), sg.InputText()],
]

light_column = [
    [sg.Text("Stimulation frequency (Hz)"), sg.InputText()],

    [sg.Text("Duty cycle (%)"), sg.InputText()],

    [sg.Text("Light Intensity (%)"), sg.InputText()],
]

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    layout = [control_column, stimulation_column, sound_column, light_column, [sg.Button("OK")]]

    print(serial_ports())

    # Create the window
    window = sg.Window("LightCore Tone Generator", layout)



    # Create an event loop
    while True:
        event, values = window.read()
        # End program if user closes window or
        # presses the OK button
        if event == "OK" or event == sg.WIN_CLOSED:
            break

    window.close()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

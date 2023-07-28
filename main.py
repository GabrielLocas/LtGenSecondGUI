
import PySimpleGUI as sg
import time
import serial
import glob
import sys
import struct
import threading
from comm import sendStartPacket, sendStopPacket

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

def checkIfInRange(value, min, max):
    print("Value is not comprised within {} and {}", min, max)
    return value >= min and value <= max

# Setup configuration of display
control_column = [

    [sg.Combo(values=serial_ports(), key='-PORT-')],

    [sg.Button("Start")],

    [sg.Button("Stop")],

    [sg.Checkbox("Random", key='-RANDOM-')]
]

stimulation_column = [
    [sg.Text("Stimulation time (s)"), sg.Input(key='-STIM_TIME-', default_text='5')],

    [sg.Text("Rest time (s)"), sg.InputText(key='-REST_TIME-', default_text='5')],

    [sg.Text("Repetitions"), sg.InputText(key='-REPETITIONS-', default_text='1')],
]

wave_forms = ['sine', 'triangle', 'square', 'saw']

sound_column = [
    [sg.Combo(values=wave_forms, key='-WAVE_FORM-')],

    [sg.Text("Pitch (Hz)"), sg.InputText(key='-PITCH-', default_text='1000')],

    [sg.Text("Volume Intensity (%)"), sg.InputText(key='-VOLUME-', default_text='50')],
]

light_column = [
    [sg.Text("Stimulation frequency (Hz)"), sg.InputText(key='-STIM_FREQ-', default_text='20')],

    [sg.Text("Duty cycle (%)"), sg.InputText(key='-DUTY_CYCLE-', default_text='50')],

    [sg.Text("Light Intensity (%)"), sg.InputText(key='-LIGHT-', default_text='100')],
]

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
            sendStartPacket(values)
        if event == "Stop":
            sendStopPacket(values)

    window.close()


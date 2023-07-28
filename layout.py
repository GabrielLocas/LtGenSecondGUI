
import PySimpleGUI as sg
from comm import serial_ports

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
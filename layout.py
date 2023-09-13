
import PySimpleGUI as sg
from comm import serial_ports

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

image_path = 'falloutGuyRescaled.png'

sg.theme_add_new('Fallout 3 Terminal', fallout_3_terminal_theme)
sg.theme('Fallout 3 Terminal')
sg.set_options(font=('Courier New', 14))

# Setup configuration of display
control_column = [
    [
        sg.Column([[sg.Combo(values=serial_ports(), key='-PORT-', size=(10,1))],
            [sg.Button("Start")],
            [sg.Button("Stop")],
            [sg.Checkbox("Random", key='-RANDOM-')]], expand_x=True, justification='left'),
        sg.Column([[sg.Image(filename=image_path)]], justification='right')
    ]
]

stimulation_column = [
    [
        sg.Column([[sg.Text("Stimulation time (s)")], [sg.Text("Rest time (s)")], [sg.Text("Repetitions")]],
                  expand_x=True, justification='left'),
        sg.Column([[sg.Input(key='-STIM_TIME-', default_text='5',  size=(10,1))],
            [sg.InputText(key='-REST_TIME-', default_text='5',  size=(10,1))],
            [sg.InputText(key='-REPETITIONS-', default_text='1',  size=(10,1))]], justification='right')
    ]
]

wave_forms = ['sine', 'triangle', 'square', 'saw']

sound_column = [
    [
        sg.Column([[sg.Text("Wave type : ")], [sg.Text("Pitch (Hz) : ")], [sg.Text("Volume Intensity (%) : ")]],
                  expand_x=True, justification='left'),
        sg.Column([[sg.Combo(values=wave_forms, key='-WAVE_FORM-', default_value= 'sine')],
            [sg.InputText(key='-PITCH-', default_text='10000',  size=(10,1))],
            [sg.InputText(key='-VOLUME-', default_text='50', size=(10, 1))]], justification='right')
    ]
]

light_column = [
    [
        sg.Column([[sg.Text("Stimulation frequency (Hz)")], [sg.Text("Duty cycle (%)")], [sg.Text("Light Intensity (%)")]],
                  expand_x=True, justification='left'),
        sg.Column([[sg.InputText(key='-STIM_FREQ-', default_text='20',  size=(10,1))],
            [sg.InputText(key='-DUTY_CYCLE-', default_text='50',  size=(10,1))],
            [sg.InputText(key='-LIGHT-', default_text='100',  size=(10,1))]], justification='right')
    ]
]

def is_valid_stim_freq(value):
    try:
        int_value = int(value)
        if 1 <= int_value <= 255:
            return True
    except ValueError:
        pass
    return False

def is_valid_pitch(value):
    try:
        int_value = int(value)
        if 1000 <= int_value <= 65535:
            return True
    except ValueError:
        pass
    return False

def is_valid_duty_cycle(value):
    try:
        int_value = int(value)
        if 0 <= int_value <= 100:
            return True
    except ValueError:
        pass
    return False

def is_valid_stim_time(value):
    try:
        int_value = int(value)
        if 1 <= int_value <= 3600:
            return True
    except ValueError:
        pass
    return False

def is_valid_rest_time(value):
    try:
        int_value = int(value)
        if 0 <= int_value <= 3600:
            return True
    except ValueError:
        pass
    return False

def is_valid_repetitions(value):
    try:
        int_value = int(value)
        if 1 <= int_value <= 100:
            return True
    except ValueError:
        pass
    return False

def is_valid_volume(value):
    try:
        int_value = int(value)
        if 0 <= int_value <= 100:
            return True
    except ValueError:
        pass
    return False

def is_valid_light(value):
    try:
        int_value = int(value)
        if 0 <= int_value <= 100:
            return True
    except ValueError:
        pass
    return False

def check_values(values):
    error_string = 'Invalid input(s)! Check these values : \n'
    chill = True
    if not is_valid_stim_time(values['-STIM_TIME-']):
        error_string += ('Stimulation time : (1 to 3600) \n')
        chill = False
    if not is_valid_rest_time(values['-REST_TIME-']):
        error_string += ('Rest time : (0 to 3600) \n')
        chill = False
    if not is_valid_repetitions(values['-REPETITIONS-']):
        error_string += ('Repetitions : (1 to 100) \n')
        chill = False
    if not is_valid_pitch(values['-PITCH-']):
        error_string += ('Pitch : (1000 to 65335) \n')
        chill = False
    if not is_valid_volume(values['-VOLUME-']):
        error_string += ('Volume intensity : (0 to 100) \n')
        chill = False
    if not is_valid_stim_freq(values['-STIM_FREQ-']):
        error_string += ('Stimulation frequency : (1 to 255) \n')
        chill = False
    if not is_valid_duty_cycle(values['-DUTY_CYCLE-']):
        error_string += ('Duty cycle : (1 to 100) \n')
        chill = False
    if not is_valid_light(values['-LIGHT-']):
        error_string += ('Light intensity : (0 to 100) \n')
        chill = False
    if not chill:
        sg.Popup(error_string)
    return chill

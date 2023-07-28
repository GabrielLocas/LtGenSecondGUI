
import serial

wave_forms = ['sine', 'triangle', 'square', 'saw']
def sendStartPacket(values):
    wave_type = wave_forms.index(values['-WAVE_FORM-'])
    pitch = int(values['-PITCH-'])
    pitch_1 = (pitch & 0xFF00) >> 8
    pitch_2 = pitch & 0x00FF
    stim_freq = int(values['-STIM_FREQ-'])
    duty_cycle = int(values['-DUTY_CYCLE-'])
    random = int(values['-RANDOM-'])
    sound_intensity = int(values['-VOLUME-'])
    light_intensity = int(values['-LIGHT-'])
    packet_list = [wave_type, pitch_1, pitch_2, stim_freq, duty_cycle, random, sound_intensity, light_intensity]
    packet = bytearray(packet_list)
    ser = serial.Serial(values['-PORT-'], 115200)
    #ser.write(packet)
    print(packet)
    return
def sendStopPacket(values):
    ser = serial.Serial(values['-PORT-'], 115200)
    #ser.write(bytearray([0x01,0x00,0x10,0x10,0,0,0,0]))
    return
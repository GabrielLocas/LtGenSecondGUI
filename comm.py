
import serial
import sys

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
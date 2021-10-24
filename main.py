import pyaudio
import numpy
import math
import struct
import time

SR = 44100  # Sample Rate

def play_sound(type, frequency, volume, duration):
   generate_sound(type, frequency, volume, duration)

def generate_sound(type, frequency, volume, duration):
    outbuf = numpy.random.normal(loc=0, scale=1, size=int(float(duration / 1000.0)*SR))

    dur = int(SR * float(duration / 1000.0))
    theta = 0.0
    incr_theta = frequency * 2 * math.pi / SR

    if type == "sine":
        for i in range(dur):
            outbuf[i] = volume * math.sin(theta)
            theta += incr_theta
    elif type == "square":
        for i in range(dur):
            if math.sin(theta) > 0:
                outbuf[i] = volume
            else:
                outbuf[i] = 0
            theta += incr_theta
    elif type == "triangle":
        incr_theta /= math.pi
        rising = True
        for i in range(dur):
            if theta < 1 and rising:
                outbuf[i] = volume * theta
                theta += incr_theta
                if theta >= 1:
                    rising = False
            else:
                outbuf[i] = volume * theta
                theta -= incr_theta
                if theta <= 0:
                    rising = True

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32, channels=1, rate=SR, output=True)
    data = b''.join(struct.pack('f', samp) for samp in outbuf)
    stream.write(data)
    stream.stop_stream()
    stream.close()
    p.terminate()

def az_to_br(char):
    char = char.lower()

    # I don't think Python has a more graceful way to do this...
    switch = {
        'a': "40",
        'b': "60",
        'c':  "44",
        'd':  "46",
        'e':  "42",
        'f':  "64",
        'g':  "66",
        'h':  "62",
        'i':  "24",
        'j':  "26",
        'k':  "50",
        'l':  "70",
        'm':  "54",
        'n':  "56",
        'o':  "52",
        'p':  "74",
        'q':  "76",
        'r':  "72",
        's':  "34",
        't':  "36",
        'u':  "51",
        'v':  "71",
        'w':  "27",
        'x':  "55",
        'y':  "57",
        'z':  "53",
        '#':  "17",
        '1':  "40",
        '2':  "60",
        '3':  "44",
        '4':  "46",
        '5':  "42",
        '6':  "64",
        '7':  "66",
        '8':  "62",
        '9':  "24",
        '0':  "26"
    }
    return switch.get(char, "00")

# Remove microtones (A#, C#, etc.)
# ONLY currently worked on base-A
def rm_micro(note):
    if(note == 1): note = 2
    elif(note == 2): note = 3
    elif(note == 3): note = 5
    elif(note == 4): note = 7
    elif(note == 5): note = 8
    elif(note == 6): note = 10

    return note;

# Each octave up of the same note is double the frequency
# A1 is the lowest tolerated by this program
A1 = 55.00
def base_to_freq(note, octave):
    note = note.upper()
    if note == 'A':
        return A1 * pow(2.00, (octave - 1))
    else:
        note = rm_micro(ord(note) - ord('A'))
        return (A1 * pow(2.00, (octave - 1))) * pow(2.00, note/12.00)

def note_to_freq(diff, base):
    return (base * pow(2, (rm_micro(int(diff)-1) / 12)))

def play_sequence(input, base):
    for i in range(len(input)):
        char = az_to_br(input[i])
        for j in range(2):
            if(char[j] == '0'):
                time.sleep(0.1)
            else:
                play_sound("square", note_to_freq(int(char[j]), base), 0.8, 100)
        time.sleep(0.1)

# Main test
baseParam = "A2"
message = "hello world"

base = base_to_freq(baseParam[0], int(baseParam[1]))
play_sequence(message, base)

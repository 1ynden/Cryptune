import pyaudio
import numpy
import math
import struct
import time
import sys
import scipy.io.wavfile as wav
from os.path import exists

SR = 44100  # Sample Rate

MODES = ["sine", "square", "triangle"]

def play_sound(type, frequency, volume, duration, fname):
   generate_sound(type, frequency, volume, duration, fname)

def generate_sound(type, frequency, volume, duration, fname):
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

    if(fname == "null"):
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paFloat32, channels=1, rate=SR, output=True)
        data = b''.join(struct.pack('f', samp) for samp in outbuf)
        stream.write(data)
        stream.stop_stream()
        stream.close()
        p.terminate()
    else:
        wav.write(fname, SR, outbuf)

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

def play_sequence(input, base, type, fname):
    for i in range(len(input)):
        char = az_to_br(input[i])
        for j in range(2):
            if(char[j] == '0'):
                time.sleep(0.1)
            else:
                play_sound(type, note_to_freq(int(char[j]), base), 0.8, 100, fname)
        time.sleep(0.1)

def welcome():
    print("  ______     ______     __  __     ______   ______   __  __     __   __     ______    ")
    print(" /\  ___\   /\  == \   /\ \_\ \   /\  == \ /\__  _\ /\ \/\ \   /\ *-.\ \   /\  ___\   ")
    print(" \ \ \____  \ \  __<   \ \____ \  \ \  _-/ \/_/\ \/ \ \ \_\ \  \ \ \-.  \  \ \  __\_  ")
    print("  \ \_____\  \ \_\ \_\  \/\_____\  \ \_\      \ \_\  \ \_____\  \ \_\\*\__\  \ \_____\ ")
    print("   \/_____/   \/_/ /_/   \/_____/   \/_/       \/_/   \/_____/   \/_/ \/_/   \/_____/ ")
    print("\n Welcome to Cryptune. The command line arguments (which come after \"main.py\") are as follows: \n")
    print("\t -d: Force run with default settings.")
    print("\t -e: Export to wav file. Duplicates will be numbered.")
    print("\t -m: Set message. Default = hello world")
    print("\t -o: Manually set octave. Default = 2")
    print("\t -w: Set wave type. Default = sine; Options = sine, square, triangle")
    print("\n For more detailed information, visit https://github.com/1ynden/Cryptune")

# Fallback values for entry
baseParam = 2
wave = "square"
message = "hello world"
export = "null"

if(len(sys.argv) != 1):
    if(sys.argv[1] == "-h"):
        welcome()
    elif(sys.argv[1] == "-d"):
        play_sequence(message, base_to_freq('A', baseParam), wave, export)
    else:
        while(len(sys.argv) > 2):
            if(sys.argv[1] == "-o"):
                if(int(sys.argv[2]) > 0):
                    if(int(sys.argv[2]) < 7):
                        baseParam = int(sys.argv[2])
                    else:
                        print("Octave can't (shouldn't) be over 7. Defaulting to 7.")
                        baseParam = 7
                else:
                    print("The octave cannot be 0 or lower. Defaulting to 1.")
                    baseParam = 1
            elif(sys.argv[1] == "-m"):
                message = sys.argv[2]
            elif(sys.argv[1] == "-w"):
                if(sys.argv[2] in MODES):
                    wave = sys.argv[2]
                else:
                    print("Invalid wave type. Defaulting to square.")
                    wave = "square"
            elif(sys.argv[1] == "-e"):
                if(exists(sys.argv[2] + ".wav")):
                    vnum = 1
                    export = sys.argv[2] + "(1).wav"
                    while(exists(export)):
                        vnum += 1
                        export = sys.argv[2] + ("(%d)" %  vnum) + ".wav"
                else:
                    export = sys.argv[2] + ".wav"
            else:
                print("Invalid argument token entered. Type \"python main.py\" to see proper arguments.")
            del sys.argv[1]
            del sys.argv[1]
        if(len(sys.argv) == 2):
            print("An invalid number of arguments were entered. \n Proceeding with those that have been processed, otherwise default settings.")
        play_sequence(message, base_to_freq('A', baseParam), wave, export)
else:
    welcome()


#base = base_to_freq(baseParam[0], int(baseParam[1]))
#play_sequence(message, base)

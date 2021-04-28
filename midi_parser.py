from mido import MidiFile
from mido import tick2second

def note2freq(x):
    """
        Convert a MIDI note into a frequency (given in Hz)
    """
    a = 110
    return (a/32) * (2 ** ((x-9)/12))


mid = MidiFile('') #midi file to parse
ticks_per_beat = mid.ticks_per_beat

for i, track in enumerate(mid.tracks):
    tempo = DEFAULT_TEMPO

    totaltime = 0
    print("Track: " + str(i))

    prev_freq = 0
    j = 0

    for message in track:
        t = ticks2s(message.time, tempo, mid.ticks_per_beat)
        totaltime += t

        if isinstance(message, MetaMessage):  # Tempo change
            if message.type == "set_tempo":
                tempo = message.tempo / 10**6
            elif message.type == "end_of_track":
                pass
            else:
                print(str(message))
        else:  # Note
            if message.type == "control_change" or \
               message.type == "program_change":
                pass

            elif message.type == "note_on" or message.type == "note_off":
                freq = note2freq(message.note)
                if message.velocity == 0:
                    freq = 0
                if (tick2second(message.time, 0.480, ticks_per_beat) != 0):
                    print(".word", round(prev_freq), ", ", round(tick2second(message.time, 0.480, ticks_per_beat)))
                    j += 1
                prev_freq = freq
            else:
                print(message)
    print("Length of array:", j)
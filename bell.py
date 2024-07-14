from machine import Pin, PWM
import math
import time


class Note:
    def __init__(self, letter, octave=6, length=0.5):
        self.letter = letter
        self.octave = octave
        self.length = length


class Bell:
    def __init__(self, pin_num):
        self.buzzer = PWM(Pin(pin_num))
        self.buzzer.duty_u16(0)
        self.playing = False

    def distance_from_a(note):
        distance = -2 * (
            (ord("H") if ord(note[0]) > ord("B") else ord("A")) - ord(note[0])
        )
        if ord(note[0]) < ord("F") and ord(note[0]) > ord("B"):
            distance += 1

        if len(note) > 1:
            if note[1] == "#":
                distance -= 1 if distance > 0 else -1
            else:
                distance += 1 if distance > 0 else -1
        return distance

    def note_to_frequency(note):
        return int(
            440
            * math.pow(
                2, (Bell.distance_from_a(note.letter) + 12 * (note.octave - 4)) / 12
            )
        )

    def play_note(self, note):
        if self.playing:
            return
        self.playing = True
        self.buzzer.freq(Bell.note_to_frequency(note))
        self.buzzer.duty_u16(32768)
        time.sleep(note.length)
        self.stop()

    def play(self):
        if self.playing:
            return
        # Classic Bell Tower type of thing
        # song = ['E', 'C', 'D', ('G', 5), ('G', 5), 'D', 'E', 'C']
        # Megalovania
        song = [
            ("D", 4, 0.2),
            ("D", 4, 0.2),
            ("D", 5, 0.4),
            ("A", 4, 0.6),
            ("G#", 4, 0.4),
            ("G", 4, 0.4),
            ("F", 4, 0.4),
            ("D", 4, 0.2),
            ("F", 4, 0.2),
            ("G", 4, 0.2),
        ]
        for position, key in enumerate(song):
            note = Note(*key)
            # If it is the same note consecutively, you don't want it to blend so add a gap
            if position < len(song) - 1 and Bell.note_to_frequency(
                note
            ) == Bell.note_to_frequency(Note(*song[position + 1])):
                note.length *= 1 / 2
                self.play_note(note)
                time.sleep(1 / 2 * note.length)
            else:
                self.play_note(note)

    def stop(self):
        self.buzzer.duty_u16(0)
        self.playing = False
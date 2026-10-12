"""Procedurally generated sound effects (no audio files needed)."""
import array
import math
import random

import pygame

SAMPLE_RATE = 44100


def _to_sound(samples):
    buf = array.array("h", samples)
    return pygame.mixer.Sound(buffer=buf.tobytes())


def _slice_sound():
    # Short high-pitched "swish": noise + rising tone, fast decay
    n = int(SAMPLE_RATE * 0.15)
    out = []
    for i in range(n):
        t = i / n
        env = (1 - t) ** 2
        tone = math.sin(2 * math.pi * (900 + 1500 * t) * i / SAMPLE_RATE)
        noise = random.uniform(-1, 1)
        out.append(int(12000 * env * (0.6 * tone + 0.4 * noise)))
    return _to_sound(out)


def _bomb_sound():
    # Low rumbling explosion: decaying noise + low sine
    n = int(SAMPLE_RATE * 0.6)
    out = []
    for i in range(n):
        t = i / n
        env = (1 - t) ** 1.5
        tone = math.sin(2 * math.pi * (110 - 70 * t) * i / SAMPLE_RATE)
        noise = random.uniform(-1, 1)
        out.append(int(20000 * env * (0.5 * tone + 0.5 * noise)))
    return _to_sound(out)


def _game_over_sound():
    # Sad descending three-note jingle
    notes = [392.0, 330.0, 262.0]
    out = []
    for freq in notes:
        n = int(SAMPLE_RATE * 0.28)
        for i in range(n):
            t = i / n
            env = min(1.0, t * 20) * (1 - t * 0.6)
            out.append(int(11000 * env * math.sin(2 * math.pi * freq * i / SAMPLE_RATE)))
    return _to_sound(out)


class Sounds:
    """Holds the sound effects. Silently does nothing if audio is unavailable."""

    def __init__(self):
        self.enabled = False
        self.slice = self.bomb = self.game_over = None
        try:
            pygame.mixer.quit()
            pygame.mixer.init(frequency=SAMPLE_RATE, size=-16, channels=1)
            self.slice = _slice_sound()
            self.bomb = _bomb_sound()
            self.game_over = _game_over_sound()
            self.enabled = True
        except pygame.error:
            print("Audio unavailable - running without sound.")

    def play(self, name):
        if self.enabled:
            sound = getattr(self, name, None)
            if sound:
                sound.play()

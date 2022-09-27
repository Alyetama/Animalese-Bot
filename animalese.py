#!/usr/bin/env python
# coding: utf-8
"""Source: https://www.youtube.com/watch?v=IKMjg2fEGgE"""

import hashlib
import string
from pathlib import Path
from typing import Optional, Tuple, Union

from pydub import AudioSegment
from pydub.playback import play


class Animalese:

    def __init__(self,
                 sentence: str = 'Hello, World!',
                 speed: Union[float, int] = 2.5,
                 bebebese: str = 'bebebese_slow',
                 swear_words: list = ['fuck', 'shit'],
                 speak: bool = True) -> None:
        self.sentence = sentence
        self.speed = speed
        self.bebebese = bebebese
        self.swear_words = swear_words
        self.speak = speak

    def build_sentence(self) -> AudioSegment:
        print(f'Translating: {self.sentence}')
        sentence_wav = AudioSegment.empty()
        self.sentence = self.sentence.lower()

        for word in self.swear_words:
            self.sentence = self.sentence.replace(word, '*' * len(word))

        while '(' in self.sentence or ')' in self.sentence:
            start = self.sentence.index('(')
            end = self.sentence.index(')')
            self.sentence = self.sentence[:start] + '*' * (
                end - start) + self.sentence[end + 1:]

        digraphs = ['ch', 'sh', 'ph', 'th', 'wh']
        i = 0

        while (i < len(self.sentence)):
            char = None
            if (i < len(self.sentence) - 1) and (
                (self.sentence[i] + self.sentence[i + 1]) in digraphs):
                char = self.sentence[i] + self.sentence[i + 1]
                i += 1
            elif self.sentence[i] in string.ascii_lowercase + string.digits:
                char = self.sentence[i]
            elif self.sentence[i] in string.punctuation:
                char = self.bebebese
            i += 1

            if char != None and char not in string.digits:
                new_segment = AudioSegment.from_wav(f'letters/{char}.wav')
                sentence_wav += new_segment
        return sentence_wav

    def change_playback_speed(self, sound: AudioSegment) -> AudioSegment:
        sound_with_altered_frame_rate = sound._spawn(
            sound.raw_data,
            overrides={'frame_rate': int(sound.frame_rate * self.speed)})
        return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)

    def to_sound(
        self,
        export: bool = False,
        export_to: Optional[str] = None
    ) -> Tuple[AudioSegment, Optional[Path]]:
        sound = self.build_sentence()
        sound_with_altered_frame_rate = sound._spawn(
            sound.raw_data,
            overrides={'frame_rate': int(sound.frame_rate * self.speed)})
        sound = sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)

        if self.speak:
            play(sound)
        file_path = None

        if export:
            if not export_to:
                export_to = Path('.')
            else:
                export_to = Path(export_to)
            fname = hashlib.md5(
                (self.sentence +
                 str(self.speed)).encode()).hexdigest() + '.wav'
            file_path = export_to / fname
            sound.export(file_path, format='wav')
            print(f'Exported to: {file_path}')
        return sound, file_path

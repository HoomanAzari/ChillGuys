import speech_recognition as sr
from os import path
from enum import Enum


class VoiceToText:

    class Trancriber(Enum):
        SPHYNX = 0
        GOOGLE_API = 1

    instance: type("VoiceToText") = None

    @staticmethod
    def get_instance() -> type("VoiceToText"):
        if VoiceToText.instance is None:
            VoiceToText.instance = VoiceToText()
        return VoiceToText.instance

    def __init__(self):
        self.recognizer = sr.Recognizer()

    def transcribe_audio_file(self, audio_file_path: str,
                              transcriber: Trancriber) -> str:
        with sr.AudioFile(audio_file_path) as src:
            audio = self.recognizer.record(src)
        res = None
        if transcriber == VoiceToText.Trancriber.SPHYNX:
            res = self.recognizer.recognize_sphinx(audio)
        elif transcriber == VoiceToText.Trancriber.GOOGLE_API:
            res = self.recognizer.recognize_google(
                audio,
                language='en-ca',
                # show_all=True
            )
        return res.lower()


def main():
    instance: VoiceToText = VoiceToText.get_instance()
    filename = "test.wav"
    try:
        res = instance.transcribe_audio_file(
            filename, transcriber=VoiceToText.Trancriber.GOOGLE_API)
    except:
        print("Can't use google for some reason")
        res = instance.transcribe_audio_file(
            filename, transcriber=VoiceToText.Trancriber.SPHYNX)
    print(res)


if __name__ == "__main__":
    main()

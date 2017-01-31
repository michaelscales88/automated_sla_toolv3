import speech_recognition as sr
import errno
from os import remove


class AudioTranscription(object):

    @staticmethod
    def transcribe(wav_files):
        r = sr.Recognizer()
        for wav_file in wav_files:
            with sr.AudioFile(wav_file) as source:
                audio = r.record(source)  # read the entire audio file

                try:
                    trans_text = ("Google Cloud Speech thinks you said:\n"
                                  "{speech}".format(speech=r.recognize_google_cloud(audio)))
                except sr.UnknownValueError:
                    print("Google Cloud Speech could not understand audio")
                except sr.RequestError as e:
                    print("Could not request results from Google Cloud Speech service; {0}".format(e))
                else:
                    AudioTranscription.del_read_file(filename=wav_file)
                    yield (trans_text)

    @staticmethod
    def del_read_file(filename):
        try:
            remove(filename)
        except OSError as e:
            if e.errno != errno.ENOENT:  # errno.ENOENT = no such file or directory
                raise

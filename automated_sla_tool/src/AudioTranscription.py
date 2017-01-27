import speech_recognition as sr


class AudioTranscription(object):

    @staticmethod
    def transcribe(wav_files):
        r = sr.Recognizer()
        # for wav_file in wav_files:
        for wav_file in wav_files[:1]:
            print(wav_file)
            print(type(wav_file))
            with sr.AudioFile(wav_file) as source:
                audio = r.record(source)  # read the entire audio file

                # recognize speech using Google Cloud Speech
                try:
                    trans_text = ("Google Cloud Speech thinks you said:\n"
                                  "{speech}".format(speech=r.recognize_google_cloud(audio)))
                    print(trans_text)
                except sr.UnknownValueError:
                    print("Google Cloud Speech could not understand audio")
                except sr.RequestError as e:
                    print("Could not request results from Google Cloud Speech service; {0}".format(e))
                else:
                    yield (trans_text)

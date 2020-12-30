#/usr/bin/python3
import speech_recognition as sr

r = sr.Recognizer()

with sr.Microphone() as source:
    print('running...')
    audio = r.listen(source)
    voice_data = r.recognize_google(audio)
    print(voice_data)
#/usr/bin/python3
import speech_recognition as sr
import playsound
import os, random
from gtts import gTTS
from time import ctime

r = sr.Recognizer()
NAME = "Ant"


'''
speech to text
'''
def record_command():
    with sr.Microphone() as source:
        audio = r.listen(source)
        voice_data = ''
        try:
            voice_data = r.recognize_google(audio)
        except sr.UnknownValueError:
            print('Sorry I did not understand that command')
        except sr.RequestError:
            print('Sorry my service is unavailable')
        return voice_data

'''
business logic
'''
def process_command(voice_data: str):
    if 'what is your name' in voice_data:
        speak(f"My name is {NAME}")
    if 'what time is it' in voice_data:
        speak(f"The current time is {ctime()}")
    if 'stop' in voice_data or 'shut down' in voice_data:
        speak('Goodbye!')
        exit()

def speak(audio_string: str):
    print(f'speaking: {audio_string}')
    tts = gTTS(text=audio_string, lang='en')
    r = random.randint(1,1000000)
    audio_file = f'audio-{r}.mp3'
    tts.save(audio_file)
    playsound.playsound(audio_file)
    os.remove(audio_file)


def handler():
    speak("How can I assist you?")
    while True:
        voice_data = record_command()
        #print(f"you asked: {voice_data}")
        process_command(voice_data)

if __name__ == '__main__':
    handler()

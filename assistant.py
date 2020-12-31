import speech_recognition as sr
import playsound
import os, random
from gtts import gTTS
from time import ctime

#recording instance
r = sr.Recognizer()

class Assistant:

    def __init__(self):
        self.Name = 'Ant'
        self.speak(f'Hi, my name is {self.Name}. How may I assist you?')

    '''
    speech to text
    '''
    def record_command(self):
        #global r
        with sr.Microphone() as source:
            audio = r.listen(source)
            voice_data = ''
            try:
                voice_data = r.recognize_google(audio)
            except sr.UnknownValueError:
                self.speak('Sorry I did not understand that command')
            except sr.RequestError:
                self.speak('Sorry my service is unavailable')
            return voice_data

    '''
    Text to speech
    '''
    def speak(self, audio_string: str):
        print(f'speaking: {audio_string}')
        tts = gTTS(text=audio_string, lang='en')
        rand = random.randint(1,1000000)
        audio_file = f'audio-{self.Name}-{rand}.mp3'
        tts.save(audio_file)
        playsound.playsound(audio_file)
        os.remove(audio_file)

    '''
    business logic
    '''
    def process_command(self, voice_data: str):
        if 'what is your name' in voice_data:
            self.speak(f"My name is {self.Name}")
        if 'what time is it' in voice_data:
            self.speak(f"The current time is {ctime()}")
        if 'exit' in voice_data or 'shut down' in voice_data:
            self.speak('Goodbye!')
            # return false? tells to end?
            return False
            #exit()
        return True
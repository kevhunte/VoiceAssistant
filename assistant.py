import speech_recognition as sr
import playsound
import os, random, json
from gtts import gTTS
from time import ctime, time
from datetime import datetime, timedelta

#recording instance
mic = sr.Recognizer()

class Assistant:

    '''
    Initializes instance with configuration file. Base is empty, but can be customized over time
    '''
    def __init__(self, config: str):
        self.config_file_name = config
        with open(self.config_file_name, 'r') as f:
            self.config_data = json.load(f)
        self.__process_config()
        self.speak(f'Hi, my name is {self.Name}. How may I assist you?')

    '''
    takes stored values and sets members of instance
    '''
    def __process_config(self):
        self.Name = 'Ant' if not self.config_data['name']['value'] else self.config_data['name']['value']

    '''
    writes changes in memory back to file
    '''
    def __save_config(self):
        with open(self.config_file_name, 'w') as f:
            self.config_data['last_modified_date'] = ctime()
            json.dump(self.config_data, f,sort_keys=True, indent=4)

    '''
    Allows user to edit and overwrite the config.json file
    '''
    def __edit_config(self):
        options = ', '.join([key for (key, val) in self.config_data.items() if isinstance(val,dict) and val.get('allow_modification') is True])
        self.speak('The following options can be changed. ')
        self.speak(options)
        self.speak('What would you like to edit?')
        choice = self.record_command()
        self.speak(f"What should the new {choice} be?")
        new_value = self.record_command()
        # set value in configs dict. Make sure not to rewrite structure
        if 'name' in choice.lower():
            self.__set_config_in_memory('name',new_value)
            self.Name = new_value
        
        self.speak(f'Saving {new_value} as {choice}')
        self.__save_config()

    '''
    Safely rewrites value in dict
    '''
    def __set_config_in_memory(self, key: str, val):
        self.config_data[key]['value'] = val

    '''
    speech to text
    '''
    def record_command(self):
        print('listening...')
        with sr.Microphone() as source:
            audio = mic.listen(source)
            voice_data = ''
            try:
                voice_data = mic.recognize_google(audio)
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
        audio_file = f'audio-{rand}.mp3'
        tts.save(audio_file)
        playsound.playsound(audio_file)
        os.remove(audio_file)

    def read_reminders(self):
        if 'reminders' not in self.config_data or self.config_data['reminders'] is None:
            self.speak("You currently have no reminders")
            if 'reminders' not in self.config_data:
                self.config_data['reminders'] = []
                self.__save_config()
        else:
            self.speak('Here is what I have saved')
            current = time()
            expired = list(filter(lambda x: x['due_date'] < current,self.config_data['reminders']))
            for reminder in self.config_data['reminders']:
                self.speak(f"{reminder['name']}")
                self.speak(f"Due on {Assistant.gettime(reminder['due_date'])}")
            if expired:
                self.speak('There are expired items in this list.') 
                self.speak('Would you like to delete them')
                choice = self.record_command()
                self.config_data['reminders'] = list(filter(lambda x: x['due_date'] >= current,self.config_data['reminders'])) if 'yes' in choice.lower() else self.config_data['reminders']
                self.__save_config()
                self.speak('Expired reminders have been deleted')
    
    def set_reminder(self):
        if 'reminders' not in self.config_data:
            self.config_data['reminders'] = []
        today = datetime.today()
        self.speak('Provide a name for the reminder')
        name = self.record_command()
        self.speak('One day, one week, or one month?')
        choice = self.record_command()
        new_date = today
        set_reminder = False
        if 'day' in choice or 'tomorrow' in choice:
            new_date += timedelta(days=1)
            set_reminder = True
        elif 'week' in choice:
            new_date += timedelta(weeks=1)
            set_reminder = True
        elif 'month' in choice:
            new_date += timedelta(weeks=4)
            set_reminder = True
        else:
            self.speak('sorry, I cannot set a reminder for that time')
        if set_reminder:
            reminder = {
                'name': name,
                'due_date': new_date.timestamp()
            }
            self.config_data['reminders'].append(reminder)
            self.__save_config()
            self.speak(f"Saved reminder for {name}")
            

    '''
    business logic
    '''
    def process_command(self, voice_data: str):
        if 'change my settings' in voice_data:
            self.speak('Sure. Opening up configs.')
            self.__edit_config()
        if 'reminders' in voice_data:
            self.speak('Would you like to read, or make a new reminder')
            choice = self.record_command()
            self.set_reminder() if 'edit' in choice or 'set' in choice or 'new' in choice else self.read_reminders()
        if 'what is your name' in voice_data:
            self.speak(f"My name is {self.Name}")
        if 'what time is it' in voice_data:
            self.speak(f"The current time is {Assistant.gettime()}")
        if 'exit' in voice_data or 'shut down' in voice_data:
            self.speak('Goodbye!')
            return False
        return True

    def gettime(string=None):
        val = list(filter(lambda x: ':' not in x, ctime(string).split(' ')))
        processed = ' '.join(val)
        return processed
#/usr/bin/python3

from assistant import Assistant

def handler():
    VA = Assistant(config="config.json")
    running = True
    while running:
        voice_data = VA.record_command()
        running = VA.process_command(voice_data)

if __name__ == '__main__':
    handler()

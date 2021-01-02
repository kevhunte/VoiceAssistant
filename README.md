# Personal Voice Assistant

```
This is built with python 3 => 3.6
```

# Needed libraries
```
---- Speech to text modules ----
pip3 install speechrecognition

pip3 install pyaudio

For macOS, portaudio is needed. Can be installed with "home brew portaudio"

---- Text to Speech modules ----
pip3 install gTTS

pip3 install playsound

pip3 install PyObjC

```

# Usage
```
Run using

python3 main.py
```

# Other findings along the way
```
*.pyc in the git ignore does not seem to work. Use "git rm -f *.pyc" to stop this from being tracked

The config.json will be a possible location of PII. This will not be tracked after updates to the skeleton are made. To do the same after pulling down this repo, run the following command 
"git update-index --assume-unchanged config.json"
```
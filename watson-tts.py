'''SETUP'''
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from pygame import mixer
import time
import pydub
import os

#Set up tts service
apikey = 'ZjBLkQcwPepIti9BlACYCNYmLplKEGtos123-EmzpAPI'
url = 'https://api.us-east.text-to-speech.watson.cloud.ibm.com/instances/3af721c1-295b-4abc-9af1-9484336a6411'
authenticator = IAMAuthenticator(apikey)
tts = TextToSpeechV1(authenticator=authenticator)
tts.set_service_url(url)
#Default voice
v = 4

#Setup output
mixer.init()
mixer.music.set_volume(0.75)

#The voices
#https://cloud.ibm.com/docs/text-to-speech?topic=text-to-speech-voices
voices = [
    ["us-m-Henry", "en-US_HenryV3Voice"],
    ["us-m-Kevin", "en-US_KevinV3Voice"],
    ["us-m-Micheal", "en-US_MichaelV3Voice"],
    ["us-f-Allison", "en-US_AllisonV3Voice"],
    ["us-f-Emily", "en-US_EmilyV3Voice"],
    ["us-f-Lisa", "en-US_LisaV3Voice"],
    ["us-f-Olivia", "en-US_OliviaV3Voice"],
    ["au-m-Craig", "en-AU_CraigVoice"],
    ["au-m-Steve", "en-AU_SteveVoice"],
    ["au-f-Madison", "en-AU_MadisonVoice"],
    ["gb-m-James", "en-GB_JamesV3Voice"],
    ["gb-f-Charlotte", "en-GB_CharlotteV3Voice"],
    ["gb-f-Kate", "en-GB_KateV3Voice"]
]



'''FUNCTIONS'''

#Set voice
def setVoice(voiceid):
    v = voiceid

#Change volume
volume = 0.75
def setVolume(vol):
    global volume
    volume = vol
    mixer.music.set_volume(vol/100)

#Talk
def talk(text):
    with open("buffer.mp3","wb") as buffer:
        res = tts.synthesize(text, accept='audio/mp3', voice=voices[v][1]).get_result().content
        buffer.write(res)
    mixer.music.set_volume(0.01)
    mixer.music.load('buffer.mp3')
    mixer.music.play()
    time.sleep(0.6)
    mixer.music.set_volume(0.75)
    mixer.music.load('buffer.mp3')
    mixer.music.play()
    while mixer.music.get_busy() == True:
        continue

talk("anehasio")
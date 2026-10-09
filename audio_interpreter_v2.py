# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 16:22:35 2026

@author: rowan
"""

import pyaudio
import keyboard
import wave
import time

# Asyncio allows shazam.io to run in Spyder IDE, as it requires the starting of its own event loop, but Spyder starts its own.

import asyncio
import nest_asyncio
nest_asyncio.apply()

from shazamio import Shazam

# %% Initialise pyaudio to use 16-bit signed integer recording
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
OUTPUT_FILENAME = "lastSong.wav"

audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

# Await keyboard press: space to begin recording. Record for 10 seconds, or until space is pressed again, 
# then save clip to OUTPUT_FILENAME. Will replace previous file.

frames = []
print("Press SPACE to start recording.")

keyboard.wait('space')
print("Recording for 10 seconds.")
# In order to prevent debouncing:
time.sleep(0.2)
# Initialise 10 second counter
start_time = time.time()

while True:
    try:
        data = stream.read(CHUNK)
        frames.append(data)
    except KeyboardInterrupt:
        break
    if time.time() - start_time >= 10:
        print("Stopping recording.") 
        time.sleep(0.2)
        break

stream.stop_stream()
stream.close()
audio.terminate()

waveFile = wave.open(OUTPUT_FILENAME, 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(frames)) 
waveFile.close()    

# %% Run Shazam on audio snippet saved to OUTPUT_FILENAME, and return song name and artist name
async def main():

  shazam = Shazam()
  out = await shazam.recognize(OUTPUT_FILENAME)
  print('Song: ', out['track']['title'])
  print('Artist: ', out['track']['subtitle'])

def run_async():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

run_async()
                      
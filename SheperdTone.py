# https://nicechord.com/post/shepard-tone/
# https://stackoverflow.com/questions/8299303/generating-sine-wave-sound-in-python

import numpy as np
import matplotlib.pyplot as plt
import pyaudio
import math
import time
          
PERIOD = 0.5          
SR = 16000
f = 2000
df = 100
groups = 8
GRP_MASK = groups-1
duration = 20

def pyaudio_init():
    pOut = pyaudio.PyAudio()
    streamOut = pOut.open(format = pyaudio.paInt16,channels = 1,rate = SR,output = True) 
    return [pOut, streamOut]
    
def pyaudio_close(pOut, streamOut):
    streamOut.close()
    pOut.terminate()

def pyaudio_play(streamOut,s):
    streamOut.write(s)
    
def signalInit():
    s = []
    t = np.linspace(0, PERIOD, int(SR * PERIOD))
    for i in range(0, groups):
        ss = (0x7FF * np.sin(2* math.pi * (f+i*df) * t)).astype(np.int16)
        s.append(ss)
    return s

def signalMixing(s, idx):
    mixS = s[idx & GRP_MASK] >> 1;
    for i in range(1,8):
        mixS = mixS + (s[(idx+i) & GRP_MASK] >> (i+1))
    return mixS
    
def sheperdToneMixing(streamOut, s):
    startTime = time.time();
    endTime = startTime;
    idx = 0
    while( duration > endTime - startTime):
        mixS = signalMixing(s, idx);
        pyaudio_play(streamOut, mixS)
        idx = idx +1;
        if(idx == groups):
            idx = 0
        endTime = time.time();
        
def mainStart():

    [pOut, streamOut] =  pyaudio_init()
    s = signalInit();
    sheperdToneMixing(streamOut,s)
    pyaudio_close(pOut, streamOut)
    
if __name__ == '__main__':
    mainStart()
    #USB_Audio_Play.realtimeplayback(10)
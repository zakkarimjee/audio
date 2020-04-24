import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

RATE = 44100 # time resolution of the recording device (Hz)
S_RATE = 200# sampling rate (Hz)
CHUNK = int(RATE/S_RATE) # length of a sample chunk
S_RATE = RATE/CHUNK # redefine sample rate based on integer chunk length

L_data = 20*CHUNK


p=pyaudio.PyAudio() # start the PyAudio class
stream=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,
              frames_per_buffer=CHUNK) #uses default input device

# create animation data
sound = np.zeros((L_data))
time = np.arange(L_data)/RATE

# figure
fig = plt.figure(figsize=(8,8))
ax = plt.subplot(111)

line, = ax.plot(time,sound)
ax.set_ylim(-4000,4000)
def update(*args):
    # create a numpy array holding a single read of audio data
    data = np.frombuffer(stream.read(CHUNK,exception_on_overflow=False),dtype=np.int16)
    # shift sound data one chunk to right
    sound[CHUNK:] = sound[:-CHUNK]
    sound[:CHUNK] = data
    line.set_ydata(sound)
    return line


anim = animation.FuncAnimation(fig, update, interval=1000/S_RATE)
plt.show()


# close the stream gracefully
stream.stop_stream()
stream.close()
p.terminate()
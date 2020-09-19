# Import the libs
import librosa
import IPython.display as ipd
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip


filename = "./audio.wav"

# Load the file
x, sr = librosa.load(filename, sr=16000)
int(librosa.get_duration(x, sr) / 60)

# Create chunks for 10 secs
max_slice = 10
window_length = max_slice * sr
a = x[21 * window_length:22 * window_length]
ipd.Audio(a, rate=sr)

# Calculate the energy
energy = sum(abs(a ** 2))
print(energy)

# Calculate the energy for each chunk
energy = np.array([sum(abs(x[i:i + window_length] ** 2)) for i in range(0, len(x), window_length)])

# Plot the above thing
plt.hist(energy)
plt.show()

# Create a df for energy data
df = pd.DataFrame(columns=['energy', 'start', 'end'])
thresh = 180
row_index = 0
for i in range(len(energy)):
    value = energy[i]
    if value >= thresh:
        i = np.where(energy == value)[0]
        df.loc[row_index, 'energy'] = value
        df.loc[row_index, 'start'] = i[0] * 10
        df.loc[row_index, 'end'] = (i[0] + 1) * 10
        row_index = row_index + 1

# create the excitement snippet
temp = []
i = 0
j = 0
n = len(df) - 2
m = len(df) - 1
while (i <= n):
    j = i + 1
    while (j <= m):
        if (df['end'][i] == df['start'][j]):
            df.loc[i, 'end'] = df.loc[j, 'end']
            temp.append(j)
            j = j + 1
        else:
            i = j
            break
df.drop(temp, axis=0, inplace=True)
print(df)

# Generate the highlights from the chunks
start = np.array(df['start'])
end = np.array(df['end'])
for i in range(len(df)):
    if i != 0:
        start_lim = start[i] - 10
    else:
        start_lim = start[i]
    end_lim = end[i]
    filename = "highlight_clips/highlight" + str(i + 1) + ".mp4"
    ffmpeg_extract_subclip("./videofile.mp4", start_lim, end_lim, targetname=filename)

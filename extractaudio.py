import moviepy.editor as mp

clip = mp.VideoFileClip("./videofile.mp4")
clip.audio.write_audiofile("./audio.wav")

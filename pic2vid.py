from moviepy.editor import *
import pydub
from pydub import AudioSegment, silence

pics = "hk_bg.jpg"
aud_p = "1.wav"
aud = AudioSegment.from_wav(aud_p)
#aud = AudioSegment.from_file(aud_p, format=audio_type)
audio_time = aud.duration_seconds

clip = ImageClip(pics)
audclip = AudioFileClip(aud_p)

clip = clip.set_audio(audclip)
clip.set_duration(audio_time).write_videofile("p2v.mp4",fps=30,audio=True)
print('图片配乐视频p2v.mp4已生成')


vid = VideoFileClip("p2v.mp4")
logss = ( ImageClip("logss.png").set_duration(5).margin(right=8,top=8,opacity=0.6).set_pos(('right','top')))
video = CompositeVideoClip([vid,logss])
video.write_videofile("log2v.mp4",codec="libx264",bitrate="10000000")
print('logo2v.mp4生成')

'''
A person who likes but is not good at computer technology such as artificial intelligence
'''
#os.system("ffmpeg -ss 0 -t 30 -f lavfi -i color=c=0x000000:s=1920x1080:r=30 -i " + pics +" -filter_complex "[1:v]scale=1920:1080[v1];[0:v][v1]overlay=0:0[outv]" -map [outv] -c:v libx264 hk2type.mp4 -y")

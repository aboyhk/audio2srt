
# 基于PaddleSpeech的语音识别API做的一个音视频文件生成srt字幕文件的小应用。

*** **脚本说明：Ubuntu20.04 | Python | paddlespeech **
 

PaddleSpeech开源出来的接口能音频识别文字，然而不支持时间码，而字幕文件还需要记录视频里人物说话的时间。这个是用了python的第三方库pydub的静默识别，而要想好一点进行人声分割则可能需要多次调节参数，所以Python执行使用的时候需要注意加上<u>min_silence_len</u>和<u>silence_thresh</u>两个参数值（比如10,-40)。另外这里还有一个是图片配乐视频的脚本，其实原本这两个脚本都只是一个别的功能实现的一部分。


*** 使用方法：**

终端中执行python audio2srt.py 10 -40

应用会提取当前目录下视频文件vid_s.mp4的音频，然后识别语音并输出。

终端中执行pyhon pic2vid.py

应用会以当前目录下的hk_bg.jpg文件为背景，以当前目录下的1.wav为背景乐创建一个时长为1.wav时长的视频。

from typing import Pattern
from moviepy.editor import *
import pydub
from pydub import AudioSegment, silence
import paddle
import re, os, sys
from paddlespeech.cli import ASRExecutor
from paddlespeech.cli import TextExecutor


lst_txt = list()
#存放语音识别后的文本行
m_sil_len = int(sys.argv[1])
sil_th = int(sys.argv[2])
#调节音频文件静默时间处分割（也就是音频中说话断句时间点）的参数


#   m_sil_len = 10
#   sil_th = -40

vid_s_p = "vid_s.mp4"
aud_p = "./tmphk/aud_s.wav"
video = VideoFileClip(vid_s_p)
video.audio.write_audiofile(aud_p)

asr_executor = ASRExecutor()
text = asr_executor(
    model='conformer_wenetspeech',
    lang='zh',
    sample_rate=16000,
    config=None,  # Set `config` and `ckpt_path` to None to use pretrained model.
    ckpt_path=None,
    audio_file=aud_p,
    force_yes=True,   # PaddleSpeech官方默认为False,设置 True 为了避免 y 确认
    device=paddle.get_device())
v2txt = format(text)
#print('ASR Result: \n{}'.format(text))

text_executor = TextExecutor()
result = text_executor(
    text=v2txt,
    task='punc',
    model='ernie_linear_p7_wudao',
    lang='zh',
    config=None,
    ckpt_path=None,
    punc_vocab=None,
    device=paddle.get_device())
txt2fmtxt = format(result)
#print('Text Result: \n{}'.format(result))

pattern = r'，|。|；| '
match = re.split(pattern,txt2fmtxt)
lst_txt = match
#print(match)
f = open('./tmphk/hk_t.txt','w',encoding='utf-8')
for im in match:
    f.write(im + '\n')
f.close


aud = AudioSegment.from_wav(aud_p)

if os.path.exists('hk_srt.srt'):
    os.remove('hk_srt.srt')

n_silen_rangs = pydub.silence.detect_nonsilent(aud, min_silence_len=m_sil_len,silence_thresh=sil_th, seek_step=50)
#print('start：\n')
#print(lst_txt)
for ln in range(len(lst_txt)-1):
    with open('hk_srt.srt','a',encoding='utf-8') as fm:
        fm.write(str(ln+1)+'\n')
        i_st = n_silen_rangs[ln][0]
        i_ed = n_silen_rangs[ln][1]
        sec_st = str(i_st / 1000).split('.')[0]
        di_st = str(i_st / 1000).split('.')[1]
        sec_ed = str(i_ed / 1000).split('.')[0]
        di_ed = str(i_st / 1000).split('.')[1]
        fm.write(str(int(i_st) // 1000 // 60 // 60).zfill(2)+':'+str(int(i_st) // 1000 // 60).zfill(2)
        +':' + sec_st.zfill(2) + ','+ di_st)
        fm.write(' --> ')
        fm.write(str(int(i_ed) // 1000 // 60 // 60).zfill(2)+':'+str(int(i_ed) // 1000 // 60).zfill(2)
        +':' + sec_ed.zfill(2) + ',' + di_ed+'\n')
        fm.write(str(lst_txt[ln]))
        fm.write('\n\n')
    fm.close
print('srt字幕文件已经保存到hk_srt.srt。AI语音识别和人声时间定位可能有偏差，因此可以以文本方式打开srt手动编辑')


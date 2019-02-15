import os
import sys
import shutil
directory = sys.argv[1]
temp = ''
finaltemp = ''
ffmpeg_path = os.path.realpath('assets/ffmpeg')

os.system('mkdir cut && mkdir temp')
os.system(f'{ffmpeg_path} -i videos/1.mp4 -ss 00:00:00 -t 00:00:04 -strict -2 -async 1 cut/0.mp4')
for filename in os.listdir(directory):
	ffmpeg = f'{ffmpeg_path} -i videos/{filename} -ss 00:00:04 -t 00:00:14 -c copy cut/{filename} -y'
	os.system(ffmpeg)
for filename in sorted(os.listdir('cut')):
	temp += f'{ffmpeg_path} -i cut/{filename} -c copy -bsf:v h264_mp4toannexb -f mpegts temp/{filename.split(".")[0]}.ts &&'
	finaltemp += f'temp/{filename.split(".")[0]}.ts|'
os.system(temp+f' {ffmpeg_path} -i "concat:{finaltemp[0:-1]}" -c copy -bsf:a aac_adtstoasc temp/appended_video.mp4 -y')
os.system(f'{ffmpeg_path} -i temp/appended_video.mp4 -q:a 0 -map a temp/tempaudio.mp3 -y')
os.system(f'{ffmpeg_path} -i assets/ncs.mp3 -i temp/tempaudio.mp3  -filter_complex amerge -c:a libmp3lame -q:a 4 temp/audiofinal.mp3 -y')
os.system(f'{ffmpeg_path} -i temp/appended_video.mp4 -an temp/noaudio.mp4')
os.system(f'{ffmpeg_path}  -i temp/noaudio.mp4 -i temp/audiofinal.mp3 -shortest -strict -2 final.mp4 -y')
shutil.rmtree('cut')
shutil.rmtree('temp')
print('Montage created!!')



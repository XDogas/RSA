python3 generate_img.py
rm -rf geckodriver.log
ffmpeg -f concat -i images/input.txt images/video.mp4

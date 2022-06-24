python3 simul.py

echo "1 - Generate video (it takes about 4 minutes)"
echo "2 - Exit program"

read -p "option: " op

case $op in
    #case 1
    1)  echo "generating video..."
        python3 generate_img.py
        rm -rf geckodriver.log
        ffmpeg -f concat -i images/input.txt images/video.mp4
        echo "video generated"
        vlc images/video.mp4 ;;

    #case 2
    2) echo "exit" ;;
esac
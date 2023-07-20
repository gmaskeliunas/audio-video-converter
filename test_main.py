import subprocess
import pytest
import os
from main import convert, convert_video


def test_convert_audio():
    input_path = 'audio\\input\\sample_audio.mp3'
    output_path = 'audio\\output\\sample_audio.wav'
    if os.path.exists(output_path):
        os.remove(output_path)
    assert convert(input_path, output_path)

def test_convert_video():
    input_path = 'videos\\input\\sample5s_video.mp4'
    output_path = 'videos\\output\\sample5s_video.mkv'
    if os.path.exists(output_path):
        os.remove(output_path)
    assert convert(input_path, output_path)

def test_wrong_format():
    input_path = 'videos\\input\\sample5s_video.mp4'
    output_path = 'videos\\output\\sample5s_video.asdasd'
    if os.path.exists(output_path):
        os.remove(output_path)

    with pytest.raises(ValueError):
        convert(input_path, output_path)

@pytest.mark.xfail(raises=subprocess.CalledProcessError)
def test_webm_conversion_raises_err():
    input_path = 'videos\\input\\sample5s_video.mp4'
    output_path = 'videos\\output\\sample5s_video.webm'
    if os.path.exists(output_path):
        os.remove(output_path)
    command = ["ffmpeg", "-y", "-i", input_path, "-c", "copy", output_path]
    convert_video(command)
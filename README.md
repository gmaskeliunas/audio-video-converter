# Audio/Video Converter Tool

This tool is designed to convert audio and video files from one format to another. It requires the following libraries to be installed:

- PySimpleGUI
- pydub
- pathlib
- os
- subprocess
- sys
- time

## Installation

1. Download and unzip the ffmpeg file `ffmpeg-git-essentials.7z` from the website "https://www.gyan.dev/ffmpeg/builds/".
2. Extract the `/bin` contents, which are `ffmpeg.exe`, `ffplay.exe`, and `ffprobe.exe`, and place them in the same folder as the `main.py` file.

## Supported file formats

- Audio files: .mp3; .wav; .ogg; .flac; .aac; .m4a; .aiff
- Video Files: .mp4; .mkv; .avi; .mov; .webm

## Usage

1. Run the `main.py` file.
2. Select what you would like to convert: either an audio or video file.
3. Select the input file by clicking on the "Browse" button.
4. After clicking "Next" button, select the output format by clicking on the dropdown menu.
5. Then click "Brows" button to select where the converted file will be saved.
6. Click on the "Convert" button to start the conversion process.

## Additinoal functionality

- User is able to configure the window color theme, by going to "Options" -> "Change theme"
- User is able to change the font size of text displayed in the window, by going to "Options" -> "Change font size"
- User is able to change the language (LT, EN) as well by going to "Options" -> "Change Language"

## Testing

There is a `test_main.py` file that tests file conversion functions.

## Input Files

There are same audio and video files in `audio/input/` and `videos/input/` folders respectively.

## Program requirements

1. The program allows to convert audio files.
2. The program allows to convert video files.
3. Program supports the most popular file formats.
4. User has the ability to freely choose where the files are saved.
5. User has the option to change the font size of the program.
6. User has the option to change the language of the program.
7. User has the option to change the color theme of the program.
8. Program has at least 2 windows; the User can seamlessly navigate back and forth.
9. Consistency has to be held in terms of selected font size, language and theme.

## Justification

I wanted to make this program, because usually when I needed a file conversion tool for various projects for school or for my hobbies, the tools online were obnoxious, because they limited file you wanted to convert duration, and the actual file conversion sat behind a paywall. More complicated solution was going into video editing software and then exporting as another file, but that usually wasn't good enough, because some popular file formats weren't supported and even if they were, sometimes you could be asked to pay for additional codec/encoder, so yet again it was frustrating. Here I try to solve this problem by coding my own convertion tool, which is able to convert popular file formats.
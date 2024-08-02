# Anime Subtitle Generator
*Generate English subtitles for Japanese videos*


## Backstory
I could not find any english subtitles for the [Space Dandy](https://en.wikipedia.org/wiki/Space_Dandy) bonus episodes so I created this program.

Original Subtitles | Generated Subtitles
--- | ---
![](/screenshots/original.png) | ![](/screenshots/generated.png)

While the results are mediocre at best, [Space Dandy](https://en.wikipedia.org/wiki/Space_Dandy) is a sci-fi show with a lot of fictional names so the resulting translated subtitles were especially terrible. However, for other genres of anime, the results should be more tolerable.

## Requirements
### Python Libraries
- [whisper](https://pypi.org/project/openai-whisper/) for audio transcription using OpenAI's Whisper
- [argostranslate](https://pypi.org/project/argostranslate/) for transcription translation using LibreTranslate
### Other requirements
- [ffmpeg](https://ffmpeg.org/) (must be added to PATH) for video to audio conversion
### Hardware
Please note that the choice of libraries makes the code run completely locally (offline) so the code will take some time to run. While I don't think any specialised hardware is required, please have patience.

## Code Explanation
The **main.py** python script will ask for a **video file name** as input (eg: `example.mp4`). The video file should be located in the same folder as the script and can be in [any video format supported by FFmpeg](https://en.wikipedia.org/wiki/FFmpeg#Supported_formats). It will generate multiple intermediate files during the subtitle generation:
- **output_audio.mp3** (audio extracted from video)
- **data.json** (word-by-word transcription of audio)
- **data2.json** (groups transcription into lines)
- **data3.json** (translated transcription)

Finally, the code will generate **output.srt** (subtitle file).

The code is well commented.

### Other Languages
While this script is written to translate from Japanese to English, lines `122` and `123` can be changed to translate to and from any of the languages supported by [LibreTranslate](https://libretranslate.com/languages).
```
122 | from_code = "ja"
123 | to_code = "en"
```
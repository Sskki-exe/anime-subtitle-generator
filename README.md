# Anime Subtitle Generator
*Generate English subtitles for Japanese videos*


## Backstory
I could not find any english subtitles for the [Space Dandy](https://en.wikipedia.org/wiki/Space_Dandy) bonus episodes so I created this program.

While this program works exactly what it is supposed to do, [Space Dandy](https://en.wikipedia.org/wiki/Space_Dandy) is a sci-fi show with a lot of fictional names so the resulting translated subtitles were *unusable*. However, I'm certain that for other genres of anime, this program would work just fine.

## Code Explanation
The code will ask for an **.mp4** file location for input. It will generate multiple intermediate files during the subtitle generation:
- **output_audio.mp3** (audio extracted from video)
- **data.json** (word-by-word transcription of audio)
- **data2.json** (groups transcription into lines)
- **data3.json** (translated audio)

Finally, the code will generate **output.srt** (subtitle file).  
The code is well commented.

While this script is written to translate from Japanese to English, lines `122` and `123` can be changed to translate to and from any of the languages supported by [LibreTranslate](https://libretranslate.com/languages).
```
122 | from_code = "ja"
123 | to_code = "en"
```
### Required Python Libraries
- [whisper](https://pypi.org/project/openai-whisper/) for audio transcription using OpenAI's Whisper
- [argostranslate](https://pypi.org/project/argostranslate/) for transcription translation using LibreTranslate
### Other requirements
- [ffmpeg](https://ffmpeg.org/) (must be added to PATH) for video to audio conversion
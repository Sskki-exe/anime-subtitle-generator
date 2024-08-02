# ========================
#   Convert video to mp3
# ========================
import subprocess
def convert_mp4_to_mp3(input_file, output_file):
    try:
        # Run ffmpeg command to convert MP4 to MP3
        subprocess.run(['ffmpeg', '-y', '-i', input_file, '-vn', '-acodec', 'libmp3lame', '-q:a', '2', output_file], check=True)
        print(f"Conversion successful: {input_file} -> {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")

input_file = input("Input video file: ")
output_file = 'output_audio.mp3'

convert_mp4_to_mp3(input_file, output_file)
print("======================")
print("video converted to mp3")


# =======================================
#   Transcribe mp3 using OpenAI Whisper
# =======================================
import whisper

model = whisper.load_model("medium")
result = model.transcribe('output_audio.mp3',word_timestamps=True)

wordlevel_info = []
for each in result['segments']:
  words = each['words']
  for word in words:
    wordlevel_info.append({'word':word['word'].strip(),'start':word['start'],'end':word['end']})
print("Transcription complete")


# ==========================================
#   Store transcription timestamps in json
# ==========================================
import json
with open('data.json', 'w') as f:
    json.dump(wordlevel_info, f,indent=4)
print("Transcription converted to json")

# Convert words to lines
with open('data.json', 'r') as f:
    wordlevel_info_modified = json.load(f)

def split_text_into_lines(data):

    #maxduration in seconds
    MaxDuration = 3.0
    #Split if nothing is spoken (gap) for these many seconds
    MaxGap = 1.5

    subtitles = []
    line = []
    line_duration = 0
    line_chars = 0


    for idx,word_data in enumerate(data):
        word = word_data["word"]
        start = word_data["start"]
        end = word_data["end"]

        line.append(word_data)
        line_duration += end - start
        
        temp = " ".join(item["word"] for item in line)
        

        # Check if adding a new word exceeds the maximum character count or duration
        new_line_chars = len(temp)

        duration_exceeded = line_duration > MaxDuration 
        if idx>0:
          gap = word_data['start'] - data[idx-1]['end'] 
          # print (word,start,end,gap)
          maxgap_exceeded = gap > MaxGap
        else:
          maxgap_exceeded = False
        

        if duration_exceeded or maxgap_exceeded:
            if line:
                subtitle_line = {
                    "word": " ".join(item["word"] for item in line),
                    "start": line[0]["start"],
                    "end": line[-1]["end"],
                    "textcontents": line
                }
                subtitles.append(subtitle_line)
                line = []
                line_duration = 0
                line_chars = 0


    if line:
        subtitle_line = {
            "word": " ".join(item["word"] for item in line),
            "start": line[0]["start"],
            "end": line[-1]["end"],
            "textcontents": line
        }
        subtitles.append(subtitle_line)

    return subtitles

linelevel_subtitles = split_text_into_lines(wordlevel_info_modified)

with open('data2.json', 'w') as f:
    json.dump(linelevel_subtitles, f,indent=4)
print("Transcription converted to lines")

# ================================================
#   Translate transcription using LibreTranslate
# ================================================
import argostranslate.package
import argostranslate.translate

from_code = "ja"
to_code = "en"

# Download and install Argos Translate package
argostranslate.package.update_package_index()
available_packages = argostranslate.package.get_available_packages()
package_to_install = next(
    filter(
        lambda x: x.from_code == from_code and x.to_code == to_code, available_packages
    )
)
argostranslate.package.install_from_path(package_to_install.download())

# Translate
# argostranslate.translate.translate("Hello World", from_code, to_code)
with open('data2.json','r') as file:
    data = json.load(file)

for line in data:
    line['word'] = argostranslate.translate.translate(line['word'], from_code, to_code)

with open('data3.json','w') as f:
    json.dump(data,f, indent=4)

print("Transcription translated")



# =======================
#   Convert to srt file
# =======================

def json_to_srt(json_file_path, srt_file_path):
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    with open(srt_file_path, 'w') as srt_file:
        for index, entry in enumerate(data, start=1):
            start_time = entry.get('start', '')
            end_time = entry.get('end', '')
            word = entry.get('word', '')

            # Format timestamps in SRT style (HH:MM:SS,mmm)
            formatted_start_time = "{:02d}:{:02d}:{:02d},{:03d}".format(
                int(start_time // 3600),
                int((start_time % 3600) // 60),
                int(start_time % 60),
                int((start_time % 1) * 1000)
            )

            formatted_end_time = "{:02d}:{:02d}:{:02d},{:03d}".format(
                int(end_time // 3600),
                int((end_time % 3600) // 60),
                int(end_time % 60),
                int((end_time % 1) * 1000)
            )

            # Write entry to SRT file
            srt_file.write(f"{index}\n{formatted_start_time} --> {formatted_end_time}\n{word}\n\n")

json_to_srt("data3.json", "output.srt")
print("Subtitle file generated")

# ======================================
#   Embed into video (not implemented)
# ======================================

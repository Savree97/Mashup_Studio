import sys
import os
import shutil
import yt_dlp
from moviepy import VideoFileClip
from pydub import AudioSegment


#argument validation
def validate_arguments(args):
    if len(args) != 5:
        print("Usage: python <program.py> <SingerName> <NumberOfVideos> <AudioDuration> <OutputFileName>")
        sys.exit()

    singer_name = args[1]

    try:
        video_count = int(args[2])
        clip_duration = int(args[3])
    except ValueError:
        print("Error: Number of videos and duration must be integers.")
        sys.exit()

    output_file = args[4]

    if video_count <= 10:
        print("Error: Number of videos must be greater than 10.")
        sys.exit()

    if clip_duration <= 20:
        print("Error: Audio duration must be greater than 20 seconds.")
        sys.exit()

    if not output_file.endswith(".mp3"):
        print("Error: Output file must have .mp3 extension.")
        sys.exit()

    return singer_name, video_count, clip_duration, output_file

#directory setup
def setup_directories():
    os.makedirs("videos", exist_ok=True)
    os.makedirs("audios", exist_ok=True)
    os.makedirs("trimmed", exist_ok=True)

#video download
def download_videos(singer, count):
    print(f"[INFO] Downloading top {count} YouTube results for '{singer}'...")

    search_query = f"ytsearch{count}:{singer} official music video"

    download_options = {
        'format': 'best',
        'outtmpl': 'videos/%(title)s.%(ext)s',
        'quiet': True
    }

    with yt_dlp.YoutubeDL(download_options) as ydl:
        ydl.download([search_query])

    print("[INFO] Video download completed.")

#audio extraction
def extract_audio():
    print("[INFO] Extracting audio from downloaded videos...")

    for file in os.listdir("videos"):
        video_path = os.path.join("videos", file)
        audio_filename = os.path.splitext(file)[0] + ".mp3"
        audio_path = os.path.join("audios", audio_filename)

        try:
            video_clip = VideoFileClip(video_path)
            video_clip.audio.write_audiofile(audio_path, logger=None)
            video_clip.close()
        except Exception as e:
            print(f"[WARNING] Failed to process {file}: {e}")

    print("[INFO] Audio extraction completed.")

#trimming audio clips
def trim_audios(duration):
    print(f"[INFO] Trimming each audio file to first {duration} seconds...")

    for file in os.listdir("audios"):
        audio_path = os.path.join("audios", file)
        trimmed_path = os.path.join("trimmed", file)

        try:
            sound = AudioSegment.from_mp3(audio_path)
            trimmed_sound = sound[:duration * 1000]
            trimmed_sound.export(trimmed_path, format="mp3")
        except Exception as e:
            print(f"[WARNING] Failed to trim {file}: {e}")

    print("[INFO] Audio trimming completed.")

#merging the sudio files
def merge_audios(output_file):
    print("[INFO] Merging trimmed audio files...")

    final_mix = AudioSegment.empty()

    for file in os.listdir("trimmed"):
        clip_path = os.path.join("trimmed", file)
        sound = AudioSegment.from_mp3(clip_path)
        final_mix += sound

    final_mix.export(output_file, format="mp3")

    print(f"[SUCCESS] Mashup created successfully: {output_file}")


def cleanup():
    print("[INFO] Cleaning temporary files...")
    shutil.rmtree("videos", ignore_errors=True)
    shutil.rmtree("audios", ignore_errors=True)
    shutil.rmtree("trimmed", ignore_errors=True)


def main():
    try:
        singer, number, duration, output = validate_arguments(sys.argv)

        setup_directories()
        download_videos(singer, number)
        extract_audio()
        trim_audios(duration)
        merge_audios(output)
        cleanup()

    except Exception as error:
        print(f"[ERROR] Unexpected issue occurred: {error}")
        cleanup()


if __name__ == "__main__":
    main()
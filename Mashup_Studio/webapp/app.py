from flask import Flask, render_template, request
import os
import zipfile
import shutil
from flask_mail import Mail, Message
import yt_dlp
from moviepy.editor import VideoFileClip
from pydub import AudioSegment

app = Flask(__name__)

# ---------------- EMAIL CONFIG ----------------

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'sdohar_be23@thapar.edu'
app.config['MAIL_PASSWORD'] = 'cadhuvujnldahitm'

mail = Mail(app)

# ---------------- MASHUP FUNCTION ----------------

def generate_mashup(singer, number, duration, output_file):

    os.makedirs("videos", exist_ok=True)
    os.makedirs("audios", exist_ok=True)
    os.makedirs("trimmed", exist_ok=True)

    query = f"ytsearch{number}:{singer} official music"

    ydl_opts = {
        'format': 'best',
        'outtmpl': 'videos/%(title)s.%(ext)s',
        'quiet': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([query])

    for file in os.listdir("videos"):
        video_path = os.path.join("videos", file)
        audio_name = os.path.splitext(file)[0] + ".mp3"
        audio_path = os.path.join("audios", audio_name)

        clip = VideoFileClip(video_path)
        clip.audio.write_audiofile(audio_path, logger=None)
        clip.close()

    for file in os.listdir("audios"):
        audio_path = os.path.join("audios", file)
        trimmed_path = os.path.join("trimmed", file)

        sound = AudioSegment.from_mp3(audio_path)
        trimmed = sound[:duration * 1000]
        trimmed.export(trimmed_path, format="mp3")

    final = AudioSegment.empty()

    for file in os.listdir("trimmed"):
        final += AudioSegment.from_mp3(os.path.join("trimmed", file))

    final.export(output_file, format="mp3")

    shutil.rmtree("videos")
    shutil.rmtree("audios")
    shutil.rmtree("trimmed")

# ---------------- ROUTE ----------------

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        singer = request.form["singer"]
        number = int(request.form["number"])
        duration = int(request.form["duration"])
        email = request.form["email"]

        output_file = "mashup.mp3"

        generate_mashup(singer, number, duration, output_file)

        zip_name = "mashup.zip"
        with zipfile.ZipFile(zip_name, 'w') as zipf:
            zipf.write(output_file)

        msg = Message("Your Mashup is Ready",
                      sender=app.config['MAIL_USERNAME'],
                      recipients=[email])

        with app.open_resource(zip_name) as fp:
            msg.attach("mashup.zip", "application/zip", fp.read())

        mail.send(msg)

        return "Mashup generated and sent successfully!"

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

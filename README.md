# 🎵 Mashup Studio

Create your own vibrant YouTube music mashups using Python and Flask.

Mashup Studio is a full-stack Python project that automatically downloads multiple YouTube videos of a selected artist, extracts audio clips, trims them, merges them into a single mashup file, and optionally delivers it via a web interface.

---

## 🖼️ UI Preview

![Mashup Studio UI](assets/ui-preview.png)

---

## 🚀 Project Overview

This project consists of two main components:

### 1️⃣ Command Line Mashup Generator  
A Python script that:
- Downloads N YouTube videos of a given singer
- Extracts audio from each video
- Trims the first Y seconds
- Merges all trimmed clips
- Generates a final MP3 mashup file

### 2️⃣ Web-Based Mashup Generator (Flask App)  
A web interface where users can:
- Enter Singer / Band name  
- Select number of videos  
- Choose clip duration  
- Provide email ID  
- Generate and receive a mashup file  

---

## ⚙️ Technologies Used

- Python  
- Flask  
- yt-dlp  
- MoviePy  
- pydub  
- FFmpeg  
- SMTP (Email delivery)

---

## 📂 Project Structure

```
Mashup_Studio/
│
├── 102317097.py              # Command-line mashup generator
├── README.md
│
├── assets/
│   └── ui-preview.png        # UI screenshot
│
└── webapp/
    ├── app.py                # Flask web application
    └── templates/
        └── index.html        # Frontend UI
```

---

## 🖥️ How to Run (Command Line Version)

Open terminal inside the project folder and run:

```
python 102317097.py "<SingerName>" <NumberOfVideos> <AudioDuration> <OutputFileName>
```

### Example:

```
python 102317097.py "Harry Styles" 12 25 mashup.mp3
```

### Conditions:
- NumberOfVideos must be greater than 10  
- AudioDuration must be greater than 20 seconds  
- Proper argument validation implemented  
- Exception handling included  

Output:  
A merged MP3 mashup file is generated in the same directory.

---

## 🌐 How to Run (Web App Version)

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the Flask server:
   ```
   python app.py
   ```

3. Open browser and visit:
   ```
   http://127.0.0.1:5000
   ```

4. Fill the form and generate your mashup.

---

## 📦 Requirements

- Python 3.10+
- pip installed
- FFmpeg installed and added to system PATH

Note:  
FFmpeg is not installed via pip. It must be downloaded separately from:  
https://ffmpeg.org/download.html

---

## ✨ Features

- Automated YouTube video downloading
- Audio extraction and trimming
- Multi-clip audio merging
- Web-based user interface
- Email delivery of mashup
- Clean, minimal, user-friendly UI

---

## 🎯 Learning Outcomes

This project demonstrates:
- Python scripting
- File handling & automation
- Audio processing
- Backend development using Flask
- Basic frontend integration
- API-based data extraction

---

## 📌 Author

Savree Dohar  

Developed as part of the UCS654 Mashup Assignment.

---


from flask import Flask, render_template, request,redirect, flash, jsonify, url_for
# import speech_recognition as sr
import yt_dlp as youtube_dl
import os
from moviepy.editor import *
import requests
app = Flask(__name__)
app.secret_key = "speach"

@app.route("/through_link", methods=["GET", "POST"])
def through_link():
    if request.method == "POST":
        if request.form.get("type") == "0":
            return render_template('index.html', error="Please Selected the Link Type")
        elif request.form.get("type") == "1":
            data = download_ytvid_as_mp3(request.form.get("url_link"))
            if data.get("success") == True:
                transcript = data.get("transcript")
                return render_template('index.html', transcript=transcript)
            else:
                error = data.get("error")
                return render_template('index.html', error=error)
        elif request.form.get("type") == "2":
            data  = download_file_from_google_drive(request.form.get("url_link"))
            if data.get("success") == True:
                transcript = data.get("transcript")
                return render_template('index.html', transcript=transcript)
            else:
                error = data.get("error")
                return render_template('index.html', error=error)

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value
    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768
    print("Downloading Video File: ")
    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
    print("Video File Saved:")
    return True

def convert_mp4_to_mp3(destination):
    print("Converting MP4 to MP3: ")

    destination_mp3 =  os.getcwd()+"/audiofiles/convert.mp3"
    # destination_mp3 = r"/home/dhanesh/Desktop/project/Updated File-20230509T071324Z-001/Updated File/Speech-Recognition-20230327T203634Z-001/Speech-Recognition/audiofiles/convert.mp3"
    # Load the mp4 file
    video = VideoFileClip(destination)
    # Extract audio from video
    video.audio.write_audiofile(destination_mp3)
    print("Audio File Saved: ")

    return destination_mp3

def speech_recognition(path):
    print("Audio converting into Text")
    import whisper
    model = whisper.load_model("base")
    # path = "/home/dhanesh/Desktop/project/Updated File-20230509T071324Z-001/Updated File/Speech-Recognition-20230327T203634Z-001/Speech-Recognition/audiofiles/"
    # print("transcribe ====  :", file.filename)
    # import pdb;pdb.set_trace()
    text = model.transcribe(path, fp16=False)
    transcript = text['text']
    print(transcript)
    return transcript
def download_file_from_google_drive(url_link):
    result = {"success": True}
    try:
        URL = "https://docs.google.com/uc?export=download"
        # id = "https://drive.google.com/file/d/1TvsaN210HrV963yaMVDK6RIpUBq2gWyt/view"
        # url = https://drive.google.com/file/d/1HT8DDtv4juT_mWl-MAdWww3UKqU7LAWa/view?usp=sharing
        # id = "1TvsaN210HrV963yaMVDK6RIpUBq2gWyt"
        # id = "1HT8DDtv4juT_mWl-MAdWww3UKqU7LAWa"
        split_url = url_link.split("/d/")[1]
        id = split_url.split("/view")[0]
        print("ID Splited: ",id)
        destination = os.getcwd()+"/audiofiles/video.mp4"
        # destination = r"/home/dhanesh/Desktop/project/Updated File-20230509T071324Z-001/Updated File/Speech-Recognition-20230327T203634Z-001/Speech-Recognition/audiofiles/video.mp4"
        session = requests.Session()
        response = session.get(URL, params = { 'id' : id }, stream = True)
        token = get_confirm_token(response)

        # if token:
        params = { 'id' : id}
        rsp = session.get(URL, params = params, stream = True)

        saved = save_response_content(rsp, destination)

        if saved:
            path = convert_mp4_to_mp3(destination)
            txt = speech_recognition(path)
            # remove audio and video file

            os.remove(path)
            os.remove(destination)
            print("File Removed: ")
            # print("convert_mp4_to_mp3 Text: ",convert_mp4_to_mp3)
            result["transcript"] = txt
            return result
    except Exception as e:
        result["success"] = False

        result["error"] = str(e)
        return result
def download_ytvid_as_mp3(video_url):
    destination_mp3 = os.getcwd()+"/audiofiles/youtube_audio.mp3"
    result = {"success": True}
    try:
        # video_url = "https://youtu.be/ry9SYnV3svc"
        video_info = youtube_dl.YoutubeDL().extract_info(url = video_url,download=False)
        filename = f"{video_info['title']}.mp3"
        print("File name===",filename)
        options={
            'format':'bestaudio/best',
            'keepvideo':False,
            'outtmpl':destination_mp3,
        }
        with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download([video_info['webpage_url']])
        print("Download complete... {}".format(filename))
        # convert audio into text
        txt = speech_recognition(destination_mp3)
        # remove audio and video file
        os.remove(destination_mp3)
        result["transcript"] = txt
        return result
    except Exception as e:
        result["success"] = False
        result["error"] = str(e)
        return result

@app.route("/", methods=["GET", "POST"])
def index():
    transcript = ""
    if request.method == "POST":
        # print("cehck ====", request.form)
        # if request.form.get("type"):
        #     transcript = through_link(request.form.get("type",'0'),request.form.get("url_link",''))
        #     # import pdb;pdb.set_trace()
        # else:
        print("FORM DATA RECEIVED")
        if "file" not in request.files:
            return redirect(request.url)

        file = request.files["file"]

        if file.filename == "":
            return redirect(request.url)

        if file:
            print("File ====> ",file)
            # file.save(file.filename)
            print(type(file))
            import whisper
            model = whisper.load_model("base")
            path = "/home/dhanesh/Desktop/project/Updated File-20230509T071324Z-001/Updated File/Speech-Recognition-Python-Final-20230327T203634Z-001/Speech-Recognition-Python-Final/audiofiles/"
            print("transcribe ====  :",file.filename)
            # import pdb;pdb.set_trace()
            text = model.transcribe(path+file.filename, fp16=False)
            transcript= text['text']
            print(transcript)
            # res = text['text']

    return render_template('index.html', transcript=transcript)


if __name__ == "__main__":
    app.run(debug=True, threaded=True)

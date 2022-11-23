from flask import Flask, render_template, url_for, request, redirect, send_file
from urllib.request import urlretrieve
from pytube import YouTube, exceptions
from os import path, rename

app = Flask(__name__)


def download_audio(video_link="", SAVE_PATH="C:/Users/ariyu/Desktop/vscode/python/youtube/"):
    yt = YouTube(video_link)   

    stream = yt.streams.filter(only_audio=True).first()

    app.logger.info(f"Downloading: {yt.title}")
    out_file = stream.download(SAVE_PATH)
    
    base, ext = path.splitext(out_file)
    new_file = base + '.mp3'
    rename(out_file, new_file)

def download_video(video_link="", SAVE_PATH="C:/Users/ariyu/Desktop/vscode/python/youtube/", resolution="720p"):
    yt = YouTube(video_link)

    stream = yt.streams.filter(res=resolution).first()
    app.logger.info(f"Downloading: {yt.title}")
    stream.download(SAVE_PATH)

def download_thumbnail(video_link="", SAVE_PATH="C:/Users/ariyu/Desktop/vscode/python/youtube/"):
    imgURL = YouTube(video_link).thumbnail_url
    app.logger.info(f"Downloading: {YouTube(video_link).title}")
    urlretrieve(imgURL, f"thumbnail {YouTube(video_link).title}.jpg")


@app.route('/')
def index():
    return redirect('/download', code=302)

@app.route('/download', methods=["GET", "POST"])
def download():
    if request.method == "POST":
        link = request.form["downloadlink"]
        dtype = request.form["dtype"]

        if(dtype == "mp3"):
            download_audio(link)
            path = f"{YouTube(link).title}.mp3".replace("'", "")
            return send_file(path, as_attachment=True)

        elif(dtype == "mp4"):
            download_video(link)
            path = f"{YouTube(link).title}.mp4".replace("'", "")
            return send_file(path, as_attachment=True)

        elif(dtype == "thumb"):
            download_thumbnail(link)
            path = f"thumbnail {YouTube(link).title}.jpg".replace("'", "")
            return send_file(path, as_attachment=True)
    else:
        return render_template('download.html')

if __name__ == "__main__":
    app.run(debug=True)

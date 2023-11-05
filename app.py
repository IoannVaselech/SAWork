from flask import Flask, render_template, request, send_file, send_from_directory
import csv
from googleapiclient.errors import HttpError
from get_comments import get_comments
from get_live_chat_comments import get_live_chat_comments
from utils import snippet_to_dict, get_video_id
from googleapiclient.discovery import build
import os

app = Flask(__name__)

# Инициализация YouTube API
API_KEY = "AIzaSyBhjWK7hVTpeVAQN0E-aFX_uCG-qpTXX-8"
service = build('youtube', 'v3', developerKey=API_KEY)


# Обработчики маршрутов

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        video_url = request.form['video_url']
        
        video_id = get_video_id(video_url)

        if video_id:
            if "youtu.be" in video_url or "youtube.com/watch" in video_url:
                
                comments = get_comments(video_id, service)
                
            else:
                return render_template('index.html')  # Ошибка - неверный формат ссылки
            
            csv_dir = os.path.join(os.getcwd(), 'csv_files')
            if not os.path.exists(csv_dir):
                os.makedirs(csv_dir)

            file_name = os.path.join(csv_dir, f"comments_{video_id}.csv")

            with open(file_name, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerow(['Author', 'Comment'])
                for comment in comments:
                    comment_lines = comment['text'].split('\n')
                    for line in comment_lines:
                        writer.writerow([comment['author'], line.strip()])

            return render_template('index.html', file_name=file_name)
        else:
            return render_template('index.html')  # Ошибка - неверный формат ссылки

    return render_template('index.html')


@app.route('/download', methods=['GET'])
def download_comments():
    file_name = request.args.get('file_name')
    try:
        return send_file(file_name, as_attachment=True)
    except FileNotFoundError:
        return "File not found"

@app.route('/list_files', methods=['GET'])
def list_files():
    csv_dir = os.path.join(os.getcwd(), 'csv_files')
    file_list = os.listdir(csv_dir)
    return render_template('list_files.html', file_list=file_list)

if __name__ == '__main__':
    app.run(debug=True)

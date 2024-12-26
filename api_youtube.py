import requests
import re
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
def extract_video_id(url):
    # Regular expression to extract video ID from YouTube URL
    pattern = r'(\w{11}).*'
    match = re.search(pattern, url)
    return match.group(1) if match else None
# https://www.youtube.com/watch?v=Eqf3TaihsOI
@app.route('/get_video_data', methods=['POST'])
def get_video_data():
    url = request.form.get('url')
    vidid = extract_video_id(url)
    if not vidid:
        return "Invalid YouTube URL"
    else:
        def get_data():
            response = requests.get(f"https://returnyoutubedislikeapi.com/votes?videoId={vidid}")
            if response.status_code == 200:
                return response.json()
            else:
                return 'Error'

        data = get_data()
        if data != 'Error':
            likes = data['likes']
            dislikes = data['dislikes']
            dislike_percentage = (dislikes / (likes + dislikes)) * 100
            return f'Likes: {likes}, Dislikes: {dislikes}, Dislike percentage: {dislike_percentage}%'
        else:
            return data

# if not vidid:
#     print("Invalid YouTube URL")
# else:
#     def get_data():
#         response = requests.get(f"https://returnyoutubedislikeapi.com/votes?videoId={vidid}")
#         if response.status_code == 200:
#             return response.json()
#         else:
#             return 'Error'

#     data = get_data()
#     if data != 'Error':
#         print('Likes is ' + str(data['likes']))
#         print('Dislikes is ' + str(data['dislikes']))
#         print(f"Dislike percentage is {(data['dislikes']/(data['likes']+data['dislikes']))*100}%")
#     else:
#         print(data)
if __name__ == '__main__':
    app.run()
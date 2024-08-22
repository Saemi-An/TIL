from flask import Flask, render_template, jsonify
from database import *
from api import *

app = Flask(__name__)

@app.route('/')
def main():

    return render_template("main.html")

@app.route('/plyy/<id>')
def plyy(id=int):

    return render_template("plyy-detail.html")

@app.route('/curator/<id>')
def curator(id):

    return render_template("curator-detail.html")

@app.route('/song_detail/<p_id>+<num>')
def song(p_id, num):

    return render_template('song-detail2.html')

# API - MAIN - 태그 검색
@app.route('/api_main/search_by_tags')
def api_main_search_by_tags():
    search_by_tags = main_search_tags()

    return jsonify(search_by_tags)

# API - MAIN - 플리 카드
@app.route('/api_main/plyy_cards')
def api_main_plyy_cards():
    plyy_cards = main_plyy_cards()

    return jsonify(plyy_cards)

# API - MAIN - 큐레이터 카드
@app.route('/api_main/curator_cards')
def api_main_curator_cards():
    curator_cards = main_curator_cards()

    return jsonify(curator_cards)


# API 플리 상세
@app.route('/api_plyy_detail/<id>')
def api_plyy_detail(id):
    plyy = plyy_detail(id)
    
    return jsonify(plyy)

# API 플리 상세 - 플리 좋아요 갯수
@app.route('/api_plyy_detail_likes/<id>')
def api_plyy_detail_likes(id):
    plyy = fetch_plyy_detail_likes(id)
    
    return jsonify(plyy)

# API 큐레이터 상세 - 큐레이터 정보
@app.route('/api_curator_detail/<c_id>')
def api_curator_detail(c_id):
    curator_details = curator_detail(int(c_id))
    
    return jsonify(curator_details)

# API 큐레이터 상세 - 개별 큐레이터의 플레이리스트 배열
@app.route('/api_curator_detail_plyy_cards/<c_id>')
def api_curator_detail_plyy_cards(c_id):
    c_detail_curator_cards = curator_detail_plyy_cards(int(c_id))
    
    return jsonify(c_detail_curator_cards)

# API 곡 상세 - 플리 id, 곡 num 필요
@app.route('/api_song_detail/<p_id>')
def api_song_detail(p_id):
    song_detail_list = song_detail(p_id)
    

    # SONG - num / vid / cmt / p_id
    # TRACK - img / title / artist / album
    # 총 곡수는 따로 구하기

    return jsonify(song_detail_list)


# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5050)

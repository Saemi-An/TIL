from flask import Flask, render_template, jsonify
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
    # 플리 카드 목록 : 
    return render_template("curator-detail.html")

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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050)

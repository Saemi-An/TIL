from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

mydatabase = {
    'user1': {
        'name': '김몰랑몰랑',
        'age': 23,
        'address': '강원도',
        'car': '없음'
    },
    'user2': {
        'name': '안새미',
        'age': 28,
        'address': '서울',
        'car': 'G70'
    },
    'user3': {
        'name': '권아무개',
        'age': 35,
        'address': '경기도',
        'car': 'K-7'
    }
}

@app.route('/')
def index():
    return render_template("POST_req.html")

@app.route('/post_endpoint', methods=['POST'])
def handle_post():
    # 요청에서 JSON 데이터를 가져오기
    data = request.get_json()
    
    # JSON 데이터가 제대로 전달되었는지 확인
    if not data:
        return jsonify({"error": "No JSON data received"}), 400
    
    # JSON 데이터 처리
    # eg) POST로 넘어온 데이터들 중 필요한 데이터 추출하기
    name = data.get('name', 'Unknown')
    print(f"포스트로 넘어온 이름: {name}")
    age = data.get('age', 'Not provided')
    address = data.get('address', 'Unknown')
    car = data.get('car', 'Unknown')
    
    # 사용자 검색: mydatabase에 존재하는 사용자일 경우 return
    for k, v in mydatabase.items():
        if name == mydatabase[k]['name']:
            print('데이터베이스에 있는 사용자 입니다.')
            # 데이터를 응답으로 반환
            response = {
                "message": "사용자 식별이 완료 되었습니다.",
                "personal_data": {
                    "이름": name,
                    "나이": age,
                    "주소": address,
                    "자동차": car
                }
            }
            return jsonify(response), 200
    
    # 사용자 검색: mydatabase에 존재 X 경우 return
    response = {
        "message": "사용자를 찾을 수 없습니다."
    }
    return jsonify(response), 200
    

if __name__ == '__main__':
    app.run(debug=True, port=5051)
import sqlite3
from pprint import pprint

def connect_db():
    conn = sqlite3.connect('plyy_v4.db')
    conn.execute('PRAGMA foreign_keys = ON')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    return conn, cur


def fetch_plyy_card_data():
    conn, cur = connect_db()
    cur.execute('''
        SELECT
            PLYY.id as plyy_id,
            PLYY.title as plyy_title,
            PLYY.img as plyy_img,
            PLYY.gen_date as plyy_gen_date,
            GENRE.name as g_name,
            CURATOR.name as c_name,
            COUNT(SONG.p_id) as total_songs,
            SUM(TRACK.rtime) as total_rtime
        FROM PLYY
                
        JOIN GENRE ON PLYY.g_id = GENRE.id
        JOIN CURATOR ON PLYY.c_id = CURATOR.id
        JOIN SONG ON PLYY.id = SONG.p_id
        JOIN TRACK ON SONG.tk_id = TRACK.id
        
        GROUP BY PLYY.title
    ''')
    raw_data = cur.fetchall()
    plyy_card = []
    for row in raw_data:
        plyy_card.append(dict(row))
    conn.close()

    for card in plyy_card:
        card['total_rtime'] = cal_rtime(card['total_rtime'])

    return plyy_card
# [ {'c_name': '쌔미',
#   'g_name': '팝',
#   'plyy_gen_date': '2024-08-03 06:25:02',
#   'plyy_id': 9,
#   'plyy_img': 'P9.jpg',
#   'plyy_title': '🧇 my_collection.zip 🥐',
#   'total_rtime': 3045711,
#   'total_songs': 16}]


def fetch_plyy_card_tags():
    conn, cur = connect_db()
    cur.execute('''
        SELECT PLYY.id as plyy_id, TAG.name as t_name from PLYY
            JOIN P_TAG ON PLYY.id = P_TAG.p_id
            JOIN TAG ON P_TAG.t_id = TAG.id
    ''')
    raw_data = cur.fetchall()
    plyy_tags = []
    for row in raw_data:
        plyy_tags.append(dict(row))
    conn.close()

    return plyy_tags
#  [{'plyy_id': 8, 't_name': '그루비'},
#  {'plyy_id': 9, 't_name': '내가_좋아하는_노래'},
#  {'plyy_id': 9, 't_name': '너도_마음에_들었으면'}]

def fetch_all_tags():
    conn = sqlite3.connect('plyy_v4.db')
    conn.execute('PRAGMA foreign_keys = ON')
    cur = conn.cursor()
    cur.execute('SELECT name FROM TAG')
    tag_data = cur.fetchall()
    cur.execute('SELECT name FROM GENRE')
    genre_data = cur.fetchall()

    tag_list = []
    for tag in tag_data:
        txt = "".join(tag)
        tag_dict = {}
        tag_dict['tag'] = txt
        tag_list.append(tag_dict)

    for genre in genre_data:
        txt = "".join(genre)
        tag_dict = {}
        tag_dict['tag'] = txt
        tag_list.append(tag_dict)

    return tag_list

# 밀리초 변환 함수
def cal_rtime(ms):
    minute_time = round(ms / 60000)
    if minute_time >= 60:
        hour_time = minute_time // 60
        minute_time = '{0:02d}'.format(minute_time % 60)
        return f"{hour_time}시간 {minute_time}분"
    else:
        minute_time = minute_time
        return f"{minute_time}분"
    
def fetch_curator_cards():
    conn, cur = connect_db()
    cur.execute('''
        SELECT 
            CURATOR.id,
            CURATOR.name,
            CURATOR.img,
            CURATOR.intro
        FROM CURATOR
    ''')
    raw_data = cur.fetchall()
    curator_card = []
    for row in raw_data:
        curator_card.append(dict(row))
    conn.close()

    return curator_card

def fetch_curator_tags():
    conn, cur = connect_db()
    cur.execute('''
        SELECT CURATOR.id as c_id, TAG.name as tag FROM CURATOR
        JOIN C_TAG ON CURATOR.id = C_TAG.c_id
        JOIN TAG ON C_TAG.t_id = TAG.id
    ''')
    raw_data = cur.fetchall()
    curator_tags = []
    for row in raw_data:
        curator_tags.append(dict(row))
    conn.close()

    return curator_tags

def fetch_curator_up_date():
    conn, cur = connect_db()
    cur.execute('''
        SELECT 
            CURATOR.id,
            PLYY.gen_date
        FROM CURATOR
        JOIN PLYY ON CURATOR.id = PLYY.c_id
    ''')
    raw_data = cur.fetchall()
    curator_up_date = []
    for row in raw_data:
        curator_up_date.append(dict(row))
    conn.close()

    return curator_up_date

# 플리상세 기본정보 fetch
def fetch_plyy_detail_1(id=int):
    conn, cur = connect_db()
    cur.execute('''
        SELECT 
            PLYY.id,
            PLYY.title,
            PLYY.gen_date,
            PLYY.cmt,
            CURATOR.name as c_name,
            COUNT(SONG.p_id) as total_songs,
            SUM(TRACK.rtime) as total_rtime
        FROM PLYY
        JOIN CURATOR ON PLYY.c_id = CURATOR.id
        JOIN SONG ON PLYY.id = SONG.p_id
        JOIN TRACK ON SONG.tk_id = TRACK.id
        WHERE PLYY.id = ?
        GROUP BY PLYY.id
    ''', (id, ))
    raw_data = cur.fetchall()
    result = []
    for row in raw_data:
        result.append(dict(row))
    conn.close()

    return result

# 플리상세 태그 fetch : g_tag + t_tag
def fetch_plyy_detail_2(id=int):
    conn, cur = connect_db()
    cur.execute('''
        SELECT 
            PLYY.id,
            GENRE.name as g_tag,
            TAG.name as tag_list 
        FROM PLYY
        JOIN GENRE ON PLYY.g_id = GENRE.id
        JOIN P_TAG ON PLYY.id = P_TAG.p_id
        JOIN TAG ON P_TAG.t_id = TAG.id
        WHERE PLYY.id = ?
    ''', (id, ))
    raw_data = cur.fetchall()
    result = []
    for row in raw_data:
        result.append(dict(row))
    conn.close()

    return result

# 플리상세 태그 fetch : songs
def fetch_plyy_detail_3(id=int):
    conn, cur = connect_db()
    cur.execute('''
        SELECT 
            PLYY.id,
            TRACK.img,
            TRACK.title,
            TRACK.artist,
            TRACK.rtime
        FROM PLYY
        JOIN SONG ON PLYY.id = SONG.p_id
        JOIN TRACK ON SONG.tk_id = TRACK.id
        WHERE PLYY.id = ?
    ''', (id, ))
    raw_data = cur.fetchall()
    result = []
    for row in raw_data:
        result.append(dict(row))
    conn.close()

    return result

if __name__ == '__main__':
    # pass

    data = fetch_plyy_detail_2(11)
    pprint(data)


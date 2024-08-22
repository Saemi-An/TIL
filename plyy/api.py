from database import *
from pprint import pprint
import random
import datetime

def main_plyy_cards():
    # step1
    raw_data = fetch_plyy_card_tags()

    # step2 : 각각의 카드에 'plyy_id'라는 키를 주고 값으로 카드를 받기
    dummy_list = []
    for row in raw_data:
        dummy_list.append(row['plyy_id'])

    uni_id = []
    for dumm in dummy_list:
        if dumm not in uni_id:
            uni_id.append(dumm)

    # step 3 : 태그리스트 합치기
    dummy_list2 = []
    for num in uni_id:
        new = {}
        dummy_list = []
        new['plyy_id'] = num
        for i in raw_data:
            if num == i['plyy_id']:
                dummy_list.append(i['t_name'])
            new['tag_list'] = dummy_list
        dummy_list2.append(new)

    # step 4
    dummy_card = fetch_plyy_card_data()
    plyy_card = []
    for c in dummy_card:
        for dummy in dummy_list2:
            if c['plyy_id'] == dummy['plyy_id']:
                c['tag_list'] = dummy['tag_list']
        plyy_card.append(c)
    
    plyy_card_list = []
    for card in plyy_card:
        plyy_card = {}
        plyy_card['plyy_card'] = card
        plyy_card_list.append(plyy_card)

    return plyy_card_list

def main_curator_cards():
    # card 기본 데이터 : img / name / intro
    curator_data = fetch_curator_cards()

    curator_cards = []
    for row in curator_data:
        demo = {}
        demo['curator_card'] = row
        curator_cards.append(demo)

    # card 기본 데이터 : latest_up_date, curator_card_label
    curator_up_date = fetch_curator_up_date()

    id_list = []
    for row in curator_up_date:
        if row['id'] not in id_list:
            id_list.append(row['id'])

    curator_up_date_list = []
    for id in id_list:
        result = {}
        dummy_list = []
        for row in curator_up_date:
            if row['id'] == id:
                dummy_list.append(row['gen_date'])
                most_dumm = max(dummy_list)
        result['id'] = id
        result['latest_up_date'] = most_dumm
        curator_up_date_list.append(result)

    current_time = datetime.datetime.now()
    a_week_ago = current_time - datetime.timedelta(weeks=1)
    one_week_ago = a_week_ago.strftime("%Y-%m-%d %H:%M:%S")   

    for up_date in curator_up_date_list:
        if up_date['latest_up_date'] > one_week_ago:
            up_date['curator_card_label'] = 'UPDATED'
        elif up_date['latest_up_date'] <= one_week_ago:
            up_date['curator_card_label'] = None

    # card 기본 데이터 : tags 리스트
    raw_curator_tags = fetch_curator_tags()

    curator_tags = []
    for id in id_list:
        demo_dict = {}
        demo_list = []
        for row in raw_curator_tags:
            if row['c_id'] == id:
                demo_list.append(row['tag'])
        demo_dict['id'] = id
        demo_dict['tags'] = demo_list
        curator_tags.append(demo_dict)

    # card API 생성 : 라벨 담기
    for row in curator_cards:
        for kow in curator_up_date_list:
            if row['curator_card']['id'] == kow['id']:
                row['curator_card']['c_label'] = kow['curator_card_label']
    
    # card API 생성 : 태그 담기
    for row in curator_cards:
        for cow in curator_tags:
            if row['curator_card']['id'] == cow['id']:
                row['curator_card']['c_tags'] = cow['tags']

    return curator_cards

def main_search_tags():
    all_tags = fetch_all_tags()
    
    # 전체 태그가 20개보다 적으면 오류 발생할 수 있음
    random_tags = random.sample(all_tags, 20)

    return random_tags

def plyy_detail(id=int):
    
    # {'id': 11, 'tag_list': ['인디세스푼', '아이돌한스푼', '케이팝']}
    raw_tags = fetch_plyy_detail_2(id)
    demo_list = []
    for row in raw_tags:
        demo_list.append(row['tag_list'])
    raw_tags[0]['tag_list'] = demo_list
    tags = raw_tags[0]
    tags['tag_list'].append(tags['g_tag'])
    del tags['g_tag']

    raw_plyy_detail_0 = fetch_plyy_detail_1(id)
    # gen_data 날짜만 넣기
    raw_plyy_detail = []
    for row in raw_plyy_detail_0:
        row['gen_date'] = row['gen_date'].split(' ')[0]
        raw_plyy_detail.append(row)

    raw_plyy_detail[0]['tag_list'] = tags['tag_list']

    raw_songs = fetch_plyy_detail_3(id)
    raw_plyy_detail[0]['song_list'] = raw_songs

    plyy_detail = {}
    for row in raw_plyy_detail:
        plyy_detail['plyy'] = row

    return plyy_detail

# 큐레이터상세 - 큐레이터 정보
def curator_detail(c_id=int):
    curator_detail = fetch_curator_detail(c_id)

    curator_info = {}
    for detail in curator_detail:
        curator_info['curator'] = detail

    return curator_info

# 큐레이터상세 - 큐레이터 플레이리스트 리스트
def curator_detail_plyy_cards(c_id=int):
    # 해당 큐레이터의 플리 리스트 가져오기
    curator_cards = fetch_plyy_card_data()

    raw_curator_card_list = []
    for card in curator_cards:
        if card['c_id'] == c_id:
            raw_curator_card_list.append(card)

    # 해당 큐레이터의 플리 리스트에 해당하는 태그 목록 가져오기
    curator_card_tags = fetch_plyy_card_tags()

    dummy_list = []
    for row in curator_card_tags:
        if row['c_id'] == c_id:
            dummy_list.append(row)
    
    # 해당 큐레이터의 플리 카드 + 태그 목록
    dummy_list_2 = []
    for card in raw_curator_card_list:
        card['tag_list'] = []
        for tag in dummy_list:
            if card['plyy_id'] == tag['plyy_id']:
                card['tag_list'].append(tag['t_name'])
        dummy_list_2.append(card)
    
    # API 형태로 만들기
    result_list = []
    for row in dummy_list_2:
        dummy_dict = {}
        dummy_dict['c_plyy_card'] = row
        result_list.append(dummy_dict)

    return result_list

# 곡상세 - 전체 곡 목록
def song_detail(p_id):
    song_detail_list = fetch_song_detail(p_id)

    song_detail = []
    for row in song_detail_list:
        song_detail_dict = {}
        song_detail_dict['song'] = row
        song_detail.append(song_detail_dict)
    
    return song_detail

if __name__ == '__main__':
    pass

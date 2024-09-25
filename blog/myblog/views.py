from django.shortcuts import render
from django.http import HttpResponseNotFound

from datetime import datetime
from pprint import pprint

database = [
    {"post" : {
            "post_num" : 1,
            "title" : "[공지]가을 과일 시즌 교체",
            "content" : "무화과의 계절이 돌아왔습니다! 무화과 생크림 케이크 & 무화과 휘낭시에가 신메뉴로 추가 되었습니다.",
            "registered_at" : "2024-09-21 13:10:00",
            "image" : "post1.jpg",
            "fixed" : False,
        }
    },
    {"post" : {
            "post_num" : 2,
            "title" : "[필독]홀케이크 예약시 유의사항",
            "content" : "무화과의 계절이 돌아왔습니다! 무화과 생크림 케이크 & 무화과 휘낭시에가 신메뉴로 추가 되었습니다.",
            "registered_at" : "2024-09-22 14:20:00",
            "image" : "post2.jpg",
            "fixed" : True,
        }
    },
    {"post" : {
            "post_num" : 3,
            "title" : "[필독]구움과자 예약시 유의사항",
            "content" : "무화과의 계절이 돌아왔습니다! 무화과 생크림 케이크 & 무화과 휘낭시에가 신메뉴로 추가 되었습니다.",
            "registered_at" : "2024-09-23 15:30:00",
            "image" : "post3.jpg",
            "fixed" : True,
        }
    },
    {"post" : {
            "post_num" : 4,
            "title" : "[긴급 공지]10/3(수) 휴무",
            "content" : "다음 주 10/3(수요일) 개인사정으로 휴무일 입니다. 더 열심히 준비해서 돌아오겠습니다!",
            "registered_at" : "2024-09-24 16:40:00",
            "image" : "post4.jpg",
            "fixed" : True,
        }
    },
    {"post" : {
            "post_num" : 5,
            "title" : "[공지] 휘낭시에 구매 요령",
            "content" : "기본 휘낭시에의 경우 영업일에도 재료를 준비하여 2, 3차 굽굽이 진행됩니다. 1차가 매진되었더라도 2, 3차가 있을 수 있으니 휘낭시에 구매를 원하시는 분들은 참고 부탁드립니다 :)",
            "registered_at" : "2024-09-20 17:50:00",
            "image" : "post5.jpg",
            "fixed" : False,
        }
    },
]


def index(request):
    # 최신순 등록일 목록 최대 3개 구하기
    order_list = []
    for data in database:
        order_list.append(data["post"]["registered_at"])
    
    order_list.sort(reverse=True)

    latest_post = []
    for order in order_list:
        for data in database:
            if data["post"]["registered_at"] == order:
                latest_post.append(data)
        if len(latest_post) == 3:
            break

    return render(request, "myblog/index.html", {"latest_posts" : latest_post})

def posts(request):
    # 최신순 등록일 목록 구하기
    order_list = []
    for data in database:
        order_list.append(data["post"]["registered_at"])
    
    order_list.sort(reverse=True)     # ['2024-09-24 16:40:00', '2024-09-23 15:30:00', '2024-09-22 14:20:00', '2024-09-21 13:10:00', '2024-09-20 17:50:00']

    # fixed 최신순 --> unfixed 최신순 전체 글목록 구하기
    ordered_posts = []
    for order in order_list:
        for data in database:
            if data["post"]["fixed"] == True and data["post"]["registered_at"] == order:
                ordered_posts.append(data)
            if data["post"]["fixed"] == False and data["post"]["registered_at"] == order:
                ordered_posts.append(data)

    # 넘버링
    num = len(ordered_posts)
    for ordered in ordered_posts:
        # 정렬 순서 부여
        ordered["post"]["num"] = num
        num -= 1

        # 등록일 연월일로 자르기
        time = ordered["post"]["registered_at"].split(" ")[0]
        ordered["post"]["registered_at"] = time

    return render(request, "myblog/posts.html", {"posts" : ordered_posts})
    
def post_detail(request, post_num):
    for data in database:
        if data["post"]["post_num"] == post_num:
            post_detail = data

    return render(request, "myblog/post_detail.html", {"post_detail" : post_detail})
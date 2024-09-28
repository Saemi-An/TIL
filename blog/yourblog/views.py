from datetime import date
from pprint import pprint

from django.shortcuts import render
from django.http import HttpResponse

from .models import Post, Author, Tag

all_posts = [
    {
        "slug": "hike-in-the-mountains",
        "image": "mountains.jpg",
        "author": "Maximilian",
        "date": date(2021, 7, 21),
        "title": "Mountain Hiking",
        "excerpt": "There's nothing like the views you get when hiking in the mountains! And I wasn't even prepared for what happened whilst I was enjoying the view!",
        "content": """Lorem ipsum dolor sit amet consectetur adipisicing elit. Officiis nobis
          aperiam est praesentium, quos iste consequuntur omnis exercitationem quam
          velit labore vero culpa ad mollitia? Quis architecto ipsam nemo. Odio.

          Lorem ipsum dolor sit amet consectetur adipisicing elit. Officiis nobis
          aperiam est praesentium, quos iste consequuntur omnis exercitationem quam
          velit labore vero culpa ad mollitia? Quis architecto ipsam nemo. Odio.

          Lorem ipsum dolor sit amet consectetur adipisicing elit. Officiis nobis
          aperiam est praesentium, quos iste consequuntur omnis exercitationem quam
          velit labore vero culpa ad mollitia? Quis architecto ipsam nemo. Odio."""
    },
    {
        "slug": "programming-is-fun",
        "image": "coding.jpg",
        "author": "Maximilian",
        "date": date(2022, 3, 10),
        "title": "Programming Is Great!",
        "excerpt": "Did you ever spend hours searching that one error in your code? Yep - that's what happened to me yesterday...",
        "content": """Lorem ipsum dolor sit amet consectetur adipisicing elit. Officiis nobis
          aperiam est praesentium, quos iste consequuntur omnis exercitationem quam
          velit labore vero culpa ad mollitia? Quis architecto ipsam nemo. Odio.

          Lorem ipsum dolor sit amet consectetur adipisicing elit. Officiis nobis
          aperiam est praesentium, quos iste consequuntur omnis exercitationem quam
          velit labore vero culpa ad mollitia? Quis architecto ipsam nemo. Odio.

          Lorem ipsum dolor sit amet consectetur adipisicing elit. Officiis nobis
          aperiam est praesentium, quos iste consequuntur omnis exercitationem quam
          velit labore vero culpa ad mollitia? Quis architecto ipsam nemo. Odio."""
    },
    {
        "slug": "into-the-woods",
        "image": "woods.jpg",
        "author": "Maximilian",
        "date": date(2020, 8, 5),
        "title": "Nature At Its Best",
        "excerpt": "Nature is amazing! The amount of inspiration I get when walking in nature is incredible!",
        "content": """Lorem ipsum dolor sit amet consectetur adipisicing elit. Officiis nobis
          aperiam est praesentium, quos iste consequuntur omnis exercitationem quam
          velit labore vero culpa ad mollitia? Quis architecto ipsam nemo. Odio.

          Lorem ipsum dolor sit amet consectetur adipisicing elit. Officiis nobis
          aperiam est praesentium, quos iste consequuntur omnis exercitationem quam
          velit labore vero culpa ad mollitia? Quis architecto ipsam nemo. Odio.

          Lorem ipsum dolor sit amet consectetur adipisicing elit. Officiis nobis
          aperiam est praesentium, quos iste consequuntur omnis exercitationem quam
          velit labore vero culpa ad mollitia? Quis architecto ipsam nemo. Odio."""
    }
]

def get_date(post):
    return post["last_modified"]

def starting_page(request):
    sorted_posts = sorted(all_posts, key=get_date)   # date를 기준으로 등록일순 정렬(가장 먼저 등록된거 --> 가장 최신)
    latest_posts = sorted_posts[-3:]   # 맨 뒤의 최신 3개 가져오기

    return  render(request, "yourblog/starting_page.html", {
        "posts" : latest_posts
    })

# DB
def query_set_to_list(query_set):
    return [dict(data) for data in query_set]

def db_index(request):
    posts_queryset = Post.objects.values()   # DB에서 쿼리셋(객체목록) 가져오기 + values() = 쿼리셋 값을 딕셔너리 형태로 반환
    posts = query_set_to_list(posts_queryset)   # 쿼리셋 리스트로 형변환
    sorted_posts = sorted(posts, key=get_date)   # date를 기준으로 오름차순 정렬된 리스트 받기: 오래전 등록 --> 최신 등록
    latest_posts = sorted_posts[-3:]   # 최신 등록 top3 
    
    # 태그

    return render(request, "yourblog/db_index.html", { 
        "posts" : latest_posts
    })








def posts(request):
    return  render(request, "yourblog/all_posts.html", {
        "all_posts" : all_posts
    })

# DB
def db_posts(request):
    posts = Post.objects.all().order_by("date")   # 최신순으로 가져오기?? 테스트 필요

    return render(request, "yourblog/db_posts.html", {"posts" : posts})








def post_detail(request, slug):
    identified_post = next(post for post in all_posts if post["slug"] == slug)

    return  render(request, "yourblog/post_detail.html", {
        "post" : identified_post
    })

# DB
def db_detail(reuquest, slug):
    posts_queryset = Post.objects.values()
    posts = query_set_to_list(posts_queryset)

    if slug:
        identified_post = next((post for post in posts if post["slug"] == slug), ("Error"))   # 이터레이션에서 찾는 값 없으면 "Error" 반환
        tag_list_queryset = Post.objects.filter(id=identified_post["id"])[0].tag.all().values()
        tag_list = query_set_to_list(tag_list_queryset)

        tag_name_list = []
        for tag in tag_list:
            tag_name_list.append(tag["tag"])


        # author 이름 가져오기
        author_info_queryset = Author.objects.filter(id=identified_post["author_id"]).values()
        author_info_dict = query_set_to_list(author_info_queryset)[0]
        author_name = author_info_dict["last_name"] + ' ' + author_info_dict["first_name"]
        author_email = author_info_dict["email"]
        
        if identified_post == "Error":
            return HttpResponse("<h1>존재하지 않는 페이지 입니다.</1>")

    return render(reuquest, "yourblog/db_detail.html", {
        "post" : identified_post,
        "author_name" : author_name,
        "author_email" : author_email,
        "tag_list" : tag_name_list
    })

def author_email(request, name, email):
    name = name
    email = email
    return render(request, "yourblog/author_email.html", {
        "name" : name, 
        "email" : email
    })

# list comprehension 풀어보기
# result = None
# ko_letters = ["가", "나", "다", "라", "마", "바", "사"]
# for letter in ko_letters:
#     if letter == "마":
#         result = letter
#         break
# print(result)
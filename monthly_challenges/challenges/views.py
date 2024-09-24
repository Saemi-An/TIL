from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse

monthly_challenges = {
    "january" : "Wake up early in the morning(10 a.m.) and then eat breakfase.",
    "feburary" : "Work out at least 30m, three days a week.",
    "march" : "Run a side project.",
    "april" : "Get a job.",
    "may" : "Start managing your finange. Track your money and start saving plan.",
    "jun" : "Wake up early in the morning(10 a.m.) and then eat breakfase.",
    "july" : "Plan a trip abroad with your company.",
    "august" : "Work out and lose weight up until 55kg.",
    "september" : "Get a hobby where you can make a friend",
    "october" : "Cook for yourself at least 4 times a week.",
    "november" : "Look back for a year and start writing a diary.",
    "december" : "List up what you want to do for the following year. List them up until No.100.",
}

def index(request):
    list_items = ""
    months = list(monthly_challenges.keys())

    for month in months:
        capitalized_month = month.capitalize()
        month_path = reverse("url_name", args=[month])
        list_items += f"<li><a href='{month_path}'>{capitalized_month}</a></li>"

    response_data = f"<ul>{list_items}</ul>"

    return HttpResponse(response_data)

# month가 숫자로 들어왔을 때 --> 함수 내에서 확인 --> 문자 month url로 리다이렉트
def monthly_challenge_by_number(request, month):
    months = list(monthly_challenges.keys())   # ['january', 'feburary', ..]
    
    if month > len(months):
        return HttpResponseNotFound("요청하신 페이지를 찾을 수 없습니다.")
    else:
        redirect_month = months[month - 1]
        redirect_path = reverse("url_name", args=[redirect_month])   # reverse(url 이름이 "url_name"인 곳으로, redirect_month를 인자로)
        return HttpResponseRedirect(redirect_path)

def monthly_challenge(request, month):
    try:
        challenge_text = monthly_challenges[month]
        response_data = f"<h1>{challenge_text}</h1>"
        return HttpResponse(response_data)
    except:
        return HttpResponseNotFound("<h1>요청하신 페이지를 찾을 수 없습니다.</h1>")
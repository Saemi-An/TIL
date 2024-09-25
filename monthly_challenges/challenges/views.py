from django.shortcuts import render
from django.http import Http404, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from django.template.loader import render_to_string

monthly_challenges = {
    "january" : "Wake up early in the morning(10 a.m.) and then eat breakfase.",
    "feburary" : "Work out at least 30m, three days a week.",
    "march" : "Run a side project.",
    "april" : None,
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
    month_list = list(monthly_challenges.keys())

    # context는 json 형태로 넘겨줘야함 
    return render(request, "challenges/index.html", {"month_list" : month_list})

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
        # render(request, 템플렛위치/템플렛명, context(html파일에 넘겨줄 변수))
        return render(request, "challenges/challenge.html", {
                "month" : month,
                "text" : challenge_text
            })
    except:
        raise Http404()
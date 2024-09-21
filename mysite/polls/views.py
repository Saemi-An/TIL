from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404

from .models import Question

import datetime

# 뷰는 클라이언트로부터 request를 받고 (백엔드에서 데이터 추출/저장/파일다운로드 로직 작성 등 코드 작성 후) HttpResponse() 함수를 리턴한다.
def index(request):
    # 현재시각 출력
    now = datetime.datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")

    # 질문들 출력
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # output = ', '.join([q.question_text for q in latest_question_list])

    # loader로 질문 리스트 템플렛에 넘겨주고 템플렛에서 질문 리스트 보여주기
    # template = loader.get_template('polls/index.html')
    # context = {
    #     'latest_question_list' : latest_question_list,
    # }

    # render 사용
    context = {'latest_question_list': latest_question_list}

    # return HttpResponse(f"Hello, world. Current time: {current_time}. \nHere are the questions: {output}")
    # return HttpResponse(template.render(context, request))
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    # 예외처리
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("매치하는 질문 번호가 존재하지 않습니다.")
    # return render(request, 'polls/detail.html', {'question' : question})

    # 숏컷
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question' : question})

def results(request, question_id):
    response = "You're looking at the RESULTS of question %s."
    return HttpResponse(response % question_id)

def vote(reuquest, question_id):
    return HttpResponse("You're VOTING on question %s." % question_id)
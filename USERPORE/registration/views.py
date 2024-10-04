
from django.shortcuts import render, redirect
from django.db.models import Sum
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.http import require_POST

from .forms import RegisterForm   # 폼클래스 불러오기
from .models import Product

from pprint import pprint        

# 모듈 ------------------------------------------------------------------------------------------------------------


# 뷰 ------------------------------------------------------------------------------------------------------------
def product_list(request):
    if request.method == "POST":
        print("포스트 요청이 옴")
        add_to_cart = request.POST.getlist("card_id")   # POST 요청에 담긴 card_id들이 담긴 리스트를 변수에 담음
        
        # 세션에 "cart_items" 키가 없을 경우(장바구니 최초 사용시): 빈 리스트를 할당하여 추후에 상품을 담을 공간을 마련
        if 'cart_items' not in request.session or not isinstance(request.session['cart_items'], list):
            request.session['cart_items'] = []

        request.session['cart_items'].extend(add_to_cart)  # (장바구니를 이미 사용한 경우를 상정하여, 새로운 상품을 추가하는 방식으로) 장바구니 세션에 상품 담기
        request.session.modified = True  # 세션 수정 플래그 설정

        return redirect("/registration")
    
    else:
        print("겟 요청이 옴")
        products = Product.objects.all()
        return render(request, "registration/product-list.html", {
            "products" : products,
        })

def cart(request):
    # 세션 데이터 가져오기
    cart_session = request.session.get('cart_items', [])   # (장바구니를 한번도 사용해보지 않은 유저가 장바구니부터 들어오는 경우를 대비하여) get()으로 장바구니 세션 목록을 변수에 담음
    # print(f"카트 내용: {cart_session}")   # ['1', '1', '1', '4']

    # DB 원본 데이터 가져오기
    cart_items = Product.objects.filter(pk__in=cart_session)

    # 1단계: 원본데이터 json 형식으로 변환
    queryset_dict = cart_items.values()   # apples = <QuerySet [{}, {}]>
    unique_cart_items = [dict(apple) for apple in queryset_dict]   # unique_cart_items = [{}, {}]
    
    # 2단계: cart_session 데이터 형식 수정 - [{"pk" : 카트에 담긴 횟수 int}, {"pk" : 카트에 담긴 횟수 int}]
    cart_quantities = [{data: cart_session.count(data)} for data in set(cart_session)]

    # 3단계: 2와 1을 대조하여 1에 수량 정보를 업데이트
    context_data = []
    for quantity in cart_quantities:
        for item in unique_cart_items:
            berry_key = list(quantity.keys())[0]
            str_ban_id = str(item["id"])
            
            if berry_key == str(str_ban_id):
                item["quantity"] = quantity[f"{berry_key}"]
                context_data.append(item)

    # 총 수량
    total_quantity = sum(data["quantity"] for data in context_data)
    # 총 금액
    total_price = sum(data["pd_price"] * data["quantity"] for data in context_data)

    return render(request, "registration/cart.html", {
        "items" : context_data,
        "total_price" : total_price,
        "total_quantity" : total_quantity,
    })

def delete_cart_item(request):
    if request.method == "POST":
        print("카트에서 포스트 요청옴")
        item_id = request.POST["cart_item_id"]
        print(f"지워야할 상품 아이디: {item_id}")

        cart_items = request.session.get("cart_items", [])
        print(f"현재 카트: {cart_items}")   # ['6', '1', '4', '5', '1']
        while item_id in cart_items:
            cart_items.remove(item_id)
        print(f"지우고 난 뒤의 카트: {cart_items}")

        request.session["cart_items"] = cart_items
        request.session.modified = True  # 세션 수정 플래그 설정

        changed_cart_itmes = request.session.get("cart_items", [])
        print(f"세션이 잘 변경 & 저장 되었나 확인!! {changed_cart_itmes}")

        return HttpResponseRedirect("/registration/cart")
    
def increase_quantity(request):
    if request.method == "POST":
        print("수량 + 포스트 요청옴")
        increase_item_id = list(request.POST["increase_item"])
        print(f"수량 +할 상품 아이디를 리스트에 담음: {increase_item_id}")

        cart_items = request.session.get("cart_items", [])
        print(f"현재 카트: {cart_items}")

        request.session['cart_items'].extend(increase_item_id)  # (장바구니를 이미 사용한 경우를 상정하여, 새로운 상품을 추가하는 방식으로) 장바구니 세션에 상품 담기
        request.session.modified = True  # 세션 수정 플래그 설정

        return HttpResponseRedirect("/registration/cart")

def decrease_quantity(request):
    if request.method == "POST":
        print("수량- 포스트 요청옴")
        decrease_item_id = request.POST["decrease_item"]
        print(f"수량- 상품 아이디: {decrease_item_id}")

        cart_items = request.session.get("cart_items", [])
        print(f"현재 카트: {cart_items}")

        while decrease_item_id in cart_items:
            cart_items.remove(decrease_item_id)
            break
        print(f"지우고 난 뒤의 카트: {cart_items}")

        request.session["cart_items"] = cart_items
        request.session.modified = True  # 세션 수정 플래그 설정

        changed_cart_itmes = request.session.get("cart_items", [])
        print(f"세션이 잘 변경 & 저장 되었나 확인!! {changed_cart_itmes}")

        return HttpResponseRedirect("/registration/cart")


def register(request):
    if request.method == "POST": 
        submitted_data = RegisterForm(request.POST, request.FILES)   # POST 요청이 오면 폼을 전송된 데이터로 채운다 / 파일 데이터는 따로 적어준다
        
        if submitted_data.is_valid():   # 전송된 데이터의 유효성검사 결과가 True 일때, 등록 성공페이지로 redirect
            # print(f"클린 데이터: {submitted_data.cleaned_data}")
            product = Product(
                pd_type=int(submitted_data.cleaned_data["pd_type"]),
                pd_name=submitted_data.cleaned_data["pd_name"],
                pd_note=submitted_data.cleaned_data["pd_note"],
                pd_price=int(submitted_data.cleaned_data["pd_price"]),
                pd_img = submitted_data.cleaned_data["pd_img"]   # 이거 여기 합쳐도 되나??
                )
            product.save()
            # pd_img = Product(pd_img=request.FILES["pd_img"])   # 인풋필드 "pd_img"에서 전송된 파일을 Product 모델(테이블)의 "pd_img" 컬럼 아래에 저장함
            # pd_img.save()
            return redirect("/registration/register-completed")
    else:
        submitted_data = RegisterForm()   # POST 요청이 아닐때, 빈 폼을 보내준다

    return render(request, "registration/register.html", {   # POST 요청이 왔으나 유효성 검사 결과가 False일때, 전송된 데이터로 채워진 폼을 보내준다 --> 에러 메세지가 보이게됨
        "forms" : submitted_data,
    })

def register_completed(request):

    return render(request, "registration/register-completed.html")


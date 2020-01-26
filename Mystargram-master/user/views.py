from django.http import request
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

import post
from follows.models import Follows
from notification.models import Notification
from post.models import Post
from user.models import User
import requests
from bs4 import BeautifulSoup


def index(request):  # 초기화면페이지.
    return render(request, "index.html")


@csrf_exempt
def login(request):  # 로그인 처리,
    if request.method == "POST":
        login_data = request.POST  # action form 에서 받아온 데이터
        id = login_data['user_id']  # 받아온 아이디 변수에 저장
        pw = login_data['pw']  # 받아온 비밀번호 변수에 저장
        login_list = User.objects.filter(user_id=id)  # user 테이블 중 받아온 id값과 같은 데이터를 가져옴

        if login_list.first() == None:  # user 테이블서 가져온 값이 없을때
            return render(request, "index.html")  # 로그인 페이지로 되돌려보냄
        else:  # user 테이블에 가져온 값이 존재할때
            if login_list[0].pw == pw:
                request.session["id"] = login_list[0].user_id  # 세션에 id 값 저장
                request.session["userpic"] = login_list[0].userpic  # 세션에 userpic 값 저장
                user_data = User.objects.filter(user_id=request.session["id"])
                heartList = post.views.heart_count(id)  # 하트가 달려있는 게시물의 아이디를 배열형태로 받아옵니다.

                # 좌측 크롤링 처리파트.
                # url = "https://search.shopping.naver.com/search/all.nhn?query=" + user_data[0].favorite
                # name_list = []
                # price_list = []
                # img_list = []
                # num_list = []
                # total_list = []
                # link_list = []
                # for i in range(0, 6):
                #     result = requests.get(url)
                #     content = BeautifulSoup(result.content, "html.parser")
                #     name = content.select("ul.goods_list div.tit>a.link")
                #     link = content.select("ul.goods_list div.tit>a.link")
                #     price = content.select("div.info>span.price span.num")
                #     img = content.select("div.search_list>ul.goods_list div.img_area>a>img._productLazyImg")
                #
                #     # print(name[i].text)
                #     # print(link[i].get("href"))
                #     # print(price[i].text)
                #     # print(img[i].get("data-original"))
                #
                #     name_list.append(name[i].text)
                #     link_list.append(link[i].get("href"))
                #     price_list.append(price[i].text)
                #     img_list.append(img[i].get("data-original"))
                #     total_list.append('<img src="' + img[i].get("data-original") + '">' + price[i].text + name[i].text)
                #     num_list.append(i + 1)
                #
                # dic = {"link": link_list, "name": name_list, "price": price_list, "img": img_list, "num": num_list,
                #        "total_list": total_list}

                id = request.session["id"]  # 아이디.
                userpic = request.session["userpic"]  # 프사.
                result = post.views.main(request)  # 나의+친구들 포스트 전체 불러오는 함수 호출.
                return render(request, "../../post/templates/main.html", {"result": result ,"heartList":heartList})  # 크롤링풀면서 dic추가.

            else:
                return render(request, "index.html")  # 회원정보불일치, 로그인으로 되돌리기.
    else:
        # 좌측 크롤링 처리파트.
        # url = "https://search.shopping.naver.com/search/all.nhn?query=" + user_data[0].favorite
        # name_list = []
        # price_list = []
        # img_list = []
        # num_list = []
        # total_list = []
        # link_list = []
        # for i in range(0, 6):
        #     result = requests.get(url)
        #     content = BeautifulSoup(result.content, "html.parser")
        #     name = content.select("ul.goods_list div.tit>a.link")
        #     link = content.select("ul.goods_list div.tit>a.link")
        #     price = content.select("div.info>span.price span.num")
        #     img = content.select("div.search_list>ul.goods_list div.img_area>a>img._productLazyImg")
        #
        #     # print(name[i].text)
        #     # print(link[i].get("href"))
        #     # print(price[i].text)
        #     # print(img[i].get("data-original"))
        #
        #     name_list.append(name[i].text)
        #     link_list.append(link[i].get("href"))
        #     price_list.append(price[i].text)
        #     img_list.append(img[i].get("data-original"))
        #     total_list.append('<img src="' + img[i].get("data-original") + '">' + price[i].text + name[i].text)
        #     num_list.append(i + 1)
        #
        # dic = {"link": link_list, "name": name_list, "price": price_list, "img": img_list, "num": num_list,
        #        "total_list": total_list}

        id = request.session["id"]  # 아이디.
        userpic = request.session["userpic"]  # 프사.
        result = post.views.main(request)  # 나의+친구들 포스트 전체 불러오는 함수 호출.
        heartList = post.views.heart_count(id)  # 하트가 달려있는 게시물의 아이디를 배열형태로 받아옵니다.
        return render(request, "../../post/templates/main.html", {"result": result, "heartList":heartList})  # 크롤링풀면서 dic추가.


def signup(request):  # 회원가입
    signup_data = request.POST  # action form 에서 받아온 데이터
    u = User(user_id=request.POST.get("user_id"),
             name=signup_data["name"],
             pw=signup_data["pw"],
             intro=signup_data["intro"],
             userpic=signup_data["userpic"],
             favorite=signup_data["favorite"])
    u.save()
    return render(request, "index.html")  # 로그인 페이지로.


def register(request):  # 회원가입하기 페이지로.
    return render(request, "signup.html")


def idConfirm(request):  # 아이디 중복확인 팝업창.
    return render(request, "id_confirm.html")


def idCheck(request):  # 아이디 중복 여부를 확인.
    id_data = request.POST
    id = id_data["user_id"]
    num0 = [0]
    num1 = [1]
    idValue = [id]
    dic_true = {"data": num0}
    dic_false = {"data": num1, "id": idValue}
    user_data = User.objects.filter(user_id=id)
    if user_data.first() == None:
        return render(request, "id_confirm.html", dic_false)
    else:
        return render(request, "id_confirm.html", dic_true)


def logout(request):  # 로그아웃.
    del request.session["id"]
    return render(request, "index.html")


def mypage(request):  # mypage로 이동.
    ssid = request.session["id"]
    user_data = User.objects.filter(user_id=ssid)  # 세션의 아이디 값으로 db에 있는 내용 불러옴.
    my_followee = read_my_followees_with_name(ssid)  #나의 팔로위 데이터 읽기 함수 호출.
    my_follower = read_my_followers_with_name(ssid)  #나의 팔로워 데이터 읽기 함수 호출.
    my_all_post = read_my_all_post(ssid) #나의 포스팅 데이터 읽기 함수 호출.
    dic_user = {"id": user_data[0].user_id, "name": user_data[0].name, "pw": user_data[0].pw,
                "intro": user_data[0].intro, "favorite": user_data[0].favorite, "userpic": user_data[0].userpic,
                "my_followee": my_followee, "my_follower": my_follower, "my_post": my_all_post}
    return render(request, "mypage.html", dic_user)


def update_mypage(request):  # mypage- 내정보수정.
    data = request.POST

    User.objects.filter(user_id=request.session["id"]).update(name=data["name"], intro=data["intro"],
                                                              favorite=data["favorite"], userpic=data["userpic"])

    return redirect("mypage")


def pw_update(request):  # mypage- 내정보수정 - 비밀번호 수정.
    data = request.POST

    User.objects.filter(user_id=request.session["id"]).update(pw=data["pw"])

    return render(request, "../../post/templates/main.html")


def user_delete(request):  # 회원 삭제- 탈퇴요청처리.
    User.objects.filter(user_id=request.session["id"]).delete()
    del request.session["id"]

    return render(request, "index.html")


def read_my_followees_with_name(id):  # 나의 팔로우스- 나의 **팔로위** 불러오기.
    result = [] #리스트변수.
    for x in Follows.objects.filter(follower=id): #인자로 전달받은 id의 팔로워 매칭데이터를
        result.append((x, x.followee.name)) #위의 리스트안으로 이름과 함께 반복넣기.
    return result


def read_my_followers_with_name(id):  # 나의 팔로우스- 나의 **팔로워** 불러오기.
    result = [] #리스트변수.
    for x in Follows.objects.filter(followee=id): #인자로 전달받은 id의 팔로위 매칭데이터를
        result.append((x, x.follower.name)) #위의 리스트안으로 이름과 함께 반복넣기.
    return result


def read_my_all_post(id):  # 나의페이지 - 나의 포스팅 불러오기.
    result = Post.objects.filter(user_id=id) #인자로받은 나의 아이디를 넣어 필터링 후 담기.
    my_post = [] #배열변수선언.
    for x in result: #읽어온 포스트의 대표이미지(img1)가 될 데이터만 담기.
        if x.img1:
            my_post.append(x)
    print(my_post)
    return my_post


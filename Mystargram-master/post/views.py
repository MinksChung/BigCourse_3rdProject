from django.http import JsonResponse
from django.shortcuts import render, redirect, render_to_response
from django.utils import timezone
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from follows.models import Follows
from heart.models import Heart
from notification.models import Notification
from post.models import Post
from postTag.models import PostTag
from user.models import User


def new_post(request):  # 새글쓰기화면 불러오기.
    ssid = request.session["id"]  #세션정보 변수저장.
    return render(request, 'new_post.html', {
        "notification_counter": Notification.objects.filter(
            userid__user_id=request.session["id"], seen=0).count()
    })  #새글쓰기화면으로 연결, 나의소식 카운팅 데이터전달


def time_getter(item):  # list_sort key Fnc. # lambda (item:item[0].time)
    return item[0].time


def followees_posts(id):  # 내친구들 포스트 갖고오기.
    f_list = Follows.objects.filter(follower=id)
    posts = []
    mine = []
    my_post = Post.objects.filter(user_id=id)
    for x in my_post:
        tags = list(PostTag.objects.filter(post_id=x.id).values_list('word', flat=True))
        mine.append((x, x.user_id.userpic, x.user_id, tags))

    for follow in f_list:
        for post in Post.objects.filter(user_id=follow.followee_id):
            tags = list(PostTag.objects.filter(post_id=post.id).values_list('word', flat=True))
            posts.append((post, follow.followee.userpic, follow.followee.name, tags))

    all_post = mine + posts
    all_post.sort(key=time_getter)

    return all_post


def get_myf_userpic(f_list):  # 내친구들 프사 사진 갖고오기.
    myf_userpic = []
    for x in f_list:
        myf_userpic.append(User.objects.filter(user_id=x).values("userpic"))
    return myf_userpic


def split_tags(tags):  # 글쓰기 입력시, 태그필드 별도 저장처리.
    output = []  # 배열로 받을 준비.
    splitted = tags.split("#")  # 샵을 기준으로 들어온 인자를 쪼개서 splitted 변수 안에 담아서,
    for split in splitted:
        stripped = split.strip()  # 반복문 통해서 앞뒤의 공백을 없애고,
        if stripped:  # 공백제거 처리된후 output 배열로 넣어준다,
            # false인 경우는 패스(' ' 와 같은 경우 공백제거로 false가 처리, 자동패스됨)
            output.append(stripped)
    return output  # 결과값 리턴.


def submit_post(request):  # 글쓰기 인서트.
    post = Post(
        img1=request.POST["img1"],
        img2=request.POST["img2"],
        img3=request.POST["img3"],
        content=request.POST["content"],
        user_id=User.objects.filter(user_id=request.session["id"]).get())  # 세션에 담겨있는 유저아이디로 저장.
    post.save()  # 포스트테이블 부분 서버로 저장완료.
    tags = split_tags(request.POST["tag"])  # 태그부분에 담긴 글을 split_tag 함수를 통해 쪼갠 후 tags 변수 안에 담기.
    for tag in tags:
        dto = PostTag(word=tag, post_id=post)
        dto.save()  # 포스트태그_테이블로 단어와, 포스트id를 반복적으로 디비저장처리.
    return redirect("home")  # 메인 페이지 보내기.


def read_post_detail(request): #나의글 수정/삭제를 위한 해당포스팅 데이터 읽어오기.
    pid = request.POST.get("pid") #포스팅의 id를 받아서.
    dto = Post.objects.get(id=pid) #해당 내용을 불러오고.
    tag_list = list(PostTag.objects.filter(post_id=pid).values_list('word', flat=True)) #태그불러오기.
    tags = '#'.join(tag_list) #단어로 분리되어 DB로 삽입된 태그를 조인.
    return render(request, "edit_post.html", {"dto": dto, "tags": tags})


def main(request):
    session_id = request.session["id"]
    # 나의 친구들과 나의 아이디+프사+포스트(내용,이미지123)+태그 를 가져올 get_all_posts 함수를 할당
    all_posts = get_all_posts(session_id)
    return all_posts


def back_to_main(request):
    id = request.session["id"]
    userpic = request.session["userpic"]
    result = get_all_posts(id)
    return render(request, "main.html", {"result": result})


# sort함수를 사용하기 위한 함수 정의
def sort_time(things):
    return things[0].time


## 나와 친구들(팔로우 관계)의 [게시물 + 해당유저 프로필사진 + 해당 유저 아이디]을 모두 불러 오는 함수
def get_all_posts(session_id):
    myf_list = Follows.objects.filter(follower_id=session_id)
    myf_posts = []
    for follow in myf_list:
        for post in Post.objects.filter(user_id=follow.followee_id):
            tags = list(PostTag.objects.filter(post_id=post.id).values_list('word', flat=True))
            myf_posts.append((post, follow.followee.userpic, follow.followee.user_id, tags))
    my_posts = Post.objects.filter(user_id=session_id)
    my_result = []

    for my in my_posts:
        tags = list(PostTag.objects.filter(post_id=my.id).values_list('word', flat=True))
        my_result.append((my, my.user_id.userpic, my.user_id.user_id, tags))

    all_post = my_result + myf_posts
    all_post.sort(key=sort_time, reverse=True)  # key=해당 테이블의 정렬할 컬럼을 지정해줄 함수명 , reverse=True:내림차순
    return all_post


def select_user(request, user_id):
    user_posts = Post.objects.filter(user_id=user_id)
    user_result = []
    for user in user_posts:
        tags = list(PostTag.objects.filter(post_id=user.id).values_list('word', flat=True))
        user_result.append((user, user.user_id.userpic, user.user_id.user_id, tags))
    user_result.sort(key=sort_time, reverse=True)
    result_followees = friends_follows(request, user_id)
    dic_data = {"user_result": user_result, "result_followees": result_followees}
    return render(request, "select_user.html", dic_data)


def friends_follows(request, user_id):  # 친구추천(내친구의 친구검색)
    session_id = request.session["id"]
    my_followees = []
    for my_followee in Follows.objects.filter(follower_id=session_id).values_list("followee_id", flat=True):
        my_followees.append(my_followee)
    f_followees = []
    for f_followee in Follows.objects.filter(follower_id=user_id).values_list("followee_id", flat=True):
        f_followees.append(f_followee)
    my_followees_set = set(my_followees)
    f_followees_set = set(f_followees)
    result_followees_set = f_followees_set - my_followees_set
    result_followees = list(result_followees_set)
    return result_followees


def post_update(request): #나의 글 업데이트.
    id = request.POST.get("pid")
    dto = Post(id=id,
               img1=request.POST["img1"],
               img2=request.POST["img2"],
               img3=request.POST["img3"],
               content=request.POST["content"],
               user_id=User.objects.filter(user_id=request.session["id"]).get(),
               time=timezone.now()) # 글을 수정받고, 시간을 새로운 시간으로 갱신.
    dto.save()
    PostTag.objects.filter(post_id=id).delete() #기존의 태그데이터를 삭제하고.
    tags = split_tags(request.POST["tag"])  #새로운 태그를 받아 split_tags 함수로 정리 후,
    for tag in tags:                                #반복문을 통해 태그테이블로 세이브처리.
        id = request.POST.get("pid")
        tag = PostTag(word=tag, post_id=dto)
        tag.save()
    return redirect("mypage")  # 메인 페이지 보내기.


def post_delete(request): #나의글 삭제
    id = request.POST.get("pid") #포스트의 id를 받아와서.
    Post.objects.get(id=id).delete()  #해당포스트를 삭제.
    PostTag.objects.filter(post_id=id).delete() #해당 포스트의 태그를 삭제.
    return redirect("mypage")


def search(request):
    data = request.POST
    input_data = request.POST.get("input_data")
    box = request.POST.get("box")
    if (box == "태그"):
        input_tag = input_data
        search_post_ids = PostTag.objects.filter(word=input_tag).values_list("post_id_id", flat=True)
        search_posts = []
        for search_post_id in search_post_ids:
            for search_post in Post.objects.filter(id=search_post_id):
                tags = list(PostTag.objects.filter(post_id=search_post.id).values_list('word', flat=True))
                search_posts.append((search_post, search_post.user_id.userpic, search_post.user_id.user_id, tags))

    elif (box == "아이디"):
        input_id = input_data
        search_posts = []
        for search_post in Post.objects.filter(user_id=input_id):
            tags = list(PostTag.objects.filter(post_id=search_post.id).values_list('word', flat=True))
            search_posts.append((search_post, search_post.user_id.userpic, search_post.user_id.user_id, tags))

    return render(request, "../../post/templates/search.html", {"search_result": search_posts})


def heart(request):  # 하트 ajax 실시간 작용
    print("views로 넘어왔어요!!!")
    user = request.GET["user_id"]
    postID = request.GET["pid"]
    try:
        Heart.objects.get(user_id_id=user, post_id_id=postID)
        heartCounting = Heart.objects.filter(post_id_id=postID)
        Heart.objects.filter(user_id_id=user, post_id_id=postID).delete()
        successData = "delete"
        print("DB에 삭제되었어요!!")
        print("하트가 몇개 있을까요????>>>>", heartCounting.count())
        heartCount = heartCounting.count()

    except Exception as e:
        print("DB에 없어서 오긴 했어요...")
        h = Heart(post_id_id=postID, user_id_id=user)
        h.save()
        heartCounting = Heart.objects.filter(post_id_id=postID)
        successData = "save"
        print("DB에 저장되었어요!!")
        print("하트가 몇개 있을까요????>>>>", heartCounting.count())
        heartCount = heartCounting.count()
    result = {
        "result": successData,
        "heartCount": heartCount
    }
    return JsonResponse(result)


def heart_count(id):  # 하트가 박혀있는 게시물의 아이디를 구하는 함수 <최지수>
    heart = Heart.objects.filter(user_id_id=id).order_by('-post_id_id')  # 하트가 박혀있는 모든 DB데이터를 가져옵니다.
    heartList = []  # 하트가 박혀있는 게시물의 아이디를 저장하기 위한 배열을 선언해줍니다.
    for i in heart:  # DB서 가져온 데이터를 i로 for문 돌려줍니다.
        heartList.append(i.post_id_id)  # DB서 가져온 데이터 중 게시물 아이디를 배열에 저장해줍니다.
    return heartList


######################################################################MAP

def get_exif(filename): #이미지의 메타데이터 추출 라이브러리 사용 함수.
    exif = Image.open(filename)._getexif() #함수파라메터값으로 들어온 이미지를 오픈.
    if exif is not None:
        for key, value in exif.items(): #이미지에 포함된 메타의 키와 밸류를 분리하여
            name = TAGS.get(key, key) #각각 전달 처리.
            exif[name] = exif.pop(key)
        if 'GPSInfo' in exif:  #필요한 정보의 키를 특정하여, (현 경우는 GPSInpo)
            for key in exif['GPSInfo'].keys():  #특정된 키 범위안의 데이터를
                name = GPSTAGS.get(key, key)  #오브젝트형태로 다시반복확보처리.
                exif['GPSInfo'][name] = exif['GPSInfo'].pop(key)

    #받은 GPS의 자료로 위도, 경도를 계산하기위해 필요한 값은 있으나 해당 키의 명칭이 부정확하게
    #표기되는 것을 발견하여, 해당 값에 필요한 명칭(키)를 정의하여 데이터를 추가삽입처리.
    exif['GPSInfo']['GPSLatitude'] = exif['GPSInfo'][2]
    exif['GPSInfo']['GPSLongitudeRef'] = exif['GPSInfo'][3]
    return exif  #GPS가 포함된 데이터를 리턴.


def Longitude(y): #경도계산을 위한 함수.
    e = y['GPSInfo']['GPSLongitude']
    ref = y['GPSInfo']['GPSLongitudeRef']
    Longitude = (e[0][0] / e[0][1] +
                 e[1][0] / e[1][1] / 60 +
                 e[2][0] / e[2][1] / 3600
                 ) * (-1 if ref in ['S', 'W'] else 1)
    print("Longitude:", Longitude)
    return Longitude


def Latitude(y): #위도계산을 위한 함수.
    e = y['GPSInfo']['GPSLatitude']
    ref = y['GPSInfo']['GPSLatitudeRef']
    Latitude = (e[0][0] / e[0][1] +
                e[1][0] / e[1][1] / 60 +
                e[2][0] / e[2][1] / 3600
                ) * (-1 if ref in ['S', 'W'] else 1)
    print("Latitude:", Latitude)
    return Latitude


def decimal_form(x, y):
    gps = []
    gps.append(x)
    gps.append(y)
    return gps


def get_gps(request): #이미지의 위도경도 추출 시 호출함수.
    the_pic = request.POST.get("the_pic") #이미지의 파일명지정.
    info = get_exif('static/img/' + the_pic) #메타데이터 추출함수에 인자로 전달.
    long = Longitude(info) #위의 함수 리턴값을 경도,
    lat = Latitude(info) #위도에 각각 넣어 확보.
    result = decimal_form(lat, long) #최종 [위도,경도]
    gps = {'lat': result[0], 'long': result[1]} #최종값을 딕셔너리 형태로 전달.
    return render(request, 'init_map.html', gps) # 맵 출력을 위한 팝업창을 연결, 데이터전달.

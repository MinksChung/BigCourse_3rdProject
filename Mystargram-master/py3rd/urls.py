from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

import follows.views
import heart.views
import post.views
import notification.views
import user.views

urlpatterns = [
    #<회원가입>
    path('admin/', admin.site.urls),
    path('register', user.views.register),  # 회원가입으로 가기 위한 경로/
    path('signup', user.views.signup),  # 회원가입 처리를 위한 경로/
    path('id_confirm', user.views.idConfirm),  # 아이디 중복확인을 위한 팝업창에 가기 위한 경로/
    path('id_check', user.views.idCheck),  # 아이디 중복확인하기 위한 경로/

    #<시작페이지, 로그인, 로그아웃>
    path('', user.views.index), #시작페이지/
    path('home', user.views.login, name="home"),  # 로그인 처리를 위한 경로/
    path('logout', user.views.logout),  # 로그아웃을 실행하는 경로/

    #<마이페이지-내정보수정/>
    path('mypage', user.views.mypage, name="mypage"),  # 마이페이지로 이동 ( 팔로우, 포스팅 탭 포함)/
    path('update_mypage', user.views.update_mypage),  # 내 정보 수정/
    path('pw_update', user.views.pw_update),  # 비밀번호 수정/
    path('user_delete', user.views.user_delete),  # 회원 삭제(탈퇴)/

    #<마이페이지-나의팔로우>
    path('del_followship', follows.views.del_followship), #팔로잉끊기/
    path('start_followship', follows.views.start_followship), #팔로잉시작(친추기능)/

    #<포스팅글쓰기/ 마이페이지-나의포스팅(수정/삭제)>
    path('new_post', post.views.new_post),  #새글쓰기연결./
    path('main', post.views.submit_post),  # 글쓰기완료 후 완료신청버튼./
    path('detail', post.views.read_post_detail), #포스팅 수정/삭제신청 클릭 후 디테일페이지./
    path('post_delete', post.views.post_delete), #포스팅 삭제./
    path('post_update',post.views.post_update), #포스팅 수정 업데이트./

    #<검색 및 부가기능>
   path('uid_<str:user_id>', post.views.select_user, name="select_user"), #특정유저의 포스트만 갖고오기/
   path('gpsmap', post.views.get_gps, name='gpsmap'), #이미지의 GPS메타 추출/
   path('search', post.views.search), #검색창 검색기능(태그,아이디)/
   path('heart', post.views.heart), #게시물 하트 추가/삭제, 하트카운트 기능/
   path('notification/read_all', notification.views.read_all), #새로운 소식 읽어오기/
   path('notification/count', notification.views.count), #새로운 소식의 갯수 읽어오기/

]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]

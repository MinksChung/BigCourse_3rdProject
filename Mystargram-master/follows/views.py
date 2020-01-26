from django.shortcuts import render, redirect

from follows.models import Follows


def del_followship(request): #팔로우 취소
    id = request.POST.get("fid") #취소할 친구의 아이디를 포스트로 받기.
    ssid=request.session.get("id") #나의 세션정보.
    Follows.objects.filter(follower_id=ssid, followee_id=id).delete() #위와 매칭데이터 삭제.
    return redirect("mypage")

def start_followship(request): #팔로잉 시작
    ssid=request.session.get("id")
    id=request.POST.get("fid")
    dto=Follows(
        followee_id=id,
        follower_id=ssid
    )
    dto.save()
    return redirect("home")

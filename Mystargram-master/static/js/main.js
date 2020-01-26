$(document).ready(function () //페이지 모두 읽고난다음에 아래의 함수를 실행.
{
    var badge_text = $("#news_badge").text() //뉴스배지 컴포넌트를 변수에 담기.
    var notification_counter = parseInt(badge_text); //위의 변수타입을 숫자로 넣고, 새로운 변수명 지정.

    if (badge_text.length > 0 && notification_counter > 0) { // 0개 이상일때만 보여주기.
        $("#news_badge").show(); //0개 이상이면 뉴스배지가 보여지고,
    } else {
         $("#news_badge").hide(); //아닌경우 보이지 않음.
    }
   var popOpen = false; //팝오픈 변수의 기본값을 fasle로 설정
    $("#my_news").on("click", function () {  //마이뉴스 버튼을 클릭할 때,
        popOpen = !popOpen; //팝오픈의 상태가 반대로 변경되고, (False -> True , Ture->False)
        if (popOpen) {  //팝오픈이 True 상태일때,
            $.get("/notification/read_all", function (data) { // notification/read_all 함수를 호출, 성공하면 콜백함수(success)
                //notifications 변수에 map으로 리턴값을 필요한데이터+원하는 텍스트로 담는 처리를 하고, join으로 줄바꿈을 처리.
                var notifications = data.notifications.map(function (notification) {
                    return "  "+ notification.fromid+ "님이 회원님의 게시물을 좋아합니다!";
                }).join("\n")

                $('#popoverb').text(notifications) //위 변수에 담긴 notifications를 팝오버 텍스트로 표시.
                $("#news_badge").hide(); // 뉴스배지다시숨긴다.
            });
            $('#popoverb').fadeTo(500, 1)
        }else {
            $('#popoverb').fadeTo(500, 0)
        }
    });

    setInterval(function () { //정해진 시간마다 자동호출 (매 10초로 설정)
        $.get("/notification/count", function (data) { //notification/count 함수를 호출
            if (data.notification_counter > 0) { //카운팅 결과값이 0보다 큰 경우,
                $("#news_badge").text(data.notification_counter); //뉴스배지의 텍스트 값으로 주어지고,
                $("#news_badge").show(); //뉴스배지가 보이게 처리.
            }
        });
    }, 10 * 1000); // 10초마다
});


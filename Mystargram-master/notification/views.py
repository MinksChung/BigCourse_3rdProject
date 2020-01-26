from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from notification.models import Notification

@csrf_exempt
def count(request):
    return JsonResponse({
        "notification_counter": Notification.objects.filter(userid__user_id=request.session["id"], seen=0).count()
    })

@csrf_exempt
def read_all(request):
    notification_objects = Notification.objects.filter(userid__user_id=request.session["id"], seen=0)
    notifications = []

    for notification in notification_objects:
        notifications.append({
            "fromid": notification.fromid.user_id,
            "note_type": notification.note_type
        })

    #notification_objects.update(seen=1)

    return JsonResponse({
        "status": "OK",
        "notifications": notifications
    })
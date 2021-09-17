from django.shortcuts import render
from rest_framework.response import Response
from notifications.signals import notify
from django.contrib.auth import get_user_model
from .serializers import NotificationSerializer
from rest_framework import status
from notifications.models import Notification
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
import json
from asgiref.sync import async_to_sync
from django.shortcuts import render, HttpResponse
from users.models import User
from rest_framework.decorators import APIView

# Create your views here.
def index(request):
    return render(request, 'notification/index.html')

def room(request, room_name):
    return render(request, 'notification/room.html', {
        'room_name': room_name
    })



# Create your models here.
User = get_user_model()

class NotificationView(APIView):
    serializer_class = NotificationSerializer

    def get(self, request, *args, **kwargs):
        queryset = Notification.objects.filter(recipient_id=request.user.id).all()
        ser_data = NotificationSerializer(queryset, many=True)
        count = queryset.count()
        data = {
            'unread_count': count,
            "notifications_list": ser_data.data
        }
        return Response(data)


# class AllNotificationCount(APIView):
#     serializer_class = NotificationSerializer

#     def get(self, request, *args, **kwargs):
#         queryset = Notification.objects.filter(recipient_id=request.user.id)
#         count = queryset.count()
#         data = {
#             'all_count': count
#         }
#         return Response(data)

# class UnreadNotificationsList(APIView):
#     serializer_class = NotificationSerializer

#     def list(self, request, *args, **kwargs):
#         queryset = Notification.objects.filter(recipient_id=request.user.id, unread=True)
#         return Response(NotificationSerializer(queryset, many=True).data)



@receiver(post_save, sender=Notification)
def notification_handeler(sender, instance, created, *args, **kwargs):
    if created:
        ser = NotificationSerializer(instance)
        channel_layer = get_channel_layer()

        if  isinstance(instance.recipient, list):

            for user in instance.recipient:
                #print(f'from 1 {user}')
                async_to_sync(channel_layer.group_send)(
                    f"notification_{user.username}_{user.id}",
                    {
                        'type': 'send_notification',
                        'message': json.dumps(ser.data)
                    }
                )
        # elif instance.recipient.model is User:
        #     print(f'from 2 {instance}')
        #     async_to_sync(channel_layer.group_send)(
        #                 f"notification_{instance.recipient.username}_{instance.recipient.id}",
        #                 {
        #                     'type': 'send_notification',
        #                     'message': json.dumps(ser.data)
        #                 }
        #             )
            
        else:
            #print(f'from 3 {instance.recipient}')
            async_to_sync(channel_layer.group_send)(
                        
                        f"notification_{instance.recipient.username}_{instance.recipient.id}",
                        {
                            'type': 'send_notification',
                            'message': json.dumps(ser.data)
                        }
                    )
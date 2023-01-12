from directs.views import inbox, Directs, SendDirect, NewConversation
from django.urls import path

urlpatterns = [
    path('', inbox, name="message"),
    path('<username>',Directs, name='direct'),
    path('send/',SendDirect, name='send-directs'),
    path('new/<username>', NewConversation, name="conversation"),
]
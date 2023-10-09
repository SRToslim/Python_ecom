from django.urls import path

from .views import *

urlpatterns = [
    path('user/chat/', ChatBox, name='chat_box'),
    path('user/chat-user-search/<search>', searchUser, name='chat_user_search'),
    # path('user/chat-user-search/', searchUser, name='chat_user_search'),
    # path('send_message/<int:recipient_id>/', send_message, name='send_message'),
    path('send_message/', send_message, name='send_message'),
]

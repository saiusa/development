from django.urls import path
from .exam_views import ChatView

urlpatterns = [
    path('chat/', ChatView.as_view(), name='chat_view'),
]
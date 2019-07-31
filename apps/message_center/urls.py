from django.urls import path
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from apps.message_center.views import UnreadMessageCount

urlpatterns = [  
    # 用户注册
    url(r'^us_reg/$',UnreadMessageCount.as_view()),
]

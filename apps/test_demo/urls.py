from django.urls import path
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from apps.test_demo.views import GenerateUser,GenerateUser2,GenerateUser3,GenerateUser4,GenerateUser5,GenerateUser1,GenerateUser6,GenerateUser7

urlpatterns = [  
    # 用户注册  按当前排列顺序来
    url(r'^us_g1/$',GenerateUser1.as_view()),
    url(r'^us_g6/$',GenerateUser6.as_view()),
    url(r'^us_g2/$',GenerateUser2.as_view()),
    url(r'^us_g3/$',GenerateUser3.as_view()),
    url(r'^us_g7/$',GenerateUser7.as_view()),
    url(r'^us_g4/$',GenerateUser4.as_view()),
    url(r'^us_g5/$',GenerateUser5.as_view()),
    url(r'^us_g/$',GenerateUser.as_view()),
]

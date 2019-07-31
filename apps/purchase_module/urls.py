from django.urls import path
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from apps.index_show.views import UserRegistrationView,SendVerificationCode,LoginView,AllContentShow

urlpatterns = [  
    # 用户注册
    url(r'^us_reg/$',UserRegistrationView.as_view()),
    # 发送/验证短信验证码
    url(r'^send_sms/$',SendVerificationCode.as_view()),
    url(r'^login/$',LoginView.as_view()),
    url(r'^all_list/$',AllContentShow.as_view()),
]

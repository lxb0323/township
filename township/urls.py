"""township URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api/(?P<version>[v1|v2]+)/index_show/', include('index_show.urls')),
    url(r'^api/(?P<version>[v1|v2]+)/write_operate/', include('writing_module.urls')),
    url(r'^api/(?P<version>[v1|v2]+)/buy/', include('purchase_module.urls')),
    url(r'^api/(?P<version>[v1|v2]+)/user_action/', include('user_action.urls')),
    url(r'^api/(?P<version>[v1|v2]+)/shop_show/', include('shop_show.urls')),
    url(r'^api/(?P<version>[v1|v2]+)/test/', include('test_demo.urls')),
    path('media/<path:path>',serve,{'document_root':settings.MEDIA_ROOT}),
]

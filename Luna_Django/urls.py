"""Luna_Django URL Configuration

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
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib.auth import login as login
from django.contrib.auth import logout as logout
# todo logout issues
# https://docs.djangoproject.com/en/2.1/_modules/django/contrib/auth/

urlpatterns = [
    url('', include('Luna.urls'), name='luna'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^auth/', include('social_django.urls', namespace='social')),
    url(r'^admin/', admin.site.urls),
    url(r'^coin/', include(('coin.urls', 'sharing'), namespace='sharing')), #Coin sharing URL
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

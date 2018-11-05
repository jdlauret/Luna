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
from django.urls import path
from Luna.urls import views
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    url('', include('Luna.urls'), name='luna'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^auth/', include('social_django.urls', namespace='social')),
    url(r'^admin/', admin.site.urls),
    url(r'^coin/', include(('coin.urls', 'sharing'), namespace='sharing')), #Coin sharing URL
    url(r'^P_Tracker/', include(('P_Tracker.urls', 'tracker'), namespace='tracker')), #Tracker URL
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

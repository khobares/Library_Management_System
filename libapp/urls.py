from django.conf.urls import url
from . import views
import os
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about$', views.about, name='about'),
    url(r'^(?P<item_id>\d+)/$', views.detail, name='detail'),
    url(r'^suggestions$', views.suggestions, name='suggestions'),
    url(r'^newitem$', views.newitem, name='newitem'),
    url(r'^searchlib$',views.searchlib, name='searchlib'),
    url(r'^result$', views.result, name='result'),
    url(r'^login$', views.user_login, name='login'),
    url(r'^logout$', views.user_logout, name='logout'),
    url(r'^myitems$', views.myitems, name='myitems'),
    url(r'^register$', views.register, name='register'),
    url(r'^book$', views.book, name='book'),
    url(r'^dvd$', views.dvd, name='dvd'),
    url(r'^other$', views.other, name='other'),
    url(r'^suggestdetail/(?P<suggest_id>\d+$)', views.suggestdetail, name='suggestdetail')

        ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from musicus import views

urlpatterns = [
    url(r'^test/$', views.Hello.as_view()),
    url(r'^song/$', views.Song.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)

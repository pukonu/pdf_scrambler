from django.conf.urls import url
from .controllers import generate, rearrange, home

urlpatterns = [
    url(r'^generate$', generate),
    url(r'^rearrange', rearrange),
    url(r'^$', home),
]

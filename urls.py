from django.conf.urls import url

from . import views

urlpatterns = [
    # e.g. /steamgames/
    url(r'^$', views.index, name='index'),
    # e.g. /steamgames/user/
    # OR
    # /steamgames/user,user2,user3/
    url(r'^(?P<steamusers>[\w,]+)$', views.detaillist, name='detaillist'),
    # e.g. /steamgames/user1,user2/useradd
    url(r'(?P<steamusers>[\w,]+)/(?P<to_add>[^/]+)', views.addcomparison, name='addcomparison'),
]

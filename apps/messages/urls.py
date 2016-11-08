from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    url('^$', login_required(views.MessagesIndexView.as_view()), name='index'),
    url('^(?P<username>[\w-]+)/$',
        login_required(views.MessagesDetailView.as_view()),
        name='detail'),
]

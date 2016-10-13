from django.conf.urls import patterns, include, url

from django.contrib import admin

from hello import views as hello_views
from requests_history import views as requests_hisory_views
admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'fortytwo_test_task.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', hello_views.HelloView.as_view(), name='hello'),
    url(r'^requests_history/$',
        requests_hisory_views.RequestsHistoryView.as_view(),
        name='requests_history')
)

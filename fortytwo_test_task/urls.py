from registration.backends.simple.views import RegistrationView

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from hello import views as hello_views
from requests_history import views as requests_hisory_views
admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'fortytwo_test_task.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout,
        {'template_name': 'registration/logout.html'}, name='logout'),
    url(r'^register/$',
        RegistrationView.as_view(get_success_url=lambda request, user: '/'),
        name='register'),
    url(r'^$', hello_views.HelloView.as_view(), name='hello'),
    url(r'^edit_hello/$',
        login_required(hello_views.HelloEditView.as_view()),
        name='edit_hello'),
    url(r'^requests_history/$',
        requests_hisory_views.RequestsHistoryView.as_view(),
        name='requests_history'),
    url(r'^pull_new_requests/$',
        requests_hisory_views.RequestsPullingView.as_view(),
        name='pull_new_requests')
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

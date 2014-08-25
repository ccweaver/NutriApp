from django.conf.urls import patterns, include, url
from nutri.views import nutriForm

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'nutri.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^', nutriForm),
    url(r'^admin/', include(admin.site.urls)),
)

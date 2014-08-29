from django.conf.urls import patterns, include, url
from nutri.views import ingredient, add_restaurant


from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'nutri.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^add_ingredient$', ingredient),
    url(r'^add_restaurant$', add_restaurant),
    url(r'^admin/', include(admin.site.urls)),
)

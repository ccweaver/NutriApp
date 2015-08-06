from django.conf.urls import patterns, include, url
from nutri.views import dish, add_restaurant, restaurant_profile, sign_in, search_results


from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'nutri.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', sign_in),
    url(r'^search/(.+)/(\d)$', search_results),
    url(r'^search/(.+)$', search_results),
    url(r'^add_dish/(\d+)$', dish),
    url(r'^add_restaurant/$', add_restaurant),
    url(r'^restaurant_profile/(\d+)$', restaurant_profile),
    url(r'^admin/', include(admin.site.urls)),

)

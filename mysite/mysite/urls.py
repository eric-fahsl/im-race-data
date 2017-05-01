from django.conf.urls import include, url
from django.contrib import admin

# from myapp.views import home

urlpatterns = [
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home')
    # url(r'^blog/', include('blog.urls')),

    # url(r'^admin/', include(admin.site.urls)),
    # url(r'', 'main.views.home')

    # url(r'^$', home, name='home')
     url(r'^$', include('main.urls')),
]

from django.conf.urls import patterns, include, url
from django.contrib import admin
from main.views import youtubebot
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'youtubebot.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^facebook_auth/', youtubebot.as_view()),
)

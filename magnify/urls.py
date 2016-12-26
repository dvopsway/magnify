from django.conf.urls import patterns, include, url
from django.contrib import admin
from reporttool.views import *
admin.autodiscover()
urlpatterns = [
    url(r'', include('reporttool.urls', namespace="report")),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
]

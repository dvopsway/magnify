from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^$', 'reporttool.views.home', name='home'),
    url(r'^get_params/', 'reporttool.views.get_params', name='get_params'),
    url(r'^load_report/(?P<report_name>.*)/$',
        'reporttool.views.load_report', name='load_report'),
    url(r'^pdf_generate/', 'reporttool.views.pdf_generate', name='pdf_generate'),
    url(r'^csv_generate/', 'reporttool.views.csv_generate', name='csv_generate'),
]

from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'uniprotmq.site_main.views.search', name='search'),
)

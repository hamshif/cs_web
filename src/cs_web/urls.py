from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cs_web.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'cs_web.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^billboard/', include('billboard.urls', namespace='billboard')),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

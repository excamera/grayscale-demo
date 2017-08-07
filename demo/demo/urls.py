from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^jobs/$', views.jobs, name='jobs'),
    url(
        r'^favicon.ico$',
        RedirectView.as_view(
            url=staticfiles_storage.url('favicon.ico'),
            permanent=False),
        name="favicon"
    ),    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

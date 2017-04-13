from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^call_mu/$', views.call_mu, name='call_mu'),
    url(r'^call_mu_stub/$', views.call_mu_stub, name='call_mu_stub'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

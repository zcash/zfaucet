from django.urls import re_path
from django.conf.urls.static import static
from django.conf import settings



from . import views

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
]


#TODO: check if dev or prod and only use below in dev
urlpatterns += urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


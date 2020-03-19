from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('new', views.newstudent),
    path('new_form_submission', views.new_form_submission),
    path('information', views.information)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
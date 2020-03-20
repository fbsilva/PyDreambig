from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('new', views.new_student),
    path('new_form_submission', views.new_form_submission),
    path('information', views.information),
    path('successful', views.successful),
    path('student_info/<int:student_id>/', views.student_info, name='student_info')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
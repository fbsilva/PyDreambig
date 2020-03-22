from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('new', views.new_student),
    path('add', views.add_student),
    path('edit_student', views.edit_student),
    path('information', views.information),
    path('successful', views.successful),
    path('edit/<int:student_id>/', views.student_info, name='edit')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
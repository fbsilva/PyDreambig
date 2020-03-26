from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.generic import RedirectView
from . import views


urlpatterns = [
    path('', views.index),
    path('new', views.new_student),
    path('add', views.add_student),
    path('edit_student', views.edit_student),
    path('information', views.information),
    path('settings', views.settings),
    path('successful', views.successful),
    path('edit/<int:student_id>/', views.student_info, name='edit'),
    path('student_class/<int:levelId>/', views.student_class, name='student_class'),
    path('settings/public_school', views.public_school_add),
    path('settings/public_school/<int:levelId>/', views.public_school_edit, name='public_school'),
    path('settings/grade', views.grade_add),
    path('settings/grade/<int:grade_id>/', views.grade_edit, name='grade'),
    path('settings/level', views.level_add),
    path('settings/level/<int:level_id>/', views.level_edit, name='level')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

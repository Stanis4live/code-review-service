from django.urls import path
from . import views


urlpatterns = [
    path('upload/', views.upload_file, name='upload_file'),
    path('file_list/', views.file_list, name='file_list'),
    path('edit_file/<int:file_id>/', views.edit_file, name='edit_file'),
    path('view_file/<int:file_id>/', views.view_file, name='view_file'),
    path('delete_file/<int:file_id>/', views.delete_file, name='delete_file'),

]

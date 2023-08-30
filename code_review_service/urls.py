from django.contrib import admin
from django.urls import path, include
from apps.users import views as user_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('accounts/', include('apps.users.urls')),
    path('', user_views.home_view, name='home'),
]

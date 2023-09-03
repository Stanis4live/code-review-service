from django.contrib import admin
from django.urls import path, include
from apps.users import views as user_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path('accounts/', include('apps.users.urls')),
    path('files/', include('apps.files.urls')),
    path('', user_views.home_view, name='home'),
]


# Проверяет, находится ли Django в режиме разработки  (DEBUG = True в settings.py)
if settings.DEBUG:
    # Создает URL-паттерны для обработки медиафайлов.
    # settings.MEDIA_URL — это URL, по которому будут доступны медиафайлы
    # document_root=settings.MEDIA_ROOT указывает на физическое расположение медиафайлов на диске сервера
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from blog.urls import main_path
from . import views

urlpatterns = [
    main_path,
    path('about/', views.about_view, name = 'about-view'),
    path('blog/', include('blog.urls')),
    path('users/', include('users.urls')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

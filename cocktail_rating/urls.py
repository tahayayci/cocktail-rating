from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView

from drunk import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomeView.as_view(), name='home'),
    path('search', views.search, name='home-search'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html', redirect_authenticated_user=True), name='login'),  
    path('logout/', views.logout_view, name='logout'),
    path('cocktails/', include('drunk.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

"""
URL configuration for construction_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from builder import views 

# ... (matha imports) ...

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_page, name='home'),
    path('materials/', views.materials_page, name='materials'),
    path('add-home/', views.add_home, name='add_home'), # Intha line add pannunga
    path('add-home/', views.add_home, name='add_home'),
    
    # Intha rendu line-a pudhusa add pannunga:
    path('view-homes/', views.view_homes, name='view_homes'),
    path('update-home/<int:id>/', views.update_home, name='update_home'), # URL-la ID pass panrom
    path('add-material/<int:id>/', views.add_material_to_home, name='add_material'),
    path('generate-bill/<int:id>/', views.generate_bill, name='generate_bill'),
    path('register/', views.register_page, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('search/', views.search_materials, name='search_materials'),
    path('mark-finished/<int:id>/', views.mark_as_finished, name='mark_finished'),
]

# ... (media settings) ...

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
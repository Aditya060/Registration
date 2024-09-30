"""
URL configuration for Registration project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from core import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.register, name = 'register'),
    path('success/<str:unique_id>/', views.success, name='success'),
    path('verify/', views.verify_qr_code, name='verify_qr_code'),

    # path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    
    path('scan_qr/', views.qr_scanner_view, name='scan_qr'),

    path('print-badge/<str:unique_id>/', views.print_badge, name='print_badge'),
    
    
    # path('verify/<uuid:unique_id>/', views.verify_qr_code, name='verify_qr_code'),


]
urlpatterns += staticfiles_urlpatterns()

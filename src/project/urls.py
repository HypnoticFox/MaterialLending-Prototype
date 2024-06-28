"""
URL configuration for the project.

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
import os
from django.contrib import admin
from django.urls import include, path
from allauth.account.decorators import secure_admin_login
from allauth.account.views import logout as allauth_logout
from project.utils.decorators import decorator_include, group_required
from . import views

admin.autodiscover()
admin.site.login = secure_admin_login(admin.site.login)
admin.site.logout = allauth_logout

urlpatterns = [
    path("products/", decorator_include(group_required("example"), "products.urls")),
    path('accounts/', include('allauth.urls')),
    path(os.getenv("DJANO_ADMIN_PATH") or "admin/", admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
    path("cloudinary-upload-sign/", views.generate_cloudinary_upload_signature, name="cloudinary-upload-signature"),
    path("health-check/", views.health_check, name="health-check"),
    path("", include("home.urls")),
]

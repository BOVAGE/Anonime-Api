"""anonime URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.conf.urls import handler404, handler500, handler400

schema_view = get_schema_view(
   openapi.Info(
      title="Anonime API",
      default_version='v1',
      description="A RSESTful API for an anonymous messaging service.",
      terms_of_service="https://www.anonime.xyz/policies/terms/",
      contact=openapi.Contact(email="contact@anonime.xyz"),
      license=openapi.License(name="Apache-2.0 license"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('',include('message.urls')),
]

handler404 ='common.errors.not_found'
handler400 ='rest_framework.exceptions.bad_request'
handler500 = 'rest_framework.exceptions.server_error'
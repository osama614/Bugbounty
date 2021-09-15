"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls
#from rest_framework.schemas import get_schema_view
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.schemas.openapi import SchemaGenerator

generator = SchemaGenerator

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('bcd729e42e8e00d78fbe8aee7fb9908b/', admin.site.urls),
    path('api/v1/auth/', include('users.urls',namespace='users')),
    path('api/v1/ads/', include('ads.urls',namespace='ads')),
    path('api/v1/hackers/', include('hackers.urls',namespace='hackers')),
    path('api/v1/programs/', include('programs.urls',namespace='programs')),
    #url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   # path('swagger/', schema_view.with_ui('swagger'), name='schema-swagger-ui'),
   # path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/v2/auth/', include('djoser.urls')),
    # path('docs/', include_docs_urls(title="Hacking Technology")),
    # path('docs2/', get_schema_view(
    #     title="Hacking Technology",
    #     description="API for all things …",
    #     version="1.0.0",
    #     generator_class=generator
    # ), name='openapi-schema'),
]

#if settings.DEBUG:
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

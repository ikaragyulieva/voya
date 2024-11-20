"""
URL configuration for voya project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.shortcuts import render
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('voya.common.urls')),
    path('clients/', include('voya.clients.urls')),
    path('companies/', include('voya.companies.urls')),
    path('employees/', include('voya.employees.urls')),
    path('request/', include('voya.requests.urls')),
    path('services/', include('voya.services.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


def custom_404(request, exception):
    return render(request, '500.html', {
        'previous_page': request.META.get('HTTP_REFERER', '/'),  # Default to '/' if no referrer
    }, status=404)


handler404 = 'voya.urls.custom_404'

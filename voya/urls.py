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
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin

from django.shortcuts import render
from django.urls import path, include
from django.views.i18n import set_language
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework.routers import DefaultRouter

from voya.proposals import views
from voya.proposals.api.views import ProposalViewSet

router = DefaultRouter()
router.register(r'proposals', ProposalViewSet, basename='proposal')


urlpatterns = [
    path('admin/', admin.site.urls),

    # API URLs
    path('api/proposals/', include('voya.proposals.api.api_urls')),

    # API Routes
    path('api/', include(router.urls)),

    # path('', include('voya.common.urls')),
    # path('clients/', include('voya.clients.urls')),
    # path('companies/', include('voya.companies.urls')),
    # path('employees/', include('voya.employees.urls')),
    # path('request/', include('voya.requests.urls')),
    # path('services/', include('voya.services.urls')),
    # path('proposals/', include('voya.proposals.urls')),
    # path('providers/', include('voya.providers.urls')),

    # Swagger URLs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # UI:
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # Language Switching
    path('i18n/', include('django.conf.urls.i18n')),
    path('i18n/setlang/', set_language, name='set_language'),
]

# Translatable URLs (frontend)
urlpatterns += i18n_patterns(
    path('', include('voya.common.urls')),
    path('clients/', include('voya.clients.urls')),
    path('companies/', include('voya.companies.urls')),
    path('employees/', include('voya.employees.urls')),
    path('request/', include('voya.requests.urls')),
    path('services/', include('voya.services.urls')),
    path('proposals/', include('voya.proposals.urls')),
    path('providers/', include('voya.providers.urls')),

    prefix_default_language=True  # Skips "/en" for default language
)

# Serve media files in dev
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# Custom Error handler
def custom_404(request, exception):
    return render(request, '500.html', {
        'previous_page': request.META.get('HTTP_REFERER', '/'),  # Default to '/' if no referrer
    }, status=404)


handler404 = 'voya.urls.custom_404'

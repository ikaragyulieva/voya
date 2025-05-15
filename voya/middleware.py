"""
Copyright (C) 2025 DROMO SA

This file is part of VOYA.

VOYA is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

[Project Name] is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
"""
import re

from django.http import HttpResponseRedirect
from django.urls import is_valid_path
from django.utils import translation

from django.conf import settings
from django.utils.deprecation import MiddlewareMixin


class UserLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.supported_languages = dict(settings.LANGUAGES).keys()

    def __call__(self, request):

        # # user_type = user.role

        path = request.path_info

        # Extract language from the path if present
        language_from_path = self.get_language_from_path(path)

        if language_from_path in self.supported_languages:
            language = language_from_path
        else:

            language = request.session.get('django_language') or settings.LANGUAGE_CODE
            user = getattr(request, 'user', None)
            if user and user.is_authenticated:
                profile = getattr(user, 'employee_profile', None)

                if profile and hasattr(profile,
                                       'preferred_language') and profile.preferred_language in self.supported_languages:
                    language = profile.preferred_language

                    # Redirect only if not already prefixed
            if not path.startswith(f"/{language}/") and self.should_redirect(path):
                return HttpResponseRedirect(f"/{language}{path}")
        #         # Avoid redirects for ignored paths
        #         ignore_prefixes = [
        #             '/api/',
        #             '/admin/',
        #             '/static/',
        #             '/media/',
        #             '/i18n/',
        #         ]
        #
        #         if not any(path_info.startswith(prefix) for prefix in ignore_prefixes):
        #             return HttpResponseRedirect(f"/{language}{path_info}")

        translation.activate(language)
        request.LANGUAGE_CODE = language

        # # Redirection logic
        # path_info = request.path_info
        # language_prefix = f"/{language}/"
        # default_language = settings.LANGUAGE_CODE
        #
        #
        #
        #
        #
        # # Do not redirect if language is default anf prefix_default _language=False
        # if (
        #         not path_info.startswith(language_prefix)
        #         and is_valid_path(path_info, urlconf=settings.ROOT_URLCONF)
        # ):
        #     return HttpResponseRedirect(f"/{language}{path_info}")

        response = self.get_response(request)
        translation.deactivate()

        return response

    def get_language_from_path(self, path):
        match = re.match(r"^/([a-zA-Z]{2})/", path)
        if match:
            return match.group(1)

        return None

    def should_redirect(self, path):
        ignore_prefixes = [
            '/api/',
            '/admin/',
            '/static/',
            '/media/',
            '/i18n/',
        ]
        return not any(path.startswith(prefix) for prefix in ignore_prefixes)

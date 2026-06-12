import logging

from django.conf import settings
from django.shortcuts import redirect
from django.http import HttpResponseForbidden
from django.template.loader import render_to_string

logger = logging.getLogger('home.middleware')

class LoginRequiredMiddleware:
    """
    Centralised authentication and role-based access-control middleware.

    Roles are defined via Django groups:
      - administrator : is_superuser=True or is_staff=True  (full access)
      - reviewer : 'reviewer' group  (all views, including write views)
      - guest : 'guest' group  (read-only views only)
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.public_paths  = getattr(settings, 'LOGIN_NOT_REQUIRED_PATHS', [])
        self.editor_paths  = getattr(settings, 'EDITOR_REQUIRED_PATHS', [])

    def __call__(self, request):
        path = request.path_info

        # Always-public paths (login, logout, static …)
        if any(path.startswith(p) for p in self.public_paths):
            return self.get_response(request)

        # Unauthenticated user → redirect to login
        if not request.user.is_authenticated:
            return redirect(f"{settings.LOGIN_URL}?next={path}")

        # Path restricted to Editor/Administrator
        if any(path.startswith(p) for p in self.editor_paths):
            if not self._is_editor_or_admin(request.user):
                ip = (request.META.get('HTTP_X_FORWARDED_FOR', '')
                      .split(',')[0].strip()
                      or request.META.get('REMOTE_ADDR', 'unknown'))
                role = (request.user.groups.values_list('name', flat=True)
                        .first() or 'no group')
                logger.warning(
                    "ACCESS DENIED | user=%s | role=%s | method=%s | path=%s | ip=%s",
                    request.user.username, role,
                    request.method, path, ip,
                )
                html = render_to_string(
                    '403.html',
                    {'user': request.user,
                     'required_role': 'Editor or Administrator'},
                    request=request,
                )
                return HttpResponseForbidden(html)

        return self.get_response(request)

    @staticmethod
    def _is_editor_or_admin(user):
        if user.is_superuser or user.is_staff:
            return True
        return user.groups.filter(name__in=['administrator', 'reviewer']).exists()
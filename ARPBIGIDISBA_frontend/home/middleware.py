from django.conf import settings
from django.shortcuts import redirect
from django.http import HttpResponseForbidden
from django.template.loader import render_to_string


class LoginRequiredMiddleware:
    """
    Middleware centralizado de autenticación y control de acceso por rol.

    Roles definidos mediante grupos Django:
      - administrator : is_superuser=True o is_staff=True  (acceso total)
      - reviewer        : grupo 'reviewer'  (todas las vistas, incluidas las de escritura)
      - guest      : grupo 'guest' (solo vistas de consulta)
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.public_paths  = getattr(settings, 'LOGIN_NOT_REQUIRED_PATHS', [])
        self.editor_paths  = getattr(settings, 'EDITOR_REQUIRED_PATHS', [])

    def __call__(self, request):
        path = request.path_info

        # 1. Rutas siempre públicas (login, logout, static…)
        if any(path.startswith(p) for p in self.public_paths):
            return self.get_response(request)

        # 2. Usuario no autenticado → redirigir a login
        if not request.user.is_authenticated:
            return redirect(f"{settings.LOGIN_URL}?next={path}")

        # 3. Ruta restringida a Editor/Administrador
        if any(path.startswith(p) for p in self.editor_paths):
            if not self._is_editor_or_admin(request.user):
                html = render_to_string(
                    '403.html',
                    {'user': request.user,
                     'required_role': 'reviewer or administraTor'},
                    request=request,
                )
                return HttpResponseForbidden(html)

        return self.get_response(request)

    @staticmethod
    def _is_editor_or_admin(user):
        if user.is_superuser or user.is_staff:
            return True
        return user.groups.filter(name__in=['administrator', 'reviewer']).exists()
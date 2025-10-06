from django.shortcuts import redirect
from django.conf import settings
from django.urls import resolve, reverse

class LoginRequiredMiddleware:
    """
    Middleware forcing to login at all the views except those explicitly allowed.
    """

    def __init__(self, get_response):
        self.get_response = get_response

        # Rutas que siempre se permiten sin login
        self.allowed_names = getattr(settings, 'LOGIN_NOT_REQUIRED_URLNAMES', [])
        self.allowed_paths = getattr(settings, 'LOGIN_NOT_REQUIRED_PATHS', [])

    def __call__(self, request):
        # Obtener el nombre de la vista actual (si está definido)
        resolver_match = resolve(request.path)
        view_name = resolver_match.url_name

        # Permitir acceso si la ruta o el nombre de la vista está en la lista blanca
        if view_name in self.allowed_names or request.path in self.allowed_paths:
            return self.get_response(request)

        # Si el usuario no está autenticado, redirigir a login
        if not request.user.is_authenticated:
            login_url = getattr(settings, 'LOGIN_URL', '/accounts/login/')
            return redirect(f'{login_url}?next={request.path}')

        return self.get_response(request)
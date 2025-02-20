from django.contrib.admin import AdminSite


class CustomAdminSite(AdminSite):
    def get_app_list(self, request, app_label=None):
        # Obtiene la lista de aplicaciones del Admin normal
        app_list = super().get_app_list(request, app_label)

        # Filtra la app que quieres ocultar
        app_list = [app for app in app_list if app["app_label"] != "dashboard"]

# Instancia personalizada del Admin
custom_admin_site = CustomAdminSite(name="custom_admin")
from django.contrib.admin import AdminSite


class CustomAdminSite(AdminSite):
    def get_app_list(self, request, app_label=None):
        # Get the app list from the default admin site
        app_list = super().get_app_list(request, app_label)

        # Filter out the app to hide
        app_list = [app for app in app_list if app["app_label"] != "dashboard"]

# Custom admin site instance
custom_admin_site = CustomAdminSite(name="custom_admin")
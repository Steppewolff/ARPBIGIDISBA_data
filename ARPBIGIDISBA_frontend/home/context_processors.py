def user_role(request):
    """
    Adds 'user_role' to the context of all templates.
    Valores posibles: 'administrator', 'reviewer', 'guest', 'user_nogroup', None
    """
    if not request.user.is_authenticated:
        return {'user_role': None}

    user = request.user
    if user.is_superuser or user.is_staff:
        role = 'administrator'
    elif user.groups.filter(name='reviewer').exists():
        role = 'reviewer'
    elif user.groups.filter(name='guest').exists():
        role = 'guest'
    else:
        role = 'user_nogroup'          # authenticated but not assigned to any group

    return {'user_role': role}
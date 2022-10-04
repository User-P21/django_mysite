from django.shortcuts import redirect
from django.contrib import messages



#### do not view the login and registration pages if i am logged in ####
def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dent:home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


def allowed_users(allowed_roles = []):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                messages.info(request, 'You are not authorized to see that page')
                return redirect('dent:home')
        return wrapper_func
    return decorator

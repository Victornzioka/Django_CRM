from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwags):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwags)

    return wrapper_func

#this function acts as a decorator to only allow specific groups of people access certain functionalities
def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not allowed to access this page')

        return wrapper_func

    return decorator

#this function acts as a decorator to only allow specific groups of people access admin functionalities
def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):

        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'customer':
            return redirect('user-page')
        if group == 'admin':
            return view_func(request, *args, **kwargs)

    return wrapper_func

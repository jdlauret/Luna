from django.shortcuts import redirect

def auth_allowed(backend, details, response, *args, **kwargs):
    if not backend.auth_allower(response, details):
        return redirect('user:error')
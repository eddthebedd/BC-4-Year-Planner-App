from functools import wraps
from django.http import HttpResponseForbidden

def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.profile.is_admin:
            return HttpResponseForbidden()
        return view_func(request, *args, **kwargs)
    return _wrapped_view
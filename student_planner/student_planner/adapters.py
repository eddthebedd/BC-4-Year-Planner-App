from allauth.account.adapter import DefaultAccountAdapter
from django.urls import reverse

class CustomAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        if not request.user.registered:
            return '/role-form'
        else:
            if request.user.role == 'STUDENT':
                return reverse('/student')
            elif request.user.role == 'ADVISOR':
                return reverse('/advisor')
      
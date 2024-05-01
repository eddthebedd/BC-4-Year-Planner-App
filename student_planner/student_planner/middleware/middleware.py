from django.shortcuts import redirect

class LoginRedirectMiddleware:
    def _init_(self, get_response):
        self.get_response = get_response

    def _call_(self, request):

        # Code that is executed in each request before the view is called

        response = self.get_response(request)

        # Code that is executed in each request after the view is called
        return response

    
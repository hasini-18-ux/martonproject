from django.urls import reverse
from django.shortcuts import redirect

class RedirectAuthenticatedUserMiddleWare:
    def __init__(self,get_response):
        self.get_response=get_response
    def __call__(self,request):
        #check user is authenticated
        if request.user.is_authenticated:
            #Lists which of the paths user have
            paths_to_redirect=[reverse('amazon:login'),reverse('amazon:register')]
            if request.path in paths_to_redirect:
                return redirect(reverse('amazon:index'))  #change to homepage
        response=self.get_response(request)
        return response

class RestrictUnauthenticatedUserMiddleWare:
    def __init__(self,get_response):
        self.get_response=get_response
    def __call__(self,request):
        if not request.user.is_authenticated:
            restricted_paths=[reverse('amazon:fashionhub')]
            if request.path in restricted_paths:
                return redirect(reverse('amazon:login'))
        response=self.get_response(request)
        return response
        
import re
from django.shortcuts import redirect
from django.urls import reverse


class Middleware:
    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        urllists = ['/myadmin/login','/myadmin/dologin','/myadmin/logout']
        if re.match(r'^/myadmin',path) and (path not in urllists):
            if 'adminuser' not in request.session:
                return redirect(reverse("myadmin_login"))
        response = self.get_response(request)
        return response
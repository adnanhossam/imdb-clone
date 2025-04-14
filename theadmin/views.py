from django.shortcuts import render
from django.http import HttpRequest , HttpResponse
from django.views import View
# Create your views here.


def h_world_view(HttpRequest):
    return HttpResponse('Hello, world')

class HomeView(View):
    def get(self, request):
        return render(template_name='home.html',request=request)
    
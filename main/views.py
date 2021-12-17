
from django.views.generic import TemplateView
from django.shortcuts import render

# class HomeView(TemplateView):
#     template_name = "templates/home.html"

def HomeView(request):
    current_user = request.user
    context = {'username': current_user.username,
               'current_user': current_user}
    return render(request, 'templates/home.html', context)


    
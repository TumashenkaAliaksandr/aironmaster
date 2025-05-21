from django.shortcuts import render


def index(request):
    return render(request, 'webapp/index.html')


def services(request):
    return render(request, 'webapp/services.html')

def single_services(request):
    return render(request, 'webapp/single_services.html')

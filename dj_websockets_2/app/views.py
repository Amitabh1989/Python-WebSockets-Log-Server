from django.shortcuts import render


# Create your views here.
def index(request):
    context = {"title": "Welcome to my website"}
    return render(request, "index.html", context)

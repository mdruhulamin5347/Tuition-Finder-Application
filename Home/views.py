from django.shortcuts import render

# Create your views here.
def HOME(request):
    return render(request,'home/home.html')
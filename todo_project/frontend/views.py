from django.shortcuts import render

# Create your views here.
def list(request):
    return render(request,'list.html')

def signup(request):
    return render(request,'Signup.html')

def login(request):
    return render(request,'login.html')
from django.shortcuts import render

# Create your views here.
def testbase(request):
    return render(request, 'base.html')
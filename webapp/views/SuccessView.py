from django.shortcuts import render

def success_view(request):
    return render(request, 'success_page.html')

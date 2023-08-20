from django.shortcuts import render

def success_view(request):
    return render(request, 'utility_pages/success_page.html')

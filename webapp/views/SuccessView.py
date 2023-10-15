from django.shortcuts import render


def success_view(request):
    return render(request, 'utility_pages/success_page.html')


def update_success_view(request):
    return render(request, 'utility_pages/update_success_page.html')


def item_success_view(request):
    return render(request, 'utility_pages/item_success_page.html')

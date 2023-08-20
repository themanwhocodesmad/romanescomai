# views.py
from django.shortcuts import render, redirect

from webapp.forms.ResourcesForms import ProductForm, ErrorCodeForm, RegionForm, VendorForm


# views.py


def add_region(request):
    if request.method == "POST":
        form = RegionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_page')  # replace with actual success url name
    else:
        form = RegionForm()
    return render(request, 'functionality/add_region.html', {'form': form})


def add_vendor(request):
    if request.method == "POST":
        form = VendorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_page')  # replace with actual success url name
    else:
        form = VendorForm()
    return render(request, 'functionality/add_vendor.html', {'form': form})


def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_page')  # replace with actual success url name
    else:
        form = ProductForm()
    return render(request, 'functionality/add_product.html', {'form': form})


def add_error_code(request):
    if request.method == "POST":
        form = ErrorCodeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_page')  # replace with actual success url name
    else:
        form = ErrorCodeForm()
    return render(request, 'functionality/add_error_code.html', {'form': form})

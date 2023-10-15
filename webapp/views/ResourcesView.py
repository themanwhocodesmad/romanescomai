# views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from webapp.forms.ResourcesForms import ProductForm, ErrorCodeForm, RegionForm, VendorForm
from webapp.permissions import role_required


# views.py

@login_required
@role_required('Technical Admin')
def add_region(request):
    if request.method == "POST":
        form = RegionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('item_success_page')  # replace with actual success url name
    else:
        form = RegionForm()
    return render(request, 'functionality/add_region.html', {'form': form})


@login_required
@role_required('Technical Admin')
def add_vendor(request):
    if request.method == "POST":
        form = VendorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('item_success_page')  # replace with actual success url name
    else:
        form = VendorForm()
    return render(request, 'functionality/add_vendor.html', {'form': form})


@login_required
@role_required('Technical Admin')
def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('item_success_page')  # replace with actual success url name
    else:
        form = ProductForm()
    return render(request, 'functionality/add_product.html', {'form': form})


@login_required
@role_required('Technical Admin')
def add_error_code(request):
    if request.method == "POST":
        form = ErrorCodeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('item_success_page')  # replace with actual success url name
    else:
        form = ErrorCodeForm()
    return render(request, 'functionality/add_error_code.html', {'form': form})

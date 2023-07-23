# views.py
from datetime import datetime

from django.forms import model_to_dict
from django.shortcuts import render, redirect

from rma.models import RMA
from webapp.forms import ConvertRMAForm, RMAForm


def convert_rma(request, rma_id):
    rma = RMA.objects.get(id=rma_id)
    if request.method == 'POST':
        form = ConvertRMAForm(request.POST, instance=rma)

        if form.is_valid():
            # Update RMA object if received_at_warehouse and convert_to_jobcard fields are checked
            if form.cleaned_data['received_at_warehouse']:
                rma.received_at_warehouse = True

            if form.cleaned_data['convert_to_jobcard']:
                rma.converted_or_closed = True
                rma.save()
                job_card = rma.create_job_card()

                # Update technician and assigned_date fields for the created job card
                job_card.assigned_technician = form.cleaned_data['technician']
                job_card.assigned_date = datetime.now()
                job_card.save()

            return redirect('open_rmas')
    else:
        form = ConvertRMAForm(instance=rma)

    return render(request, 'convert_rma.html', {'form': form, 'rma': rma})


# views.py

from django.shortcuts import render, redirect


# views.py

def open_rmas(request):
    rm_as = RMA.objects.filter(converted_or_closed=False)
    context = {'rm_as': rm_as}
    return render(request, 'open_rmas.html', context)


# views.py

def edit_rma(request, rma_id):
    rma = RMA.objects.get(id=rma_id)
    if request.method == 'POST':
        # Create a copy of the current RMA instance's data
        rma_data = model_to_dict(rma)
        # Update this data with the POST data (partial update)
        rma_data.update(request.POST.dict())

        # Pass the updated data to the form
        form = RMAForm(rma_data, instance=rma)

        if form.is_valid():
            form.save()
            return redirect('open_rmas')
    else:
        form = RMAForm(instance=rma)

    return render(request, 'edit_rma.html', {'form': form})


def add_rma(request):
    if request.method == "POST":
        form = RMAForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_page')  # replace with the actual success URL name
    else:
        form = RMAForm()
    return render(request, 'add_rma.html', {'form': form})

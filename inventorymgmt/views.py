from django.shortcuts import render, redirect

from inventorymgmt.forms import InventoryCreateForm, InventorySearchForm, InventoryUpdateForm
from .models import *

from django.http import HttpResponse
import csv

from django.contrib import messages

from .forms import IssueForm, ReceiveForm

# Create your views here.


def home(request):
	title = 'Welcome: This is the Home Page'
	context = {
	"title": title,
	}
	return render(request, "home.html",context)


def list_items(request):
    title = 'List of all items'
    form = InventorySearchForm(request.POST or None)
    queryset = Inventory.objects.all
    context = {
    "title": title,
    "form": form,
    "queryset": queryset,

    }
    if request.method == 'POST':
        queryset = Inventory.objects.filter(#category__icontains=form['category'].value(),
									item_name__icontains=form['item_name'].value()
									)
        if form['export_to_CSV'].value() == True:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="List of inventory.csv"'
            writer = csv.writer(response)
            writer.writerow(['CATEGORY', 'ITEM NAME', 'QUANTITY'])
            instance = queryset
            for inventory in instance:
                writer.writerow([inventory.category, inventory.item_name, inventory.quantity])
            return response
        context = {
	    "form": form,
	    "queryset": queryset,
    }
    return render(request, "list_items.html",context)

def add_items(request):
    form = InventoryCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Successfully Saved')
        return redirect('/list_items')
    context = {
        "form": form,
        "title": "Add Item",
    }
    return render(request, "add_items.html", context)



def update_items(request, pk):
    queryset = Inventory.objects.get(id=pk)
    form = InventoryUpdateForm(instance=queryset)
    if request.method == 'POST':
        form = InventoryUpdateForm(request.POST, instance=queryset)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully Updated')
            return redirect('/list_items')

    context = {
		'form':form
	}
    return render(request, 'add_items.html', context)



def delete_items(request, pk):
    queryset = Inventory.objects.get(id=pk)
    if request.method == 'POST':
        queryset.delete()
        messages.success(request, 'Successfully Deleted')
        return redirect('/list_items')
    return render(request, 'delete_items.html')


def inventory_details(request, pk):
	queryset = Inventory.objects.get(id=pk)
	context = {
		"title": queryset.item_name,
		"queryset": queryset,
	}
	return render(request, "inventory_details.html", context)



def issue_items(request, pk):
	queryset = Inventory.objects.get(id=pk)
	form = IssueForm(request.POST or None, instance=queryset)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.quantity -= instance.issue_quantity
		instance.issue_by = str(request.user)
		messages.success(request, "Issued SUCCESSFULLY. " + str(instance.quantity) + " " + str(instance.item_name) + "s now left in Store")
		instance.save()

		return redirect('/inventory_details/'+str(instance.id))
		# return HttpResponseRedirect(instance.get_absolute_url())

	context = {
		"title": 'Issue ' + str(queryset.item_name),
		"queryset": queryset,
		"form": form,
		"username": 'Issue By: ' + str(request.user),
	}
	return render(request, "add_items.html", context)



def receive_items(request, pk):
	queryset = Inventory.objects.get(id=pk)
	form = ReceiveForm(request.POST or None, instance=queryset)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.quantity += instance.receive_quantity
		instance.save()
		messages.success(request, "Received SUCCESSFULLY. " + str(instance.quantity) + " " + str(instance.item_name)+"s now in Store")

		return redirect('/inventory_details/'+str(instance.id))
		# return HttpResponseRedirect(instance.get_absolute_url())
	context = {
			"title": 'Reaceive ' + str(queryset.item_name),
			"instance": queryset,
			"form": form,
			"username": 'Receive By: ' + str(request.user),
		}
	return render(request, "add_items.html", context)
















#myusername
#Dheeraj@3211




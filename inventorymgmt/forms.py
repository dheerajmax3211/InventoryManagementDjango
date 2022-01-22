from django import forms
from .models import Inventory



class InventoryCreateForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['category', 'item_name', 'quantity']

    def clean_category(self):
        category = self.cleaned_data.get('category')
        if not category:
            raise forms.ValidationError('Category is must')
        for instance in Inventory.objects.all():
            if instance.category == category:
                raise forms.ValidationError(str(category) + ' is already created')
		
        return category



    def clean_item_name(self):
        item_name = self.cleaned_data.get('item_name')
        if not item_name:
            raise forms.ValidationError('This field is required')
        return item_name


class InventorySearchForm(forms.ModelForm):
    export_to_CSV = forms.BooleanField(required="False")

    class Meta:
     model = Inventory
     fields = ['category', 'item_name']


class InventoryUpdateForm(forms.ModelForm):
	class Meta:
		model = Inventory
		fields = ['category', 'item_name', 'quantity']



class IssueForm(forms.ModelForm):
	class Meta:
		model = Inventory
		fields = ['issue_quantity', 'issue_to']


class ReceiveForm(forms.ModelForm):
	class Meta:
		model = Inventory
		fields = ['receive_quantity', 'receive_by']
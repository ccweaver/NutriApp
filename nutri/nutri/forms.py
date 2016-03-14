from django import forms
from ingred_table.models import Ingredient
from Restaurant.models import Restaurant

class NutriForm(forms.Form):

	units = (('g','g'),('oz','oz'),('mL','mL'),('tsp','tsp'),('tblspn','tblspn'))

	ingredient = forms.ModelMultipleChoiceField(queryset=Ingredient.objects.filter(ingredient__icontains='stea'))
	amount = forms.DecimalField(max_digits=7, decimal_places=2, min_value=(0))
	unit = forms.ChoiceField(choices=units)

class UserForm(forms.Form):
	hoods = (('None','None'),('Allston','Allston'))
	
	email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': ' Email', 'style': 'width:99%'}))
	email2 = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': ' Re-enter Email', 'style': 'width:99%'}))
	password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'placeholder': ' Password', 'style':'width:99%'}))
	restaurant = forms.BooleanField(required=False)
	neighborhood = forms.ChoiceField(choices=hoods)

	def clean(self):
		email = self.cleaned_data.get('email')
		email2 = self.cleaned_data.get('email2')
		neighborhood = self.cleaned_data.get('neighborhood')
		restaurant = self.cleaned_data.get('restaurant')
		if email != email2:
			raise forms.ValidationError("Email Addresses don't match")
		return self.cleaned_data



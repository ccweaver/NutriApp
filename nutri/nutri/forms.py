from django import forms
from ingred_table.models import Ingredient

class NutriForm(forms.Form):

	units = (('g','g'),('oz','oz'),('mL','mL'),('tsp','tsp'),('tblspn','tblspn'))

	ingredient = forms.ModelMultipleChoiceField(queryset=Ingredient.objects.filter(ingredient__icontains='stea'))
	amount = forms.DecimalField(max_digits=7, decimal_places=2, min_value=(0))
	unit = forms.ChoiceField(choices=units)
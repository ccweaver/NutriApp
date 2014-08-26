from django import forms

class NutriForm(forms.Form):
	ingreds = (('Tomatoes','Tomatoes'),('Potatoes','Potatoes'),)
	units = (('g','g'),('oz','oz'),('mL','mL'),('tsp','tsp'),('tblspn','tblspn'))

	ingredient = forms.ChoiceField(choices=ingreds)
	amount = forms.DecimalField(max_digits=7, decimal_places=2, min_value=(0))
	unit = forms.ChoiceField(choices=units)
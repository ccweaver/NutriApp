from django.http import HttpResponse
from django import forms
from nutri.forms import NutriForm
from django.shortcuts import render
from ingred_table.models import Ingredient

def ingredient(request):
	ingred_list = []
	error = ""
	#['jelly beans,RAW(of course)', 'barnacles']
	if request.method == 'POST':
		print request.POST
		if 'term' in request.POST:
			print request.POST['term']
			terms = request.POST['term'].split(' ')

			if len(terms) == 1:
				ingred_list = Ingredient.objects.filter(ingredient__icontains=request.POST['term'])
			if len(terms) == 2:
				ingred_list = Ingredient.objects.filter(ingredient__icontains=terms[0]).filter(ingredient__icontains=terms[1])
			if len(terms) == 3:
				ingred_list = Ingredient.objects.filter(ingredient__icontains=terms[0]).filter(ingredient__icontains=terms[1]).filter(ingredient__icontains=terms[2])
			if len(terms) == 4:
				ingred_list = Ingredient.objects.filter(ingredient__icontains=terms[0]).filter(ingredient__icontains=terms[1]).filter(ingredient__icontains=terms[2]).filter(ingredient__icontains=terms[3])


			if not ingred_list:
				ingred_list = ['Sorry, no ingredient found']
			if not request.POST['term']:
				ingred_list = []
			
			#count = 10
			#for x in range(0,count):
			#	print ingred_list[x].id

		if 'amount' in request.POST:
			if 'ingred_to_add' not in request.POST:
				error = 'Please search for and select an ingredient'
			else:
				ingred_to_add = request.POST['ingred_to_add']
			amount = request.POST['amount']
			unit = request.POST['unit']

			if not error and not amount:
				error = 'Please input an amount'
			if error:
				print 'major error'
				return render(request, 'nutri_form.html', {'ingred_list':ingred_list, 'error':error})


		return render(request, 'select_temp.html', {'ingred_list':ingred_list, 'error':error})
	else:
		return render(request, 'nutri_form.html', {'ingred_list':ingred_list, 'error':error})

def add_restaurant(request):
	return render(request, 'add_rest.html')
	
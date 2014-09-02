from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from nutri.forms import NutriForm
from django.shortcuts import render
from ingred_table.models import Ingredient
from Restaurant.models import Restaurant
import re

def sign_in(request):
	if request.method == 'POST':
		print request.POST
	return render(request, 'sign_in.html')

def ingredient(request):

	ingred_list = []
	d_name = "chicken parm"
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
			return render(request, 'select_temp.html', {'ingred_list':ingred_list, 'error':error, 'd_name':d_name})
		
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
				return render(request, 'nutri_form.html', {'ingred_list':ingred_list, 'error':error, 'd_name':d_name})

		if 'dish_name' in request.POST:
			d_name = request.POST['dish_name']
			print d_name


	return render(request, 'nutri_form.html', {'ingred_list':ingred_list, 'error':error, 'd_name':d_name})

def add_restaurant(request):
	error = ""
	rest_name = ""
	num_street = ""
	city = ""
	state = "--"
	zipcode = ""
	if request.method == 'POST':
		rest_name = request.POST['rest_name']
		if not rest_name:
			error = 'Please enter the name of your restaurant'

		num_street = request.POST['num_street']

		nsSplit = num_street.split(' ')
		num = nsSplit[0]
		try:
			int(num)
		except ValueError:
			if not error:
				error = 'Please enter a street number and street name'

		street = ""
		for x in range (1, len(nsSplit)):
			street = street + nsSplit[x]

		city = request.POST['city']
		if not city and not error:
			error = 'Please enter a city'
		
		state = request.POST['state']
		if state == '--' and not error:
			error = 'Please select a state'

		zipcode = request.POST['zipcode']
		zRE = re.compile("^[0-9][0-9][0-9][0-9][0-9]$")
		if not zRE.match(zipcode) and not error:
			error = 'Please enter a valid 5 digit zip code'

		if not error:
			r = Restaurant(name=rest_name, number=num, street=street, city=city, state=state, zipcode=zipcode)
			r.save()
			return HttpResponseRedirect('/restaurant_profile')


	return render(request, 'add_rest.html', {'error':error, 'rest_name':rest_name, 'num_street':num_street, 'city':city, 'state':state, 'zipcode':zipcode})
	
def restaurant_profile(request):

	return render(request, 'rest_profile.html')


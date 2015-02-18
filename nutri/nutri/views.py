from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from nutri.forms import UserForm
from django.shortcuts import render
from ingred_table.models import Ingredient
from Restaurant.models import Restaurant
from menu_items.models import Item
from added_ingreds.models import Addition
import re, json
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib import auth

    
def sign_in(request):
    invalid = ""
    error = ""
    uform = UserForm
    is_user = False
    if request.user.username != '':
        is_user = True

    print request.user
    print is_user

    if request.method == 'POST':
        print request.POST
        if 'login_email' in request.POST:
            login_email = request.POST['login_email']
            login_pass = request.POST['login_pass']
            user = auth.authenticate(username=login_email, password=login_pass)
            print 'hi'
            if user is not None:
                auth.login(request, user)
                data = {'success':'true'}
            else:
                data = {'success':'false'}

            return HttpResponse(json.dumps(data), content_type = "application/json")
            
        if 'logout' in request.POST:
            logout(request)
            is_user = False
            data = {'success':'true'}
            return HttpResponse(json.dumps(data), content_type = "application/json")

        if 'proflink' in request.POST:
            rest_id = Restaurant.objects.filter(user=request.user.id)

            if len(rest_id) > 0:
                print 'mallows'
                address = '/restaurant_profile/' + str(rest_id[0])
            else:
                address = "/add_restaurant"
            
            data = {'success':'true', 'href':address}

            return HttpResponse(json.dumps(data), content_type = "application/json")                    
                
                

        if 'first_name' in request.POST:
            uform = UserForm(request.POST)
            

            if uform.is_valid():
                print 'valid form'
                cd = uform.cleaned_data
                fname = cd['first_name']
                lname = cd['last_name']
                email = cd['email']
                email2 = cd['email2']                       
                password = cd['password']
                print fname, lname, email, email2, password
                if User.objects.filter(username=email):
                    error = 'This email address is already in use'
                    return render(request, 'sign_in.html', {'form':uform, 'invalid':invalid, 'error':error})
                user = User.objects.create_user(email, email, password)
                user.first_name = fname
                user.last_name = lname
                user.save()

                print 'xxx'
                user = auth.authenticate(username=email, password=password)
                auth.login(request, user)
                print '&*('
                return HttpResponseRedirect('/add_restaurant')
            
            else:
                ere = re.compile("^.+@.+\..+$")

                invalid = 'true'
                print 'invalid form'
                if not request.POST['first_name']:
                    error = 'Please enter a first name'
                elif not request.POST['last_name']:
                    error = 'Please enter a last name'              
                elif not ere.match(request.POST['email']):
                    error = 'Please enter a valid email address'
                elif request.POST['email2'] != request.POST['email']:
                    error = "Email addresses don't match"
                elif not request.POST['password']:
                    error = 'Please enter a password'

    return render(request, 'sign_in.html', {'form':uform, 'invalid':invalid, 'error':error, 'is_user':is_user, 'user':request.user.username})


def dish(request, rid):
    ingred_list = []
    error = ""
    add_i = {}
    #['jelly beans,RAW(of course)', 'barnacles']
    if not Restaurant.objects.filter(id=rid):
        return HTTPResponseNotFound
    if request.method == 'POST':
        print request.POST
        if 'done' in request.POST:
            print '******'
            print request.POST['ingred_dish']
            print '****'
            dish = Item.objects.filter(rest_id=rid).filter(name=request.POST['ingred_dish'])[0]
            dish.valid = True;
            dish.save()
            data = {'rid':rid}
            return HttpResponse(json.dumps(data), content_type="application/json")
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
            #   print ingred_list[x].id
            return render(request, 'select_temp.html', {'ingred_list':ingred_list, 'error':error, 'added_ingreds':add_i})
        
        if 'amount' in request.POST:
            ingred_to_add = request.POST['ingred_to_add']
            amount = request.POST['amount']
            unit = request.POST['unit']
            dish = Item.objects.filter(rest_id=rid).filter(name=request.POST['ingred_dish'])

            if not ingred_to_add:
                error = "Please search for and select an ingredient"
            elif not amount or float(amount) < 0:
                error = 'Please input a valid amount'
            elif amount == '0':
                error = 'Please input an amount'


            if error:
                print 'major error: ', error

            if not error:
                i_t_a = Ingredient.objects.filter(ingredient=ingred_to_add)
                
                if unit == 'g':
                    amnt_grams = float(amount)
                elif unit == 'oz':
                    amnt_grams = float(amount) * 28.3495
                elif unit == 'tsp':
                    amnt_grams = float(amount) * 4.92892
                elif unit == 'tblspn':
                    amnt_grams = float(amount) * 14.78676
                elif unit == 'Fl. Oz':
                    amnt_grams = float(amount) * 0.0338150371
                
                amnt_grams = "{0:.2f}".format(round(amnt_grams,2))
                
                i_t_a_id = i_t_a.values_list('id')[0][0]
                
                added_ingred_ids = dish.values_list('ingredients')
                for ind in range(0, len(added_ingred_ids)):       
                    index = added_ingred_ids[ind][0]
                    if index != None:
                        print 'index'
                        print index
                        #grab id of ingredient
                        prev_ads = Addition.objects.filter(id=index).values_list('ingred_id')[0][0]
                        print 'hi'
                        if prev_ads == i_t_a_id:
                            error = "Ingredient already added to dish"

                if not error:                  
                    addition = Addition(amount_grams=amnt_grams)
                    addition.ingred_id = i_t_a_id 
                    addition.save()     
                    dish[0].ingredients.add(addition)


            
            
            data = {}
            data['error'] = error
            data['d_name'] = request.POST['ingred_dish']
            
            if not error:
                added_ingred_ids = dish.values_list('ingredients')
                for ind in range(0,len(added_ingred_ids)):
                    index = added_ingred_ids[ind][0]
                    print index
                    data[index] = str(Addition.objects.filter(id=index)[0])
                    print data[index]
                
            print data
            
            return HttpResponse(json.dumps(data), content_type="application/json")

        if 'dish_name' in request.POST:
            d_name = request.POST['dish_name']
            d_price = request.POST['dish_price']
            print Item.objects.filter(name=d_name).filter(rest_id=rid)
            if not d_name:
                error = 'Please enter a dish name'
            elif Item.objects.filter(name=d_name).filter(rest_id=rid):
                error = 'Dish already exists on this menu'
            elif not d_price:
                error = "Please enter a dish price"
            else:
                try:
                    if float(d_price) == 0:
                        error = "Please enter a dish price"
                except ValueError:
                    error='Please enter a valid dish price'
            print 'the error is: ', error
            if not error:   
                print d_name, d_price, rid
                r = Restaurant.objects.filter(id=rid)
                print r
                i = Item(name=d_name, rest_id=rid, price=d_price)
                i.save()
            data = {'error':error, 'd_name':d_name}
            return HttpResponse(json.dumps(data), content_type="application/json")

        if 'delete_key' in request.POST:
            error = ''
            print "HEYO"
            delete_key = request.POST['delete_key']
            dish = Item.objects.filter(rest_id=rid).filter(name=request.POST['ingred_dish'])
            Addition.objects.filter(id=delete_key).delete()


            data = {}
            data['error'] = error
            data['d_name'] = request.POST['ingred_dish']

            added_ingred_ids = dish.values_list('ingredients')
            print added_ingred_ids
            for ind in range(0,len(added_ingred_ids)):
                index = added_ingred_ids[ind][0]
                if index != None:
                    print index
                    data[index] = str(Addition.objects.filter(id=index)[0])
                    print data[index]

            return HttpResponse(json.dumps(data), content_type="application/json")

    return render(request, 'nutri_form.html', {'ingred_list':ingred_list, 'error':error})

def add_restaurant(request):
    error = ""
    rest_name = ""
    num_street = ""
    city = ""
    state = "--"
    zipcode = ""
    print request.user
    print request.user.id
    if not request.user or request.user.is_anonymous():
        error = 'You must be signed into an account to create a restaurant'

    if request.method == 'POST':


        rest_name = request.POST['rest_name']
        if not rest_name and not error:
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
            r = Restaurant(name=rest_name, number=num, street=street, city=city, state=state, zipcode=zipcode, user=request.user)
            r.save()
            rid = r.id
            print rid
            return HttpResponseRedirect('/restaurant_profile/' + str(rid))


    return render(request, 'add_rest.html', {'error':error, 'rest_name':rest_name, 'num_street':num_street, 'city':city, 'state':state, 'zipcode':zipcode})
    
def restaurant_profile(request, rid):
    print rid
    print request.user.username
    if request.method == 'POST':
        return HttpResponseRedirect('/add_dish/' + rid)

    restaurant = Restaurant.objects.filter(id=rid)[0]


    menu = Item.objects.filter(rest_id=rid).filter(valid=True)
    print menu
    strings = []
    for item in menu:
        price = '$' + str(item.price)
        cal = 0
        gpro = 0
        gfat = 0
        gcarb = 0
        gsug = 0 
        mgna = 0

        for add in item.ingredients.all():
            ingred = Ingredient.objects.filter(id=add.ingred_id)[0]
            amount = add.amount_grams
            print ingred
            cal = cal + ingred.calories*amount
            gpro = gpro + ingred.protein*amount
            gfat = gfat + ingred.fat*amount
            gcarb = gcarb + ingred.carbs*amount
            gsug = gsug + ingred.sugar*amount
            mgna = mgna + ingred.sodium*amount
        
        strings.append(item.name)
        strings.append("%.2f" % cal)
        strings.append("%.2f" % gpro)
        strings.append("%.2f" % gfat)
        strings.append("%.2f" % gcarb)
        strings.append("%.2f" % gsug)
        strings.append("%.2f" % mgna)
        strings.append(price)
      
    print strings

    return render(request, 'rest_profile.html', {'uname':request.user.username, 'rest':restaurant, 'strings':strings})


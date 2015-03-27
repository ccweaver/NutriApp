from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import HttpResponseForbidden
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
from datetime import datetime

    
def sign_in(request):
    invalid = ""
    error = ""
    uform = UserForm
    is_user = False
    if request.user.username != '':
        is_user = True

    print request.user
    print is_user

    
    if request.method == 'GET':
        if 'search' in request.GET:
            term = request.GET['search']
            print term
            
            zRE = re.compile("^[0-9][0-9][0-9][0-9][0-9]$")
            if zRE.match(term):
                restaurants = Restaurant.objects.all().order_by('zipcode').order_by('street')
                rs = []
                for r in restaurants:
                    rs.append({'r':r.name, 'zipDist':abs(int(r.zipcode)-int(term)), 'rid':r.id, 's':r.street, 't':r.number, 'u':r.city, 'v':r.state, 'w':r.zipcode, 'x':r.cuisine, 'y':r.seamless})
                r_zipSorted = sorted(rs, key=lambda r: r['zipDist'])
                return render(request, 'search_results.html', {'rests':r_zipSorted})

            else:
                r_citySorted = Restaurant.objects.filter(city__icontains=term).order_by('street')
                rs = []
                for r in r_citySorted:
                    rs.append({'r':r.name, 'rid':r.id, 's':r.street, 't':r.number, 'u':r.city, 'v':r.state, 'w':r.zipcode, 'x':r.cuisine, 'y':r.seamless})
                return render(request, 'search_results.html', {'rests':rs})

    if request.method == 'POST':
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
                address = '/restaurant_profile/' + str(rest_id[0].id)
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
    alpha_ingreds = Ingredient.objects.order_by('name')
    error = ""
    add_i = {}
    #['jelly beans,RAW(of course)', 'barnacles']
    rest = None
    rest_list = Restaurant.objects.filter(id=rid)
    if len(rest_list) > 0:
        rest = rest_list[0]

    if not rest:
        return HttpResponseForbidden()
    if rest.user.id != request.user.id:
        return HttpResponseForbidden()

    if request.method == 'POST':
        print request.POST
        if 'done' in request.POST:
            dish = Item.objects.filter(rest_id=rid).filter(name=request.POST['ingred_dish'])[0]
            dish.valid = True;
            dish.save()
            data = {'rid':rid}
            return HttpResponse(json.dumps(data), content_type="application/json")
        if 'term' in request.POST:
            print request.POST['term']
            terms = request.POST['term'].split(' ')

            if len(terms) == 1:
                ingred_list = Ingredient.objects.filter(ingredient__icontains=request.POST['term']).order_by('ingredient')
            if len(terms) == 2:
                ingred_list = Ingredient.objects.filter(ingredient__icontains=terms[0]).filter(ingredient__icontains=terms[1]).order_by('ingredient')
            if len(terms) == 3:
                ingred_list = Ingredient.objects.filter(ingredient__icontains=terms[0]).filter(ingredient__icontains=terms[1]).filter(ingredient__icontains=terms[2]).order_by('ingredient')
            if len(terms) == 4:
                ingred_list = Ingredient.objects.filter(ingredient__icontains=terms[0]).filter(ingredient__icontains=terms[1]).filter(ingredient__icontains=terms[2]).filter(ingredient__icontains=terms[3]).order_by('ingredient')


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
                error = "Please search for and select (by clicking on) an ingredient. Then enter an amount, and click Add Ingredient."
            elif not amount or float(amount) < 0:
                error = 'Please input a valid amount'
            elif amount == '0':
                error = 'Please input an amount. Then click Add Ingredient.'


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
                    amnt_grams = float(amount) * 30
                
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
            d_description = request.POST['dish_description']
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
                r = Restaurant.objects.filter(id=rid)
                i = Item(name=d_name, rest_id=rid, price=d_price, description=d_description)
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
    cuisine = "American, Chinese, Mexican, etc."
    seamless = ""
    num_street = ""
    city = ""
    state = "--"
    zipcode = ""
    website = ""
    phone = ""
    MoOpen = ""
    MoClose = ""
    TuOpen = ""
    TuClose = ""
    WeOpen = ""
    WeClose = ""
    ThOpen = ""
    ThClose = ""
    FrOpen = ""
    FrClose = ""
    SaOpen = ""
    SaClose = ""
    SuOpen = ""
    SuClose = ""    
    print request.user
    print request.user.id
    if not request.user or request.user.is_anonymous():
        error = 'You must be signed into an account to create a restaurant'

    if request.method == 'POST':


        rest_name = request.POST['rest_name']
        if not rest_name and not error:
            error = 'Please enter the name of your restaurant'

        cuisine = request.POST['cuisine']
        if not cuisine or cuisine == 'American, Chinese, Mexican, etc.' and not error:
            error = 'Please enter a cuisine type'

        seamless = request.POST['seamless']
        
        website = request.POST['website']
        zRE = re.compile("^.+\..{2,3}$")
        h = re.compile("^http:.*")
        hs = re.compile("^https:.*")
        w = re.compile("^www\..*")
        if not website and not error:
            error = "Please enter a valid website"
        elif (not h.match(website)) and (not hs.match(website)):
            if w.match(website):
                website = "http://" + website
            elif zRE.match(website):
                website = "http://www." + website
            elif not error:
                error = "Please enter a valid website"


        phone = request.POST['phone']
        zRE = re.compile("^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$")
        if not zRE.match(phone) and not error:
            error = 'Please enter a valid 10 digit phone number'
        elif zRE.match(phone):
            phoneNum = phone.replace('-', '').replace(' ', '').replace('(', '').replace(')', '').replace('+', '') 
            print phoneNum
            phoneNum = int(float(phoneNum))

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
            street = street + ' ' + nsSplit[x]

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

        #opening times
        rawTime = request.POST['MoOpen']
        split = rawTime.split(':')
        hr = split[0]
        if hr == '12':
            hr = '0'
        mi = int(split[1].split(' ')[0])
        if split[1].split(' ')[1] == 'pm':
            hr = int(hr) + 12
        MoOpen = datetime(2014, 3, 9, int(hr), mi)

        rawTime = request.POST['TuOpen']
        split = rawTime.split(':')
        hr = split[0]
        if hr == '12':
            hr = '0'
        mi = int(split[1].split(' ')[0])
        if split[1].split(' ')[1] == 'pm':
            hr = int(hr) + 12
        TuOpen = datetime(2014, 3, 9, int(hr), mi)

        rawTime = request.POST['WeOpen']
        split = rawTime.split(':')
        hr = split[0]
        if hr == '12':
            hr = '0'
        mi = int(split[1].split(' ')[0])
        if split[1].split(' ')[1] == 'pm':
            hr = int(hr) + 12
        WeOpen = datetime(2014, 3, 9, int(hr), mi)

        rawTime = request.POST['ThOpen']
        split = rawTime.split(':')
        hr = split[0]
        if hr == '12':
            hr = '0'
        mi = int(split[1].split(' ')[0])
        if split[1].split(' ')[1] == 'pm':
            hr = int(hr) + 12
        ThOpen = datetime(2014, 3, 9, int(hr), mi)

        rawTime = request.POST['FrOpen']
        split = rawTime.split(':')
        hr = split[0]
        if hr == '12':
            hr = '0'
        mi = int(split[1].split(' ')[0])
        if split[1].split(' ')[1] == 'pm':
            hr = int(hr) + 12
        FrOpen = datetime(2014, 3, 9, int(hr), mi)

        rawTime = request.POST['SaOpen']
        split = rawTime.split(':')
        hr = split[0]
        if hr == '12':
            hr = '0'
        mi = int(split[1].split(' ')[0])
        if split[1].split(' ')[1] == 'pm':
            hr = int(hr) + 12
        SaOpen = datetime(2014, 3, 9, int(hr), mi)

        rawTime = request.POST['SuOpen']
        split = rawTime.split(':')
        hr = split[0]
        if hr == '12':
            hr = '0'
        mi = int(split[1].split(' ')[0])
        if split[1].split(' ')[1] == 'pm':
            hr = int(hr) + 12
        SuOpen = datetime(2014, 3, 9, int(hr), mi)

        #closing times
        rawTime = request.POST['MoClose']
        split = rawTime.split(':')
        hr = split[0]
        if hr == '12':
            hr = '0'
        mi = int(split[1].split(' ')[0])
        if split[1].split(' ')[1] == 'pm':
            hr = int(hr) + 12
        MoClose = datetime(2014, 3, 9, int(hr), mi)

        rawTime = request.POST['TuClose']
        split = rawTime.split(':')
        hr = split[0]
        if hr == '12':
            hr = '0'
        mi = int(split[1].split(' ')[0])
        if split[1].split(' ')[1] == 'pm':
            hr = int(hr) + 12
        TuClose = datetime(2014, 3, 9, int(hr), mi)

        rawTime = request.POST['WeClose']
        split = rawTime.split(':')
        hr = split[0]
        if hr == '12':
            hr = '0'
        mi = int(split[1].split(' ')[0])
        if split[1].split(' ')[1] == 'pm':
            hr = int(hr) + 12
        WeClose = datetime(2014, 3, 9, int(hr), mi)

        rawTime = request.POST['ThClose']
        split = rawTime.split(':')
        hr = split[0]
        if hr == '12':
            hr = '0'
        mi = int(split[1].split(' ')[0])
        if split[1].split(' ')[1] == 'pm':
            hr = int(hr) + 12
        ThClose = datetime(2014, 3, 9, int(hr), mi)

        rawTime = request.POST['FrClose']
        split = rawTime.split(':')
        hr = split[0]
        if hr == '12':
            hr = '0'
        mi = int(split[1].split(' ')[0])
        if split[1].split(' ')[1] == 'pm':
            hr = int(hr) + 12
        FrClose = datetime(2014, 3, 9, int(hr), mi)

        rawTime = request.POST['SaClose']
        split = rawTime.split(':')
        hr = split[0]
        if hr == '12':
            hr = '0'
        mi = int(split[1].split(' ')[0])
        if split[1].split(' ')[1] == 'pm':
            hr = int(hr) + 12
        SaClose = datetime(2014, 3, 9, int(hr), mi)

        rawTime = request.POST['SuClose']
        split = rawTime.split(':')
        hr = split[0]
        if hr == '12':
            hr = '0'
        mi = int(split[1].split(' ')[0])
        if split[1].split(' ')[1] == 'pm':
            hr = int(hr) + 12
        SuClose = datetime(2014, 3, 9, int(hr), mi)


        if not error:
            r = Restaurant(name=rest_name, cuisine=cuisine, seamless=seamless, number=num, street=street, city=city, state=state, zipcode=zipcode, website=website, phone=phoneNum, moopen=MoOpen, tuopen=TuOpen, weopen=WeOpen, thopen=ThOpen, fropen=FrOpen, saopen=SaOpen, suopen=SuOpen, moclose=MoClose, tuclose=TuClose, weclose=WeClose, thclose=ThClose, frclose=FrClose, saclose=SaClose, suclose=SuClose, user=request.user)
            r.save()
            rid = r.id
            print rid
            return HttpResponseRedirect('/restaurant_profile/' + str(rid))


    return render(request, 'add_rest.html', {'error':error, 'cuisine':cuisine, 'seamless':seamless, 'rest_name':rest_name, 'num_street':num_street, 'city':city, 'state':state, 'zipcode':zipcode, 'website':website, 'phone':phone, 'MoOpen':MoOpen, 'TuOpen':TuOpen, 'WeOpen':WeOpen, 'ThOpen':ThOpen, 'FrOpen':FrOpen, 'SaOpen':SaOpen, 'SuOpen':SuOpen, 'MoClose':MoClose, 'TuClose':TuClose, 'WeClose':WeClose, 'ThClose':ThClose, 'FrClose':FrClose, 'SaClose':SaClose, 'SuClose':SuClose})
    
def restaurant_profile(request, rid):
    MoOpen = ""
    MoClose = ""
    TuOpen = ""
    TuClose = ""
    WeOpen = ""
    WeClose = ""
    ThOpen = ""
    ThClose = ""
    FrOpen = ""
    FrClose = ""
    SaOpen = ""
    SaClose = ""
    SuOpen = ""
    SuClose = ""   
    print rid
    print request.user.username
    
    my_prof = False
    no_seamless = False

    restaurant = Restaurant.objects.filter(id=rid)[0]
    if restaurant.user.id == request.user.id:
        my_prof = True
    else:
        restaurant.hits = restaurant.hits + 1
        restaurant.save()

    if restaurant.seamless == 'No':
        no_seamless = True

    website = str(restaurant.website)
    address = str(restaurant.number) + ' ' + str(restaurant.street)
    city_st_zip = str(restaurant.city) + ', ' + str(restaurant.state) + ', ' + str(restaurant.zipcode)
    
    phone = str(restaurant.phone)
    if len(phone) == 10:
        phone = '(' + phone[0:3] + ') ' + phone[3:6] + '-' + phone[6:10]
    
    hr = restaurant.moopen.hour
    mi = restaurant.moopen.minute
    if str(mi) == '0':
        mi = '00'
    if hr == 0:
        MoOpen = 12 + str(':') + str(mi) + ' am'
    elif hr > 12:
        MoOpen = str(hr - 12) + str(':') + str(mi) + ' pm'
    else:
        MoOpen = str(hr) + str(':') + str(mi) + ' am'
    
    hr = restaurant.tuopen.hour
    mi = restaurant.tuopen.minute
    if str(mi) == '0':
        mi = '00'
    if hr == 0:
        TuOpen = 12 + str(':') + str(mi) + ' am'
    elif hr > 12:
        TuOpen = str(hr - 12) + str(':') + str(mi) + ' pm'
    else:
        TuOpen = str(hr) + str(':') + str(mi) + ' am'

    hr = restaurant.weopen.hour
    mi = restaurant.weopen.minute
    if str(mi) == '0':
        mi = '00'
    if hr == 0:
        WeOpen = 12 + str(':') + str(mi) + ' am'
    elif hr > 12:
        WeOpen = str(hr - 12) + str(':') + str(mi) + ' pm'
    else:
        WeOpen = str(hr) + str(':') + str(mi) + ' am'

    hr = restaurant.thopen.hour
    mi = restaurant.thopen.minute
    if str(mi) == '0':
        mi = '00'
    if hr == 0:
        ThOpen = 12 + str(':') + str(mi) + ' am'
    elif hr > 12:
        ThOpen = str(hr - 12) + str(':') + str(mi) + ' pm'
    else:
        ThOpen = str(hr) + str(':') + str(mi) + ' am'
    
    hr = restaurant.fropen.hour
    mi = restaurant.fropen.minute
    if str(mi) == '0':
        mi = '00'
    if hr == 0:
        FrOpen = 12 + str(':') + str(mi) + ' am'
    elif hr > 12:
        FrOpen = str(hr - 12) + str(':') + str(mi) + ' pm'
    else:
        FrOpen = str(hr) + str(':') + str(mi) + ' am'
    
    hr = restaurant.saopen.hour
    mi = restaurant.saopen.minute
    if str(mi) == '0':
        mi = '00'
    if hr == 0:
        SaOpen = 12 + str(':') + str(mi) + ' am'
    elif hr > 12:
        SaOpen = str(hr - 12) + str(':') + str(mi) + ' pm'
    else:
        SaOpen = str(hr) + str(':') + str(mi) + ' am'
    
    hr = restaurant.suopen.hour
    mi = restaurant.suopen.minute
    if str(mi) == '0':
        mi = '00'
    if hr == 0:
        SuOpen = 12 + str(':') + str(mi) + ' am'
    elif hr > 12:
        SuOpen = str(hr - 12) + str(':') + str(mi) + ' pm'
    else:
        SuOpen = str(hr) + str(':') + str(mi) + ' am'

    #closing times
    hr = restaurant.moclose.hour
    mi = restaurant.moclose.minute
    if str(mi) == '0':
        mi = '00'
    if hr == 0:
        MoClose = 12 + str(':') + str(mi) + ' am'
    elif hr > 12:
        MoClose = str(hr - 12) + str(':') + str(mi) + ' pm'
    else:
        MoClose = str(hr) + str(':') + str(mi) + ' am'
    
    hr = restaurant.tuclose.hour
    mi = restaurant.tuclose.minute
    if str(mi) == '0':
        mi = '00'
    if hr == 0:
        TuClose = 12 + str(':') + str(mi) + ' am'
    elif hr > 12:
        TuClose = str(hr - 12) + str(':') + str(mi) + ' pm'
    else:
        TuClose = str(hr) + str(':') + str(mi) + ' am'

    hr = restaurant.weclose.hour
    mi = restaurant.weclose.minute
    if str(mi) == '0':
        mi = '00'
    if hr == 0:
        WeClose = 12 + str(':') + str(mi) + ' am'
    elif hr > 12:
        WeClose = str(hr - 12) + str(':') + str(mi) + ' pm'
    else:
        WeClose = str(hr) + str(':') + str(mi) + ' am'

    hr = restaurant.thclose.hour
    mi = restaurant.thclose.minute
    if str(mi) == '0':
        mi = '00'
    if hr == 0:
        ThClose = 12 + str(':') + str(mi) + ' am'
    elif hr > 12:
        ThClose = str(hr - 12) + str(':') + str(mi) + ' pm'
    else:
        ThClose = str(hr) + str(':') + str(mi) + ' am'
    
    hr = restaurant.frclose.hour
    mi = restaurant.frclose.minute
    if str(mi) == '0':
        mi = '00'
    if hr == 0:
        FrClose = 12 + str(':') + str(mi) + ' am'
    elif hr > 12:
        FrClose = str(hr - 12) + str(':') + str(mi) + ' pm'
    else:
        FrClose = str(hr) + str(':') + str(mi) + ' am'
    
    hr = restaurant.saclose.hour
    mi = restaurant.saclose.minute
    if str(mi) == '0':
        mi = '00'
    if hr == 0:
        SaClose = 12 + str(':') + str(mi) + ' am'
    elif hr > 12:
        SaClose = str(hr - 12) + str(':') + str(mi) + ' pm'
    else:
        SaClose = str(hr) + str(':') + str(mi) + ' am'
    
    hr = restaurant.suclose.hour
    mi = restaurant.suclose.minute
    if str(mi) == '0':
        mi = '00'
    if hr == 0:
        SuClose = 12 + str(':') + str(mi) + ' am'
    elif hr > 12:
        SuClose = str(hr - 12) + str(':') + str(mi) + ' pm'
    else:
        SuClose = str(hr) + str(':') + str(mi) + ' am'

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
        description = str(item.description)

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
        
        calbyTen = cal/10
        calbyTen = round(calbyTen)
        cal = calbyTen*10
        strings.append(item.name)
        strings.append("%d" % cal)
        strings.append("%d" % gpro)
        strings.append("%d" % gfat)
        strings.append("%d" % gcarb)
        strings.append("%d" % gsug)
        strings.append("%d" % mgna)
        strings.append(price)
        strings.append(description)
      
    print strings


    if request.method == 'POST':
        if 'delete_key' in request.POST:
            print request.POST['delete_key']
            delete_item = Item.objects.filter(rest_id=rid).filter(valid=True).filter(name=request.POST['delete_key'])[0]
            print delete_item
            for add in delete_item.ingredients.all():
                print add.id
                add.delete()
            delete_item.delete()

            return render(request, 'rest_profile.html', {'no_seamless':no_seamless, 'hits':restaurant.hits, 'my_prof':my_prof, 'uname':request.user.username, 'rest':restaurant, 'strings':strings, 'address':address, 'website':website, 'csz':city_st_zip, 'phone':phone, \
            'MoOpen':MoOpen, 'TuOpen':TuOpen, 'WeOpen':WeOpen, 'ThOpen':ThOpen, 'FrOpen':FrOpen, 'SaOpen':SaOpen, 'SuOpen':SuOpen, 'MoClose':MoClose, 'TuClose':TuClose, 'WeClose':WeClose, 'ThClose':ThClose, 'FrClose':FrClose, 'SaClose':SaClose, 'SuClose':SuClose})

        if 'ingred_dish' in request.POST:
            print '*****************'
            print request.POST['ingred_dish']
            item = Item.objects.filter(rest_id=rid).filter(valid=True).filter(name=request.POST['ingred_dish'])[0]
            ingreds = []
            for i in item.ingredients.all():
                ingreds.append(str(i.ingred) + ' ' + str(i.amount_grams) + 'g')
            print ingreds

            data = {'ingreds':ingreds, 'dish':request.POST['ingred_dish']}
            return HttpResponse(json.dumps(data), content_type="application/json")

        return HttpResponseRedirect('/add_dish/' + rid)
    
    return render(request, 'rest_profile.html', {'no_seamless':no_seamless, 'hits':restaurant.hits, 'my_prof':my_prof, 'uname':request.user.username, 'rest':restaurant, 'strings':strings, 'address':address, 'website':website, 'csz':city_st_zip, 'phone':phone, \
        'MoOpen':MoOpen, 'TuOpen':TuOpen, 'WeOpen':WeOpen, 'ThOpen':ThOpen, 'FrOpen':FrOpen, 'SaOpen':SaOpen, 'SuOpen':SuOpen, 'MoClose':MoClose, 'TuClose':TuClose, 'WeClose':WeClose, 'ThClose':ThClose, 'FrClose':FrClose, 'SaClose':SaClose, 'SuClose':SuClose})


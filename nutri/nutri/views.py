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
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib import auth
from datetime import datetime
from operator import itemgetter

    
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
            return HttpResponseRedirect('/search/' + str(request.GET['search']))

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

def search_results(request, term, page=1):
    print "Searching for: " + term
    print "Page: " + str(page) 

    #################
    # Zip Code Search
    #################
    zRE = re.compile("^[0-9][0-9][0-9][0-9][0-9]$")
    if zRE.match(term):
        restaurants = Restaurant.objects.all().order_by('zipcode').order_by('street', 'number')
        rs = []
        for r in restaurants:
            bool_dm = False
            if r.cuisine2:
                if r.cuisine3:
                    cuisine = r.cuisine1 + ', ' + r.cuisine2 + ', ' + r.cuisine3
                else:
                    cuisine = r.cuisine1 + ', ' + r.cuisine2
            else:
                cuisine = r.cuisine1
            if r.delivery_min != 0:
                bool_dm = True
            rs.append({'r':r.name, 'zipDist':abs(int(r.zipcode)-int(term)), 'rid':r.id, 's':r.street, 't':r.number, 'u':r.city, 'v':r.state, 'w':r.zipcode, 'x':cuisine, 'y':r.seamless, 'z':r.delivery_min, 'bool_dm':bool_dm})
        rs = sorted(rs, key=lambda r: r['zipDist'])


    #################
    # City Search
    ################
    else:
        rests = Restaurant.objects.filter(Q(city__icontains=term) | Q(street__icontains=term) | Q(name__icontains=term)).order_by('street', 'number')
        rs = []
        for r in rests:
            bool_dm = False
            if r.cuisine2:
                if r.cuisine3:
                    cuisine = r.cuisine1 + ', ' + r.cuisine2 + ', ' + r.cuisine3
                else:
                    cuisine = r.cuisine1 + ', ' + r.cuisine2
            else:
                cuisine = r.cuisine1
            if r.delivery_min != 0:
                bool_dm = True
            rs.append({'r':r.name, 'rid':r.id, 's':r.street, 't':r.number, 'u':r.city, 'v':r.state, 'w':r.zipcode, 'x':cuisine, 'y':r.seamless, 'z':r.delivery_min, 'bool_dm':bool_dm})
    
    
    if int(page) == 1:
        rs_10 = rs[:10]
    else:
        low_index = 10*(int(page)-1)
        high_index = 10* (int(page))
        rs_10 = rs[low_index:high_index]
    return render(request, 'search_results.html', {'rests':rs_10, 'num_rests':len(rs), 'page':int(page), 'page_mult10':int(page)*10, 'term':term})

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
            print ingred_list
            if ingred_list:
                ingreds = []
                print 'hi'
                for i in ingred_list:
                    tup = (i, str(i).lower().index(terms[0].lower()))
                    ingreds.append(tup)
                ingreds = sorted(ingreds, key=itemgetter(1))
                ingreds_sorted = []
                for x in ingreds:
                    ingreds_sorted.append(x[0])

            elif not ingred_list:
                ingreds_sorted = ['Sorry, no ingredient found']
            if not request.POST['term']:
                ingreds_sorted = []
            
            #count = 10
            #for x in range(0,count):
            #   print ingred_list[x].id
            return render(request, 'select_temp.html', {'ingred_list':ingreds_sorted, 'error':error, 'added_ingreds':add_i})
        
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
                
                density = float(i_t_a.values_list('g_per_ml')[0][0])
                print 'a;lskdjf;lasdkj'
                #unit conversions
                if unit == 'g':
                    amnt_grams = float(amount)
                elif unit == 'oz':
                    amnt_grams = float(amount) * 28.3495
                elif unit == 'tsp':
                    amnt_grams = float(amount) * 4.92892 * density
                elif unit == 'tblspn':
                    amnt_grams = float(amount) * 14.78676 * density
                elif unit == 'Fl. Oz':
                    amnt_grams = float(amount) * 30 * density

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
                    print dish[0]
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
            elif Item.objects.filter(name=d_name).filter(rest_id=rid).filter(valid=True):
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

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def add_restaurant(request):
    error = ""
    rest_name = ""
    cuisine = ""
    c1 = ""
    c2 = ""
    c3 = ""
    seamless = ""
    deliv_min = "0"
    num_street = ""
    city = ""
    state = "No Selection"
    zipcode = ""
    website = ""
    yelp = ""
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


       
        cuisine = request.POST.getlist('cuisine[]')
        if not cuisine and not error:
            error = 'Please enter a cuisine type'
        print cuisine
        if cuisine:
            c1 = cuisine[0]
            if len(cuisine) > 1:
                c2 = cuisine[1]
                if len(cuisine) > 2:
                    c3 = cuisine[2]

        seamless = request.POST['seamless']

        deliv_min = request.POST['deliv_min']
        if not is_number(deliv_min) and not error:
            error = "Please enter a valid Delivery Minimum"

        website = request.POST['website']
        zRE = re.compile("^.+\..{2,3}$")
        h = re.compile("^http:.*")
        hs = re.compile("^https:.*")
        w = re.compile("^www\..*")
        if not website and not error:
            error="Please enter a valid website"
        elif (not h.match(website)) and (not hs.match(website)):
            if w.match(website):
                website = "http://" + website
            elif zRE.match(website):
                website = "http://www." + website
            elif not error:
                error = "Please enter a valid website"
            

        
        zRE = re.compile("^.+yelp\..+$")
        jk = re.compile("^http:.*")
        kk = re.compile("^https:.*")
        lm = re.compile("^www\..*")
        if (not jk.match(yelp)) and (not kk.match(yelp)):
            if lm.match(yelp):
                yelp = "http://" + yelp 
            elif zRE.match(yelp):
                yelp = "http://www." + yelp

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
        
        state = request.POST.get('state', None)
        if state == '--' and not error:
            error = 'Please select a state'

        zipcode = request.POST['zipcode']
        zRE = re.compile("^[0-9][0-9][0-9][0-9][0-9]$")
        if not zRE.match(zipcode) and not error:
            error = 'Please enter a valid 5 digit zip code'

        #opening times
        MoOpen = request.POST['MoOpen']
        TuOpen = request.POST['TuOpen']
        WeOpen = request.POST['WeOpen']
        ThOpen = request.POST['ThOpen']
        FrOpen = request.POST['FrOpen']
        SaOpen = request.POST['SaOpen']
        SuOpen = request.POST['SuOpen']
        
        MoClose = request.POST['MoClose']
        TuClose = request.POST['TuClose']
        WeClose = request.POST['WeClose']
        ThClose = request.POST['ThClose']
        FrClose = request.POST['FrClose']
        SaClose = request.POST['SaClose']
        SuClose = request.POST['SuClose']


        if not error:
            r = Restaurant(name=rest_name, cuisine1=c1, cuisine2=c2, cuisine3=c3, seamless=seamless, delivery_min=deliv_min, number=num, street=street, city=city, state=state, zipcode=zipcode, website=website, yelp=yelp, phone=phoneNum, moopen=MoOpen, tuopen=TuOpen, weopen=WeOpen, thopen=ThOpen, fropen=FrOpen, saopen=SaOpen, suopen=SuOpen, moclose=MoClose, tuclose=TuClose, weclose=WeClose, thclose=ThClose, frclose=FrClose, saclose=SaClose, suclose=SuClose, user=request.user)
            r.save()
            rid = r.id
            print rid
            return HttpResponseRedirect('/restaurant_profile/' + str(rid))
    

    return render(request, 'add_rest.html', {'error':error, 'cuisine':cuisine, 'seamless':seamless, 'deliv_min':deliv_min, 'rest_name':rest_name, 'num_street':num_street, 'city':city, 'state':state, 'zipcode':zipcode, 'website':website, 'yelp':yelp, 'phone':phone, 'MoOpen':MoOpen, 'TuOpen':TuOpen, 'WeOpen':WeOpen, 'ThOpen':ThOpen, 'FrOpen':FrOpen, 'SaOpen':SaOpen, 'SuOpen':SuOpen, 'MoClose':MoClose, 'TuClose':TuClose, 'WeClose':WeClose, 'ThClose':ThClose, 'FrClose':FrClose, 'SaClose':SaClose, 'SuClose':SuClose})
    
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

    
    my_prof = False
    no_seamless = False
    no_yelp = False
    
   
    
    restaurant = Restaurant.objects.filter(id=rid)[0]
    if restaurant.user.id == request.user.id:
        my_prof = True
    else:
        restaurant.hits = restaurant.hits + 1
        restaurant.save()

    if restaurant.seamless == 'No':
        no_seamless = True
    
    if restaurant.yelp == "":
        no_yelp = True
    
  
    
    website = str(restaurant.website)
    yelp = str(restaurant.yelp)
    address = str(restaurant.number) + ' ' + str(restaurant.street)
    city_st_zip = str(restaurant.city) + ', ' + str(restaurant.state) + ', ' + str(restaurant.zipcode)
    
    phone = str(restaurant.phone)
    if len(phone) == 10:
        phone = '(' + phone[0:3] + ') ' + phone[3:6] + '-' + phone[6:10]
    
    MoOpen = restaurant.moopen
    TuOpen = restaurant.tuopen
    WeOpen = restaurant.weopen
    ThOpen = restaurant.thopen
    FrOpen = restaurant.fropen
    SaOpen = restaurant.saopen
    SuOpen = restaurant.suopen

    MoClose = restaurant.moclose
    TuClose = restaurant.tuclose
    WeClose = restaurant.weclose
    ThClose = restaurant.thclose
    FrClose = restaurant.frclose
    SaClose = restaurant.saclose
    SuClose = restaurant.suclose


    menu = Item.objects.filter(rest_id=rid).filter(valid=True)
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
            cal = cal + ingred.calories*amount
            gpro = gpro + ingred.protein*amount
            gfat = gfat + ingred.fat*amount
            gcarb = gcarb + ingred.carbs*amount
            gsug = gsug + ingred.sugar*amount
            mgna = mgna + ingred.sodium*amount
        
        calbyTen = cal/10
        calbyTen = round(calbyTen)
        mgnabyTen = mgna/10
        mgnabyTen = round(mgnabyTen)
        
        
        cal = calbyTen*10
        mgna = mgnabyTen*10 
        strings.append(item.name)
        strings.append("%d" % cal)
        strings.append("%d" % gpro)
        strings.append("%d" % gfat)
        strings.append("%d" % gcarb)
        strings.append("%d" % gsug)
        strings.append("%d (%d%s)" % (mgna, (100*mgna)/2500, '%'))
        strings.append(price)
        strings.append(description)


    if request.method == 'POST':
        if 'delete_key' in request.POST:
            delete_item = Item.objects.filter(rest_id=rid).filter(valid=True).filter(name=request.POST['delete_key'])[0]
            for add in delete_item.ingredients.all():
                add.delete()
            delete_item.delete()

            return render(request, 'rest_profile.html', {'no_yelp':no_yelp, 'no_seamless':no_seamless, 'hits':restaurant.hits, 'my_prof':my_prof, 'uname':request.user.username, 'rest':restaurant, 'strings':strings, 'address':address, 'website':website, 'yelp':yelp, 'csz':city_st_zip, 'phone':phone, \
            'MoOpen':MoOpen, 'TuOpen':TuOpen, 'WeOpen':WeOpen, 'ThOpen':ThOpen, 'FrOpen':FrOpen, 'SaOpen':SaOpen, 'SuOpen':SuOpen, 'MoClose':MoClose, 'TuClose':TuClose, 'WeClose':WeClose, 'ThClose':ThClose, 'FrClose':FrClose, 'SaClose':SaClose, 'SuClose':SuClose})

        if 'delete_ingred' in request.POST:
            dish = Item.objects.filter(rest_id=rid).filter(valid=True).filter(name=request.POST['dish'])[0]
            for add in dish.ingredients.all():
                if str(add.ingred) == str(request.POST['delete_ingred']):
                    add.delete()
            
            return render(request, 'rest_profile.html', {'no_yelp':no_yelp, 'no_seamless':no_seamless, 'hits':restaurant.hits, 'my_prof':my_prof, 'uname':request.user.username, 'rest':restaurant, 'strings':strings, 'address':address, 'website':website, 'yelp':yelp, 'csz':city_st_zip, 'phone':phone, \
            'MoOpen':MoOpen, 'TuOpen':TuOpen, 'WeOpen':WeOpen, 'ThOpen':ThOpen, 'FrOpen':FrOpen, 'SaOpen':SaOpen, 'SuOpen':SuOpen, 'MoClose':MoClose, 'TuClose':TuClose, 'WeClose':WeClose, 'ThClose':ThClose, 'FrClose':FrClose, 'SaClose':SaClose, 'SuClose':SuClose})


        if 'ingred_dish' in request.POST:
            item = Item.objects.filter(rest_id=rid).filter(valid=True).filter(name=request.POST['ingred_dish'])[0].order_by('calories')
            ingreds = "".order_by('calories')
            for i in item.ingredients.all():
                ingreds += '<span class="glyphicon glyphicon-remove-circle" onClick="removeIngred(\'' + str(i.ingred) + '\', \'' + request.POST['ingred_dish'] + '\')"></span>' + str(i.ingred) + ' ' + str(i.amount_grams) + 'g' + '<br>'
            data = {'ingreds':ingreds, 'dish':request.POST['ingred_dish'].order_by('calories')}
            return HttpResponse(json.dumps(data), content_type="application/json")

        return HttpResponseRedirect('/add_dish/' + rid)
    
    return render(request, 'rest_profile.html', {'no_yelp':no_yelp, 'no_seamless':no_seamless, 'hits':restaurant.hits, 'my_prof':my_prof, 'uname':request.user.username, 'rest':restaurant, 'strings':strings, 'address':address, 'website':website, 'yelp':yelp, 'csz':city_st_zip, 'phone':phone, \
        'MoOpen':MoOpen, 'TuOpen':TuOpen, 'WeOpen':WeOpen, 'ThOpen':ThOpen, 'FrOpen':FrOpen, 'SaOpen':SaOpen, 'SuOpen':SuOpen, 'MoClose':MoClose, 'TuClose':TuClose, 'WeClose':WeClose, 'ThClose':ThClose, 'FrClose':FrClose, 'SaClose':SaClose, 'SuClose':SuClose})


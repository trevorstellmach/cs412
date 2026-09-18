# File: restaurant/views.py
# Author: Trevor Stellmach, tstell@bu.edu (09/15/26)
# Description: Restaurant site views file

import random
import time
from django.shortcuts import render
from django.http import HttpResponse

specials = [
    "Pigs-in-a-blanket",
    "Chili Dog",
    "Corn Dog",
    "Foot-Long Dog"
]

prices = {
    "Classic Dog": 8,
    "Ketchup": 0.50,
    "Mustard": 0.50,
    "Relish": 0.50,
    "Chicago Dog": 9,
    "Fully Loaded Dog": 11,
    "Short Dog": 7,
    "Special": 8
}

# Create your views here.
def main(request):
    """ responds to 'main' url """

    template_name = "restaurant/main.html"      # assigns main html file to template_name

    return render(request, template_name)

def order(request):
    """ responds to 'order' url """

    #context variables
    context = {
        "special": specials[random.randint(0, len(specials) - 1)]   # picks random special
    }

    template_name = "restaurant/order.html"     # assigns order html file to template_name

    return render(request, template_name, context)

def confirmation(request):
    """ responds to 'confirmation' url """

    print(request.POST)

    cost = 0        # total cost
    food_order = [] # list of ordered food items
    toppings = []   # list of ordered toppings


    # pull form fields into data
    for x in request.POST:
        if x == 'csrfmiddlewaretoken':      # skip first in dictionary
            continue
        if x == "special_instructions":     # break at end of food items
            break
        if x == "Ketchup" or x == "Mustard" or x == "Relish":  # build 'toppings' list
            toppings += [x]
        else:
            food_order += [x]       # build 'food_order' list


    # add cost of food items to total cost
    for x in food_order:
        cost += prices[x]

    # add cost of toppings to total cost
    for x in toppings:
        cost += prices[x]

    # if no toppings, provide 'no toppings' message
    if toppings == []:
        toppings = ["No toppings"]

    # select ready time 30-60 minutes from current time
    readytime = time.time() + random.randint(1800, 3600)
    readytime = time.ctime(readytime)

    # context variables
    context = {
        "instructs": request.POST["special_instructions"],
        "name": request.POST["name"],
        "number": request.POST["number"],
        "email": request.POST["email"],
        "food_order": food_order,
        "toppings": toppings,
        "cost": cost,
        "readytime": readytime
    }

    
    # html template file
    template_name = "restaurant/confirmation.html"

    return render(request, template_name, context)
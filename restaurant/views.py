# File: restaurant/views.py
# Author: Trevor Stellmach, tstell@bu.edu (09/15/26)
# Description: Restaurant site views file

import random
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
    "Ketchup": 0.5,
    "Mustard": 0.5,
    "Relish": 0.5,
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

    cost = 0
    food_order = []
    toppings = []
    instructs = ""
    name = ""
    number = ""
    email = ""

    # check if POST data exists
    #if request.POST:

    # pull form fields into data
    for x in request.POST:
        print(request.POST[x])


    #context = {

    

    template_name = "restaurant/confirmation.html"

    return render(request, template_name)
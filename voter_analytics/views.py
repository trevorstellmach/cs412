# File: voter_analytics/views.py
# Author: Trevor Stellmach, tstell@bu.edu (10/27/26)
# Description: defines view classes and logic for voter_analytics

from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from datetime import date
from . models import Voter

# eligible birth years
YEARS = range(1920, 2005)

# list of potential parties
PARTIES = [
    "U ", "D ", "R ", "J ", "A ", "CC", "X ", "L ", "Q ", "S ",
    "FF", "G ", "HH", "T ", "AA", "GG", "Z ", "O ", "P ", "E ",
    "V ", "H ", "Y ", "W ", "EE", "K "
]

# list of previous elections
PREV_ELECTIONS = ["v20state", "v21town", "v21primary", "v22general", "v23town"]

# Create your views here.
class VotersListView(ListView):
    """view to display all Voter objects"""

    model = Voter
    template_name = 'voter_analytics/voters.html'
    context_object_name = 'voters'
    paginate_by = 100 # show 100 records per page

    def get_queryset(self):
        """returns queryset to be displayed on page"""
        voters =  super().get_queryset()

        print(self.request.GET)

        # look for party filter in url
        if 'party' in self.request.GET:
            party = self.request.GET['party']
            if party:
                voters = voters.filter(party_affiliation=party)

        # look for score filter in url
        if 'score' in self.request.GET:
            score = self.request.GET['score']
            if score:
                voters = voters.filter(voter_score = int(score))

        # look for min_dob filter in url
        if 'min_dob' in self.request.GET:
            min_dob = self.request.GET['min_dob']
            if min_dob:
                voters = voters.filter(date_of_birth__gte=date(int(min_dob), 1, 1))

        # look for max_dob filter in url
        if 'max_dob' in self.request.GET:
            max_dob = self.request.GET['max_dob']
            if max_dob:
                voters = voters.filter(date_of_birth__lte=date(int(max_dob), 1, 1))


        # look for previous elections in url
        if 'v20state' in self.request.GET:
            voters = voters.filter(v20state=True)

        if 'v21town' in self.request.GET:
            voters = voters.filter(v21town=True)

        if 'v21primary' in self.request.GET:
            voters = voters.filter(v21primary=True)

        if 'v22general' in self.request.GET:
            voters = voters.filter(v22general=True)

        if 'v23town' in self.request.GET:
            voters = voters.filter(v23town=True)

        return voters

    def get_context_data(self, **kwargs):
        """provides context variables to be used in template"""
        context = super().get_context_data(**kwargs)

        context['years'] = YEARS
        context['parties'] = PARTIES
        context['elections'] = PREV_ELECTIONS

        context["selected_party"] = self.request.GET.get("party")
        context["selected_voter_score"] = self.request.GET.get("score")
        context["selected_min_dob"] = self.request.GET.get("min_dob")
        context["selected_max_dob"] = self.request.GET.get("max_dob")

        print("CONTEXT", context["selected_party"])

        return context


class VoterDetailView(DetailView):
    """view to display single Voter object"""

    model = Voter
    template_name = "voter_analytics/voter_detail.html"
    context_object_name = 'v'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['map_url'] = "https://www.google.com/maps/place/" + self.object.street_number + "+" + self.object.street_name + "+Newton, MA"

        return context
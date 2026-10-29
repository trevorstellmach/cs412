# File: voter_analytics/views.py
# Author: Trevor Stellmach, tstell@bu.edu (10/27/26)
# Description: defines view classes and logic for voter_analytics

from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from datetime import date
from . models import Voter

import plotly
import plotly.graph_objs as go

# eligible birth years
YEARS = [str(x) for x in range(1920, 2005)]

# list of potential parties
PARTIES = [
    "U ", "D ", "R ", "J ", "A ", "CC", "X ", "L ", "Q ", "S ",
    "FF", "G ", "HH", "T ", "AA", "GG", "Z ", "O ", "P ", "E ",
    "V ", "H ", "Y ", "W ", "EE", "K "
]

# list of voter scores
SCORES = ['0', '1', '2', '3', '4', '5']

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

        # add lists to context data
        context['years'] = YEARS
        context['parties'] = PARTIES
        context['elections'] = PREV_ELECTIONS
        context['scores'] = SCORES

        # add previous input to context data
        context["selected_party"] = self.request.GET.get("party")
        context["selected_voter_score"] = self.request.GET.get("score")
        context["selected_min_dob"] = self.request.GET.get("min_dob")
        context["selected_max_dob"] = self.request.GET.get("max_dob")

        # allows filters to hold across pages
        params = self.request.GET.copy()
        params.pop("page", None)
        context["query_string"] = params.urlencode()

        return context


class VoterDetailView(DetailView):
    """view to display single Voter object"""

    model = Voter
    template_name = "voter_analytics/voter_detail.html"
    context_object_name = 'v'

    def get_context_data(self, **kwargs):
        """defines and retrieves context data to be used in template"""
        context = super().get_context_data(**kwargs)

        context['map_url'] = "https://www.google.com/maps/place/" + self.object.street_number + "+" + self.object.street_name + "+Newton, MA"

        return context

class GraphListView(ListView):
    """view to display graph representations of data"""

    model = Voter
    template_name = "voter_analytics/graphs.html"
    context_object_name = 'v'

    def get_context_data(self, **kwargs):
        """provides context variables for use in template"""
        context = super().get_context_data(**kwargs)
        v = self.get_queryset()

        # create bar chart for number of voters per birth year
        x = []
        y = []
        for i in range(1910, 2005):
            x += [str(i)]
            y += [len(v.filter(date_of_birth__year=i))]

        fig = go.Bar(x=x, y=y)
        title_text = "Number of Voters Per Birth Year"
        graph_div_years = plotly.offline.plot({"data": [fig],
                                                "layout_title_text": title_text,
                                                }, auto_open=False, 
                                                output_type="div",)

        context['graph_div_years'] = graph_div_years

        # create a pie chart for distribution of party affiliation
        x = PARTIES
        y = []
        for i in PARTIES:
            y += [len(v.filter(party_affiliation=i))]

        fig = go.Pie(labels=x, values=y)
        title_text = "Number of Voters Per Party"
        graph_div_party = plotly.offline.plot({"data": [fig],
                                                "layout_title_text": title_text,
                                                }, auto_open=False, 
                                                output_type="div",)

        context['graph_div_party'] = graph_div_party

        # create a bar chart for distribution of party affiliation
        x = PREV_ELECTIONS
        y = [len(v.filter(v20state=True))]
        y += [len(v.filter(v21town=True))]
        y += [len(v.filter(v21primary=True))]
        y += [len(v.filter(v22general=True))]
        y += [len(v.filter(v23town=True))]

        fig = go.Bar(x=x, y=y)
        title_text = "Number of Voters Per Election"
        graph_div_election = plotly.offline.plot({"data": [fig],
                                                "layout_title_text": title_text,
                                                }, auto_open=False, 
                                                output_type="div",)

        context['graph_div_election'] = graph_div_election

        # add lists to context data
        context['years'] = YEARS
        context['parties'] = PARTIES
        context['elections'] = PREV_ELECTIONS
        context['scores'] = SCORES

        # add previous input to context data
        context["selected_party"] = self.request.GET.get("party")
        context["selected_voter_score"] = self.request.GET.get("score")
        context["selected_min_dob"] = self.request.GET.get("min_dob")
        context["selected_max_dob"] = self.request.GET.get("max_dob")

        return context

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
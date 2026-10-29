# File: voter_analytics/models.py
# Author: Trevor Stellmach, tstell@bu.edu (10/27/26)
# Description: includes model classes and methods for voter_analytics

from django.db import models

def load_data():
    """loads data from CSV into Django database"""

    Voter.objects.all().delete()

    filename = '/Users/trevorstellmach/Downloads/newton_voters.csv'
    f = open(filename, 'r')
    f.readline() # discard headers
 
    for row in f:
 
        fields = row.split(',')

        try:
            voter = Voter(
                first_name=fields[1],
                last_name=fields[2],
                street_number=fields[3],
                street_name=fields[4],
                apt_number=fields[5],
                zip_code=fields[6],
                date_of_birth=fields[7],
                date_of_registration=fields[8],
                party_affiliation=fields[9],
                precinct_number=fields[10],
                v20state=(fields[11].strip().upper() == 'TRUE'),
                v21town=(fields[12].strip().upper() == 'TRUE'),
                v21primary=(fields[13].strip().upper() == 'TRUE'),
                v22general=(fields[14].strip().upper() == 'TRUE'),
                v23town=(fields[15].strip().upper() == 'TRUE'),
                voter_score=int(fields[16]),
            )

            voter.save()
        except:
            print(f'Skipped: {fields}')
    print('done')

# Create your models here.
class Voter(models.Model):
    """defines Voter model"""

    last_name = models.TextField()
    first_name = models.TextField()
    street_number = models.TextField()
    street_name = models.TextField()
    apt_number = models.TextField()
    zip_code = models.TextField()
    date_of_birth = models.DateField()
    date_of_registration = models.DateField()
    party_affiliation = models.CharField(max_length=2)
    precinct_number = models.TextField()

    v20state = models.BooleanField()
    v21town = models.BooleanField()
    v21primary = models.BooleanField()
    v22general = models.BooleanField()
    v23town = models.BooleanField()
    voter_score = models.IntegerField()

    def __str__(self):
        """returns string representation of Voter object"""
        return f'{self.first_name} {self.last_name} ({self.precinct_number}), party {self.party_affiliation}, score {self.voter_score}'


from __future__ import unicode_literals
import os
import re
import json
import django
from django.db import models
from Luna.models import DataWarehouse
from .utilities.user_list import *
from .utilities.coin_sharing_info import *
import random
import string

class coinManager(models.Manager):
    def random_string_generator(length=12):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    # print(random_string_generator())

    # Validates the redemption code that the user enters in
    def validate_redemption_code(self, clean_data, post_data):
        errors = []
        if len(self.filter(redemption_code=post_data['redemption_code'])) > 0:
    #         checks the redemption code to other codes
            coin_transaction = self.filter(redemption_code = clean_data(post_data['redemption_code']))[0]
            if not post_data['redemption_code']:
                errors.append('Redemption Code Invalid')
        else:
            errors.append('Redemption Code Invalid')

        if errors:
            return errors

        # once everything is validated, the user is able to enter the code in. It creates a new line in the db
        # if not errors:
            # create new data in table
            # new_redemption_code = self.create{
            #     from_badgeid = post_data['from_badgeid'],
            #     redemption_code = post_data['redemption_code'],
            # }
        return post_data['redemption_code']

    # def coin_status(self, clean_data, coin_to_give, post_data):
    #     errors = []
    #     # Checks to see if there is enough coins to share with other agents
    #     if clean_data['coin_to_give']== clean_data(post_data['coin_give']):
    #         errors.append("You do not have enough coins to give to others")
    #     # If there are any type of errors, it will return an error message
    #     else:
    #         return clean_data(post_data['coin_give'])
    #     if errors:
    #         return errors
    #     return

class coin_status(models.Model):
    agent_name = models.CharField(max_length=100)
    badge_id = models.IntegerField
    coin_give = models.IntegerField #How much you can give to another agent
    coin_received = models.IntegerField #How much was received by another agent
    coin_total = models.IntegerField #How much you have in your bank
    objects = coinManager()

class coin_transaction(models.Model):
    from_badgeid = models.IntegerField
    to_badgeid = models.IntegerField
    coin_to_give = models.IntegerField #How much coin you want to give to another agent
    redemption_code = models.CharField(max_length=12) #copy over from coin_status table
    note = models.TextField
    # created_at = models.DateTimeField(auto_now=True) #Issues with Date, need to work on this
    objects = coinManager()



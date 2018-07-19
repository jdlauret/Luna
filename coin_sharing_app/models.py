from __future__ import unicode_literals
# import os
# import re
# import json
# import django
from django.db import models
from Luna.models import DataWarehouse
from .utilities.user_list import *
from .utilities.coin_sharing_info import *
import random
import string

class coinManager(models.Manager):
    def random_string_generator(length=12):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

    # Validates the redemption code that the user enters in
    # def validate_redemption_code(self, clean_data, post_data):
    #     errors = []
    #     if len(self.filter(redemption_code=post_data['redemption_code'])) > 0:
    # #         checks the redemption code to other codes
    #         coin_transaction = self.filter(redemption_code = clean_data(post_data['redemption_code']))[0]
    #         if not post_data['redemption_code']:
    #             errors.append('Redemption Code Invalid')
    #     else:
    #         errors.append('Redemption Code Invalid')
    #
    #     if errors:
    #         return errors

        # once everything is validated, the user is able to enter the code in. It creates a new line in the db

        # return post_data['redemption_code']
    def insert_coin_transaction(self, FROM_BADGEID, TO_BADGEID, COIN_TO_GIVE, REDEMPTION_CODE, NOTE):
        query = "INSERT INTO coin_transaction(FROM_BADGEID, TO_BADGEID, COIN_TO_GIVE, REDEMPTION_CODE, NOTE)"

class coin_status(models.Model):
    agent_name = models.CharField(max_length=100)
    badge_id = models.IntegerField
    coin_give = models.IntegerField #How much you can give to another agent
    coin_received = models.IntegerField #How much was received by another agent
    coin_total = models.IntegerField #How much you have in your bank
    objects = coinManager()

class coin_transaction(models.Model):
    FROM_BADGEID = models.IntegerField
    TO_BADGEID = models.IntegerField
    COIN_TO_GIVE = models.IntegerField #How much coin you want to give to another agent
    REDEMPTION_CODE = models.CharField(max_length=12) #copy over from coin_status table
    NOTE = models.TextField
    # created_at = models.DateTimeField(auto_now=True) #Issues with Date, need to work on this
    objects = coinManager()



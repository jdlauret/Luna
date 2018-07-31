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

    # THIS IS A RANDOM CODE GENERATOR
    def random_string_generator(length=12):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

    # VALIDATES THE INFORMATION IN TRANSACTION WINDOW TO SEE IF ALL THE INFORMATION IS FILLED \
    #       ALSO CHECKS TO SEE IF THERE IS ENOUGH COINS TO SEE IF YOU CAN GIVE ANYONE COIN
    def validate_field (self, post_data):
        errors= []

        # todo first needs to find out the badgeid of person signed on
        # todo next it needs to filter out the table to only just the signed in person's info
        # todo next it needs to compare the coin_give to the coin_to_give info
        # todo once it is validated then it can input the new information to the transaction_coin table
        # todo updates the status_coin in the coin_give section

        # VALIDATES THE FIELD TO SEE IF THERE IS INFORMATION IN THE BOXES ON THE TRANSACTION PAGE
    #     if len(post_data['TO_BADGEID']) > 0 and len(post_data['COIN_TO_GIVE']) > 0 and len(post_data['NOTE']) > 0:
    #         pass
    #     else:
    #         errors.append('Cannot leave field blank')
    #         return errors
    #
    # #     VALIDATES THE BALANCE TO SEE IF THERE IS ENOUGH COIN TO GIVE TO SOMEONE ELSE ON TRANSACTION PAGE
    # #     needs to compare information between the user who is logged in and their balance
    # #     Then needs to call the COIN_TO_GIVE and compare that to what is found in the database
    #     if status_coin.COIN_GIVE >= post_data['COIN_TO_GIVE']:
    #         status_coin.COIN_GIVE = status_coin.COIN_GIVE - post_data['COIN_TO_GIVE']
    #     else:
    #         errors.append('Not enough coins to share')

    # Validates the redemption code that the user enters in the agent_view.html
    def validate_code(self, post_data):
        errors = []
    #   todo finds the badgeid of person signed in
    # todo then it looks through transaction in to_badgeid
    # todo then it compares the redemption code to the new redemption code entered
    # todo then it pulls up the badge id of person signed-in in the status_coin
    # todo replaces the coin_total
    # # checks the redemption code to other codes
    #     if len(transaction_coin.objects.filter(REDEMPTION_CODE = post_data['REDEMPTION_CODE'])) > 0:
    #         print('Need to validate if the code is correct')
    #     #     call the current user signed in and compare that to the redemption code that the user receving
    #         if transaction_coin.REDEMPTION_CODE ==  post_data['REDEMPTION_CODE']:
    #             print('Transaction Code Accepted')
    #
    #     else:
    #         errors.append('Redemption Code Invalid')
    #         return errors

        # once everything is validated, the user is able to enter the code in. It creates a new line in the db

    # THIS SECTION CREATES THE TABLE DATA
    @classmethod
    def create_transaction(self, clean_data, badge_id, TO_BADGEID, COIN_TO_GIVE, REDEMPTION_CODE, NOTE):
        # todo validate the information being inserted into table
        FROM_BADGEID = self.create(FROM_BADGEID=badge_id)
        TO_BADGEID = self.create(TO_BADGEID=TO_BADGEID)
        COIN_TO_GIVE = self.create(COIN_TO_GIVE=COIN_TO_GIVE)
        REDEMPTION_CODE = self.create(REDEMPTION_CODE=REDEMPTION_CODE)
        NOTE = self.create(NOTE=NOTE)

    @classmethod
    def create_status (self, AGENT_NAME, BADGE_ID, COIN_GIVE, COIN_RECEIVED, COIN_TOTAL):
        AGENT_NAME = self.create(AGENT_NAME=AGENT_NAME)
        BADGE_ID = self.create(BADGE_ID=BADGE_ID)
        COIN_GIVE = self.create(COIN_GIVE=COIN_GIVE)
        COIN_RECEIVED = self.create(COIN_RECEIVED=COIN_RECEIVED)
        COIN_TOTAL = self.create(COIN_TOTAL=COIN_TOTAL)

    # THIS SECTION EDITS THE TABLE
    @classmethod
    def edit_transaction(self, FROM_BADGEID, TO_BADGEID, COIN_TO_GIVE, REDEMPTION_CODE, NOTE):
        transaction_coin.save(FROM_BADGEID, TO_BADGEID, COIN_TO_GIVE, REDEMPTION_CODE, NOTE)

    @classmethod
    def edit_status(self, AGENT_NAME, BADGE_ID, COIN_GIVE, COIN_RECEIVED, COIN_TOTAL):
        status_coin.save(AGENT_NAME, BADGE_ID, COIN_GIVE, COIN_RECEIVED, COIN_TOTAL)


# COIN SHARING DATABASE
# THIS TABLE IS A VIEW OF ALL THE AGENTS AND HOW MANY COINS THEY HAVE
class status_coin(models.Model):
    AGENT_NAME = models.CharField(max_length=100)
    BADGE_ID = models.IntegerField()
    # todo create a time limit on the coin_give, clears out every quarter
    COIN_GIVE = models.IntegerField() #How much you can give to another agent
    COIN_RECEIVED = models.IntegerField() #How much was received by another agent
    COIN_TOTAL = models.IntegerField() #How much you have in your bank
    CREATED_AT = models.DateTimeField(default=django.utils.timezone.now)
    EDITED_AT = models.DateTimeField(default=django.utils.timezone.now)
    objects = coinManager()

# THIS TABLE IS A VIEW OF ALL THE TRANSACTIONS OF THE AGENTS
class transaction_coin(models.Model):
    FROM_BADGEID = models.IntegerField()
    TO_BADGEID = models.IntegerField()
    COIN_TO_GIVE = models.IntegerField() #How much coin you want to give to another agent
    REDEMPTION_CODE = models.CharField(max_length=12) #copy over from coin_status table
    NOTE = models.TextField()
    CREATED_AT = models.DateTimeField(default=django.utils.timezone.now)

    objects = coinManager()



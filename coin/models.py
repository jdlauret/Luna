from __future__ import unicode_literals
import os
import json
import datetime as dt
from django.db import models


class coinManager(models.Manager):
    # DEALS WITH THE TRANSACTION PAGE
    @classmethod
    def validate_transaction(self, post_data):
        errors = []
        agent_info = employee_id.objects.get(badgeid=int(post_data['benefactor'])) #GRABS BENEFACTOR FROM POST_DATA INPUTS INTO EMPLOYEE_ID
        rec_ID = employee_id.objects.get(badgeid=int(post_data['recipient']))  #GRABS RECIPIENT FROM POST_DATA INPUTS INTO EMPLOYEE_ID
        coin_given=int(float(post_data['award']))
        if coin_given > agent_info.allotment:
            errors.append('Exceeds Sharing Balance')
            return errors
        # BENEFACTOR AND RECIPIENT CANNOT BE THE SAME
        else:
            if agent_info.badgeid == rec_ID.badgeid:
                errors.append('Please Share')
                return errors
            else:
                agent_info.allotment -= coin_given
                agent_info.save()
                temp = transaction(
                    benefactor_name = agent_info.name,
                    benefactor= agent_info.badgeid,
                    recipient=rec_ID.badgeid,
                    recipient_name=rec_ID.name,
                    award=coin_given,
                    note=post_data['note'],
                    anonymous=int(post_data['anonymous']),
                )
                temp.save()

    # OVERLORD CONTROL PANEL
    @classmethod
    def employee_action(self, post_data):
        errors = []
        if post_data['allotment'] == "":
            errors.append('Cannot enter in blank Sharing Balance')
            return errors
        elif int(post_data['allotment']) < 0:
            errors.append('Cannot enter in a negative number')
            return errors
        else:
            e = employee_id.objects.get(id=int(post_data['id']))
            e.allotment = int(post_data['allotment'])
            e.edited = dt.datetime.now()
            e.save()

    # ADDS TRANSACTION FROM OVERLORD PAGE
    @classmethod
    def ol_transaction(self, post_data):
        errors = []
        agent_info = employee_id.objects.get(badgeid=int(post_data['id']))  # get's agent info from employee_id
        rec_ID = employee_id.objects.get(badgeid=int(post_data['recipient']))
        coin_given = int(float(post_data['award']))

        # SAVES THE TRANSACTION THAT WAS CREATED BY OVERLORD
        temp=transaction(
            benefactor_name = agent_info.name,
            benefactor=post_data['id'],
            recipient=post_data['recipient'],
            recipient_name=rec_ID.name,
            award=post_data['award'],
            note=post_data['note'],
            anonymous=post_data['anonymous'],
        )
        temp.save()

        # DEDUCTS THE TRANSACTION ALLOTMENT FROM WHO CREATED THE TRANSACTION
        agent_info.allotment -= coin_given
        agent_info.save()

# COIN SHARING DATABASE~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# THIS TABLE IS A VIEW OF ALL THE AGENTS AND HOW MANY COIN THEY HAVE
class employee_id(models.Model):
    name = models.CharField(max_length=100)
    badgeid = models.IntegerField()
    allotment = models.IntegerField()  # How much you can give to another agent
    # to_accept = models.IntegerField()  # Transition coin, agent can accept the coin or not
    edited = models.DateTimeField(auto_now_add=True, blank=True)
    terminated = models.IntegerField(default=0)
    objects = coinManager()


# THIS TABLE IS A VIEW OF ALL THE TRANSACTIONS OF THE AGENTS
class transaction (models.Model):
    anonymous = models.IntegerField(default=0)
    bad_comment = models.IntegerField(default=0)
    # accept = models.BooleanField(default=False)
    benefactor = models.IntegerField()
    benefactor_name = models.CharField(max_length=100, default='To Be Filled in Later')
    recipient = models.IntegerField()
    recipient_name = models.CharField(max_length=100, default='To Be Filled in Later')
    award = models.IntegerField()  # How much coin you want to give to another agent
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True) #('US/Mountain'))
    redeemed = models.IntegerField(default=0)
    objects = coinManager()

class leaders (models.Model):
    name = models.CharField(max_length=100, default='To Be Filled in Later')
    badge_num = models.IntegerField()
    amount = models.IntegerField()
    objects = coinManager()
    created = models.DateTimeField(auto_now_add=True, blank=True)
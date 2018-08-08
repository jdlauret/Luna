from __future__ import unicode_literals
import os
import django
import json
import datetime as dt
from django.db import models
from django.utils import timezone

MAIN_DIR = os.path.dirname(os.path.realpath(__file__))
LOGS_DIR = os.path.join(MAIN_DIR, 'logs')


class coinManager(models.Manager):

    @classmethod
    def validate_transaction(self, post_data):
        errors = []
        # VALIDATES THE FIELD TO SEE IF THERE IS INFORMATION IN THE BOXES ON THE TRANSACTION PAGE
        # if len(badge_id) <= 0 or len(post_data['gave']) <= 0 or len(post_data['note']) <= 0:
        #     errors.append('Cannot leave field blank')
        #     return errors
        # else:
        the_ID = int(post_data['badge_id'])  # grabbing badge id from post_data
        agent_info = employee_id.objects.get(badgeid=the_ID)  # get's agent info from employee_id
        coin_given = int(post_data['award'])

        if coin_given > agent_info.allotment:
            errors.append('Cannot give more than allotment')
            return errors
        # deducts the amount from the agent who gave the coin to someone else
        else:
            agent_info.allotment -= coin_given
            agent_info.save()
            # adds the coin to the yet to be accept
            # to_id = int(post_data['to_id'])
            # to_badgeid = employee_id.objects.get(badge_id=to_id)
            # to_badgeid.to_accept += post_data['gave']
            temp = transaction(
                benefactor=post_data['benefactor'],
                recipient=post_data['recipient'],
                award=post_data['award'],
                note=post_data['note'],
                anonymous=post_data['anonymous'],
            )
            temp.save()

    @classmethod
    def time_limit(self):
        log_file_path = os.path.join(LOGS_DIR, 'date_resets.json')
        with open(log_file_path) as infile:
            log_file = json.load(infile)

        months = [
            1,
            4,
            7,
            10
        ]
        now = dt.date.today()
        standard = 75

        if now.month in months and now.day == 1:
            if str(now) not in log_file.keys():
                log_file[str(now)] = False

            if not log_file[str(now)]:
                # special badges that are given extra allotment
                sb1 = [120690]
                sb1_coin = 10000000 + standard
                sb2 = [53931,
                       207208,
                       120220,
                       200023,
                       104550]
                sb2_coin = 600 + standard
                sb3 = [119945]
                sb3_coin = 500 + standard
                sb4 = [200360,
                       123014,
                       62836,
                       209349]
                sb4_coin = 300 + standard
                sb5 = [103390,
                       119688,
                       201640,
                       201662,
                       201737,
                       201738,
                       201767,
                       201846,
                       201869,
                       206321,
                       206415,
                       206417,
                       206470,
                       123645,
                       206530,
                       206563]
                sb5_coin = 150 + standard
                sb6 = [107938]
                sb6_coin = 100 + standard
                sb7 = [106452,
                       209196,
                       206679,
                       95347,
                       205821,
                       206225,
                       209272,
                       209409,
                       209144]
                sb7_coin = 75 + standard
                sb8 = [206225]
                sb8_coin = 5 + standard

                if employee_id.badgeid == sb1:
                    employee_id.objects.update(allotment=sb1_coin)
                elif employee_id.badgeid == sb2:
                    employee_id.objects.update(allotment=sb2_coin)
                elif employee_id.badgeid == sb3:
                    employee_id.objects.update(allotment=sb3_coin)
                elif employee_id.badgeid == sb4:
                    employee_id.objects.update(allotment=sb4_coin)
                elif employee_id.badgeid == sb5:
                    employee_id.objects.update(allotment=sb5_coin)
                elif employee_id.badgeid == sb6:
                    employee_id.objects.update(allotment=sb6_coin)
                elif employee_id.badgeid == sb7:
                    employee_id.objects.update(allotment=sb7_coin)
                elif employee_id.badgeid == sb8:
                    employee_id.objects.update(allotment=sb8_coin)
                else:
                    employee_id.objects.update(allotment=standard)

                log_file[str(now)] = True
                with open(log_file_path, 'w') as outfile:
                    json.dump(outfile, log_file, indent=4, sort_keys=True)


# COIN SHARING DATABASE
# THIS TABLE IS A VIEW OF ALL THE AGENTS AND HOW MANY COINS THEY HAVE
class employee_id (models.Model):
    name = models.CharField(max_length=100)
    badgeid = models.IntegerField()
    allotment = models.IntegerField()  # How much you can give to another agent
    # to_accept = models.IntegerField()  # Transition coin, agent can accept the coin or not
    edited = models.DateTimeField(default=django.utils.timezone.now)
    objects = coinManager()



# THIS TABLE IS A VIEW OF ALL THE TRANSACTIONS OF THE AGENTS
class transaction(models.Model):
    anonymous = models.IntegerField(default=0)
    bad_comment = models.IntegerField(default=0)
    # accept = models.BooleanField(default=False)
    benefactor = models.IntegerField()
    recipient = models.IntegerField()
    award = models.IntegerField()  # How much coin you want to give to another agent
    note = models.TextField()
    created_at = models.DateTimeField(default=django.utils.timezone.now)
    objects = coinManager()



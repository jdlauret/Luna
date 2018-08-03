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
        from_badgeid = post_data['badge_id']  # grabbing badge id from post_data
        agent_info = status.objects.get(
            badgeid=from_badgeid)  # get's agent info from status
        coin_given = int(post_data['gave'])

        if coin_given > agent_info.give:
            errors.append('Cannot give more than allotment')
            return errors
        # deducts the amount from the agent who gave the coin to someone else
        else:
            agent_info.give -= coin_given
            agent_info.save()
            # adds the coin to the yet to be accept
            to_id = post_data['to_id']
            to_badgeid = status.objects.get(badge_id=to_id)
            to_badgeid.to_accept += post_data['gave']
            temp = transaction(
                from_id=post_data['from_id'],
                to_id=post_data['to_id'],
                gave=post_data['gave'],
                note=post_data['note'],
                anonymous=post_data['anonymous'],
            )
            temp.save()

    @classmethod
    def filter_from(self, post_data):
        id = post_data['badge_id']
        transaction.objects.get(from_id=id)
    #     todo if anonymous is true, to_id is hidden
    #     todo if bad_comment is true, comment is hidden

    @classmethod
    def filter_to(self, post_data):
        id = post_data['badge_id']
        transaction.objects.get(to_id=id)
        #     todo if anonymous is true, to_id is hidden
        #     todo if bad_comment is true, comment is hidden

    @classmethod
    def filter_all(self, post_data):
        id = post_data['badge_id']
        transaction.objects.get(from_id=id)
        transaction.objects.get(to_id=id)
        #     todo if anonymous is true, to_id is hidden
        #     todo if bad_comment is true, comment is hidden

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

                if status.badgeid == sb1:
                    status.objects.update(give=sb1_coin)
                elif status.badgeid == sb2:
                    status.objects.update(give=sb2_coin)
                elif status.badgeid == sb3:
                    status.objects.update(give=sb3_coin)
                elif status.badgeid == sb4:
                    status.objects.update(give=sb4_coin)
                elif status.badgeid == sb5:
                    status.objects.update(give=sb5_coin)
                elif status.badgeid == sb6:
                    status.objects.update(give=sb6_coin)
                elif status.badgeid == sb7:
                    status.objects.update(give=sb7_coin)
                elif status.badgeid == sb8:
                    status.objects.update(give=sb8_coin)
                else:
                    status.objects.update(give=standard)

                log_file[str(now)] = True
                with open(log_file_path, 'w') as outfile:
                    json.dump(outfile, log_file, indent=4, sort_keys=True)


# COIN SHARING DATABASE
# THIS TABLE IS A VIEW OF ALL THE AGENTS AND HOW MANY COINS THEY HAVE
class status(models.Model):
    name = models.CharField(max_length=100)
    badgeid = models.IntegerField()
    give = models.IntegerField()  # How much you can give to another agent
    to_accept = models.IntegerField()  # Transition coin, agent can accept the coin or not
    edited = models.DateTimeField(default=django.utils.timezone.now)
    objects = coinManager()




# THIS TABLE IS A VIEW OF ALL THE TRANSACTIONS OF THE AGENTS
class transaction(models.Model):
    anonymous = models.BooleanField(default=False)
    bad_comment = models.BooleanField(default=False)
    accept = models.BooleanField(default=False)
    from_id = models.IntegerField()
    to_id = models.IntegerField()
    gave = models.IntegerField()  # How much coin you want to give to another agent
    note = models.TextField()
    created_at = models.DateTimeField(default=django.utils.timezone.now)
    objects = coinManager()



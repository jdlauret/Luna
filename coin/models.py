from __future__ import unicode_literals
import os
import json
import datetime as dt
from django.db import models

MAIN_DIR = os.path.dirname(os.path.realpath(__file__))
LOGS_DIR = os.path.join(MAIN_DIR, 'logs')


class coinManager(models.Manager):

    @classmethod
    def validate_transaction(self, post_data):
        errors = []
        agent_info = employee_id.objects.get(badgeid=int(post_data['badge_id']))  # get's agent info from employee_id
        rec_ID = employee_id.objects.get(badgeid=int(post_data['recipient']))
        coin_given=int(float(post_data['award']))
        if coin_given > agent_info.allotment:
            errors.append('Cannot give more than Sharing Balance')
            return errors
        # deducts the amount from the agent who gave the coin to someone else
        else:
            if agent_info.badgeid == rec_ID.badgeid:
                errors.append('You cannot give coins to yourself')
                return errors
            else:

                agent_info.allotment -= coin_given
                agent_info.save()
                # adds the coin to the yet to be accept
                # to_id = int(post_data['to_id'])
                # to_badgeid = employee_id.objects.get(badge_id=to_id)
                # to_badgeid.to_accept += post_data['gave']
                temp = transaction(
                    benefactor_name = agent_info.name,
                    benefactor=post_data['badge_id'],
                    recipient=post_data['recipient'],
                    recipient_name=rec_ID.name,
                    award=post_data['award'],
                    note=post_data['note'],
                    anonymous=post_data['anonymous'],
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

    # todo new employees are created
    # have this access once a week
    # go through hire date and add them to employee_id

    # @classmethod
    # def create_id(self):
    #     log_file_path = os.path.join(LOGS_DIR, 'created_id.json')
    #     with open(log_file_path) as infile:
    #         log_file = json.load(infile)
    #
    # #     code
    #     now = dt.date.today()
    #
    #
    #     log_file[str(now)] = True
    #     with open(log_file_path, 'w') as outfile:
    #         json.dump(outfile, log_file, indent=4, sort_keys=True)

    # CONTROLS WHO GETS WHAT ALLOTMENT
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

                employee_id.save()

                log_file[str(now)] = True
                with open(log_file_path, 'w') as outfile:
                    json.dump(outfile, log_file, indent=4, sort_keys=True)


# COIN SHARING DATABASE
# THIS TABLE IS A VIEW OF ALL THE AGENTS AND HOW MANY COINS THEY HAVE
class employee_id(models.Model):
    name = models.CharField(max_length=100)
    badgeid = models.IntegerField()
    allotment = models.IntegerField()  # How much you can give to another agent
    # to_accept = models.IntegerField()  # Transition coin, agent can accept the coin or not
    edited = models.DateTimeField(auto_now_add=True, blank=True)
        # default=django.utils.timezone.now(), blank=True)#('US/Mountain'))
    objects = coinManager()


# THIS TABLE IS A VIEW OF ALL THE TRANSACTIONS OF THE AGENTS
class transaction(models.Model):
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
    objects = coinManager()

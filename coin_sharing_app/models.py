from django.db import models

class coin_status(models.Model):
    agent_name = models.CharField(max_length=100)
    badge_id = models.IntegerField
    coin_given = models.IntegerField
    coin_received = models.IntegerField
    coin_total = models.IntegerField

class coin_transaction(models.Model):
    # from badge id
    # to badge id
    coin_to_give = models.IntegerField
    redemption_code = models.CharField(max_length=12)
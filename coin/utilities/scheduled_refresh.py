import os
import json
import datetime as dt

from coin.models import employee_id, leaders

MAIN_DIR = os.path.dirname(os.path.realpath(__file__))
LOGS_DIR = os.path.join(MAIN_DIR, 'logs')

# SCHEDULED REFRESH OF THE COINS, EMPLOYEES AND LEADERSHIP ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def scheduled_refresh():
    log_file_path = os.path.join(LOGS_DIR, 'date_resets.json')
    with open(log_file_path) as infile:
        log_file = json.load(infile)

    months = [1, 4, 7, 10]
    monthly = [2, 3, 5, 6, 8, 9, 11, 12]

    now = dt.date.today()
    standard = 250

    # CHECKS THE DATE AND SEES IF IT'S THE QUARTER OR NOT, CLEARS EVERYTHING OUT AND STARTS REFRESH
    if now.month in months and now.day == 1:
        if str(now) not in log_file.keys():
            log_file[str(now)] = False

        if not log_file[str(now)]:
            if employee_id.badgeid == leaders.badge_num:
                new_allotment = employee_id.objects.get(badgeid=leaders.badge_num)
                new_allotment.allotment = leaders.amount
                new_allotment.save()

            else:
                new_allotment2 = employee_id.objects.get(badgeid=leaders.badge_num)
                if new_allotment2.terminated ==0:
                    new_allotment2.allotment = standard
                    new_allotment2.save()
                else:
                    new_allotment2.allotment = 0
                    new_allotment2.save()

            print('saved quarterly')
            # employee_id.save()

            log_file[str(now)] = True
            with open(log_file_path, 'w') as outfile:
                json.dump(outfile, log_file, indent=4, sort_keys=True)

    # CHECKS IF THE DATE IS THE BEGINNING OF MONTH AND ADDS COIN TO WHAT THEY ALREADY HAVE
    elif now.month in monthly and now.day == 1:
        if str(now) not in log_file.keys():
            log_file[str(now)] = False
        if not log_file[str(now)]:
            total = employee_id.objects.get(badgeid=leaders.badge_num)

            if employee_id.badgeid == leaders.badge_num:
                new_allotment = employee_id.objects.get(badgeid=leaders.badge_num)
                new_allotment.allotment = leaders.amount + total.allotment
                new_allotment.save()

            else:
                new_allotment2 = employee_id.objects.get(badgeid=leaders.badge_num)
                if new_allotment2.terminated == 0:
                    new_allotment2.allotment = standard + total.allotment
                    new_allotment2.save()
                else:
                    new_allotment2.allotment = 0
                    new_allotment2.save()

            print('saved monthly')
            # employee_id.save()

            log_file[str(now)] = True
            with open(log_file_path, 'w') as outfile:
                json.dump(outfile, log_file, indent=4, sort_keys=True)
    return 'Success with Scheduled refresh'
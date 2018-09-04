import os
# import json
import datetime as dt
from Luna.models import DataWarehouse
from coin.models import employee_id
#
# MAIN_DIR = os.path.dirname(os.path.realpath(__file__))
# CREATED_DIR = os.path.join(MAIN_DIR, 'logs')

main_dir = os.getcwd()
coin_dir = os.path.join(main_dir, 'coin')
utilities_dir = os.path.join(coin_dir, 'utilities')

def new_user():
    # log_file_path = os.path.join(CREATED_DIR, 'created_id.json')
    # with open(log_file_path) as infile:
    #     log_file = json.load(infile)
    #
    # now = dt.datetime.now().strftime('%Y-%m-%d')
    agent_list = {}

    dw = DataWarehouse('admin')

    with open(os.path.join(utilities_dir, 'create_new_user.sql'), 'r') as file:
        sql = file.read()
    dw.query_results(sql, bindvars=None)

    try:
        result = dw.results
        column = dw.column_names
        # print('Column: ', column)

        if len(result) == 0:
            agent_list['no_new_employees'] = 'No New Employees'
            return agent_list

    except Exception as e:
        agent_list['error'] = e
        return agent_list
    #
    for j, value in enumerate(result):
        agent_list[value[0]] = value[1]

    # log_json = False

    # key-full name, value- badge id
    for key, value in agent_list.items():
        old_employee = employee_id.objects.filter(badgeid=value)
        if not old_employee:
            employee_id.objects.create(name=key, badgeid=value, allotment=250, edited=dt.datetime.now()).save()
            # log_json = True
            print("Created New ID")
    #
    # if log_json:
    #     log_file[now] = True
    #     with open(log_file_path, 'w') as outfile:
    #         json.dump(outfile, log_file, indent=4, sort_keys=True)
    return 'Success in running Create new user'
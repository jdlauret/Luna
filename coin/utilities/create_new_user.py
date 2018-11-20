import os
import datetime as dt
from BI.data_warehouse.connector import Snowflake
from BI.luna_db.connector import Postgres
from coin.models import employee_id

main_dir = os.getcwd()
coin_dir = os.path.join(main_dir, 'coin')
utilities_dir = os.path.join(coin_dir, 'utilities')

DB = Snowflake()
DB.set_user('MACK_DAMAVANDI')


def new_user():
    DB = Snowflake()
    DB.set_user('MACK_DAMAVANDI')
    luna = Postgres()
    luna.set_user('POSTGRES_HOST')

    # log_file_path = os.path.join(CREATED_DIR, 'created_id.json')
    # with open(log_file_path) as infile:
    #     log_file = json.load(infile)
    #
    # now = dt.datetime.now().strftime('%Y-%m-%d')
    agent_list = {}

    try:
        DB.open_connection()
        with open(os.path.join(utilities_dir, 'create_new_user.sql'), 'r') as file:
            sql = file.read()
        DB.execute_query(sql, bindvars=None)
        result = DB.query_results

        if len(result) == 0:
            agent_list['no_new_employees'] = 'No New Employees'
            return agent_list

    except Exception as e:
        agent_list['error'] = e
        return agent_list

    finally:
        DB.close_connection()

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
import os
from BI.data_warehouse.connector import Snowflake
from coin.models import employee_id

# MAIN_DIR = os.path.dirname(os.path.realpath(__file__))
# CREATED_DIR = os.path.join(MAIN_DIR, 'logs')

main_dir = os.getcwd()
coin_dir = os.path.join(main_dir, 'coin')
utilities_dir = os.path.join(coin_dir, 'utilities')

DB = Snowflake()
DB.set_user('MACK_DAMAVANDI')

def terminated_user():
    # log_file_path = os.path.join(CREATED_DIR, 'date_terminated.json')
    # with open(log_file_path) as infile:
    #     log_file = json.load(infile)

    # now = dt.datetime.now().strftime('%Y-%m-%d')
    agent_list = {}

    try:
        DB.open_connection()
        with open(os.path.join(utilities_dir, 'termination_list.sql'), 'r') as file:
            sql = file.read()
        DB.execute_query(sql, bindvars=None)
        result = DB.query_results

        if len(result) == 0:
            agent_list['termination'] = 'No Terminations'
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
        try:
            old_employee = employee_id.objects.get(badgeid=value)
            if old_employee == 0:
                if old_employee:  # True
                    old_employee.terminated = 1
                    old_employee.save()
        except Exception as e:
            pass

        # log_json = True
    # if log_json:
    #     log_file[now] = True
    #     with open(log_file_path, 'w') as outfile:
    #         json.dump(log_file, outfile, indent=4, sort_keys=True)
    return 'Success in changing status of User'

import os
from BI.data_warehouse.connector import Snowflake
# from BI.luna_db.connector import Postgres
import datetime as dt
from coin.models import employee_id


main_dir = os.getcwd()
coin_dir = os.path.join(main_dir, 'coin')
utilities_dir = os.path.join(coin_dir, 'utilities')

DB = Snowflake()
DB.set_user('MACK_DAMAVANDI')

def terminated_user():
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

    # key-full name, value- badge id
    for key, value in agent_list.items():
        try:
            old_employee = employee_id.objects.get(badgeid=value)
            if old_employee == 0:
                if old_employee:  # True
                    old_employee.terminated = 1
                    old_employee.edited = dt.datetime.now()
                    old_employee.save()
        except Exception as e:
            pass
    return agent_list

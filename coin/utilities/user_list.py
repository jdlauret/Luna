import os
from Luna.models import DataWarehouse
from models import SnowFlakeDW, SnowflakeConsole

main_dir = os.getcwd()
coin_dir = os.path.join(main_dir, 'coin')
utilities_dir = os.path.join(coin_dir, 'utilities')

DB = SnowFlakeDW()
DB.set_user('MACK_DAMAVANDI')

def user_list():
    agent_list = {}

    try:
        DB.open_connection()
        DW = SnowflakeConsole(DB)
        with open(os.path.join(utilities_dir, 'user_list.sql'), 'r') as file:
            sql = file.read()
        DW.execute_query(sql, bindvars=None)
        result = DW.query_results
        column = DW.column_names

        if len(result) == 0:
            agent_list['error'] = 'Error'
            return agent_list

    except Exception as e:
        agent_list['error'] = e
        return agent_list

    finally:
        DB.close_connection()
    #
    for j, value in enumerate(result):
        # print(value)
        agent_list[value[0]] = value[1]
    return agent_list
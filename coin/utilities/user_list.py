import os
from BI.data_warehouse.connector import Snowflake

main_dir = os.getcwd()
coin_dir = os.path.join(main_dir, 'coin')
utilities_dir = os.path.join(coin_dir, 'utilities')

DB = Snowflake()
DB.set_user('MACK_DAMAVANDI')

def user_list():
    agent_list = {}

    try:
        DB.open_connection()
        with open(os.path.join(utilities_dir, 'user_list.sql'), 'r') as file:
            sql = file.read()
        DB.execute_query(sql, bindvars=None)
        result = DB.query_results

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
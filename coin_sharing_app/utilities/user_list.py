import os
from Luna.models import DataWarehouse

main_dir = os.getcwd()
coin_dir = os.path.join(main_dir, 'coin_sharing_app')
utilities_dir = os.path.join(coin_dir, 'utilities')


def user_list():
    agent_list = {
    }
    dw = DataWarehouse('admin')

    with open(os.path.join(utilities_dir, 'user_list.sql'), 'r') as file:
        sql = file.read()
    dw.query_results(sql, bindvars=None)

    try:
        result = dw.results
        column = dw.column_names
        # print('Column: ', column)

        if len(result) == 0:
            agent_list['error'] = 'Error'
            return agent_list

    except Exception as e:
        agent_list['error'] = e
        return agent_list
    #
    for j, value in enumerate(result):
        # print(value)
        agent_list[value[0]] = value[1]
    return agent_list
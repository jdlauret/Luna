import os
from Luna.models import DataWarehouse

main_dir = os.getcwd()
coin_dir = os.path.join(main_dir, 'coin')
utilities_dir = os.path.join(coin_dir, 'utilities')


def agent_name():
    user = {}
    dw = DataWarehouse('admin')
    with open(os.path.join(utilities_dir, 'agent_name.sql'), 'r') as file:
        sql = file.read()
        sql = sql.split(';')
    # bindvars = {'badge_id': badge_id}
    # bindvars=bindvars
    try:
        dw.query_results(sql[0])
        account_info = dw.results[0]
        if len(account_info) == 0:
            user['error'] = 'Error'
            return user

    except Exception as e:
        user['error'] = e
        return user

    user['account_info'] = account_info
    return user


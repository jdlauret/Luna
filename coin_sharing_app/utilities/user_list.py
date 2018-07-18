import os
from Luna.models import DataWarehouse

main_dir = os.getcwd()
coin_dir = os.path.join(main_dir, 'coin_sharing_app')
utilities_dir = os.path.join(coin_dir, 'utilities')


def user_list():
    user_list = {
        'list_of_user': {}
    }
    dw = DataWarehouse('admin')

    with open(os.path.join(utilities_dir, 'user_list.sql'), 'r') as file:
        sql = file.read()
    dw.query_results(sql, bindvars=None)

    try:
        result = dw.results

        if len(result) == 0:
            user_list['error'] = 'Error'
            return list

    except Exception as e:
        user_list['error'] = e
        return user_list

    user_list['list_of_user'] = result
    return user_list
import os
from Luna.models import DataWarehouse

main_dir = os.getcwd()
coin_dir = os.path.join(main_dir, 'coin_sharing_app')
utilities_dir = os.path.join(coin_dir, 'utilities')


def coin_sharing(work_email_address):
    user_info = {
        'account_info': {}
    }
    dw = DataWarehouse('admin')
    with open(os.path.join(utilities_dir, 'coin_sharing_info.sql'), 'r') as file:
        sql = file.read()
        sql = sql.split(';')
    bindvars = {'work_email_address': work_email_address}

    try:
        dw.query_results(sql[0], bindvars=bindvars)
        account_info = dw.results[0]
        if len(account_info) == 0:
            user_info['error'] = 'Error'
            return user_info

    except Exception as e:
        user_info['error'] = e
        print('user info error: ', user_info['error'])
        print('user info: ', user_info)
        return user_info

    user_info['account_info'] = account_info
    return user_info

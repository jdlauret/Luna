import os
from datetime import date, timedelta
from models import SnowFlakeDW, SnowflakeConsole

main_dir = os.getcwd()
luna_dir = os.path.join(main_dir, 'Luna')
utilities_dir = os.path.join(luna_dir, 'utilities')

DB = SnowFlakeDW()
DB.set_user('MACK_DAMAVANDI')


def work_order (servicenum):
    install_notes = {
        'account_info': {},
    }

    if 'S-' in servicenum.upper():
        servicenum = servicenum.upper().replace('S-','')

    try:
        DB.open_connection()
        DW = SnowflakeConsole(DB)
        with open(os.path.join(utilities_dir, 'work_order.sql'), 'r') as file:
            sql = file.read()
        sql = sql.split(';')
        DW.execute_query(sql[0].format(service_number = str(servicenum)))

        account_information = DW.query_results[0]

        if len(account_information) == 0:
            install_notes['error'] = '{} is not a valid service number.'.format(servicenum)
            return install_notes

    except Exception as e:
        install_notes['error'] = e
        return install_notes

    finally:
        DB.close_connection()

    install_notes['account_info'] = account_information

    return install_notes

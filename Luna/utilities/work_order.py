import os
from models import SnowFlakeDW, SnowflakeConsole

main_dir = os.getcwd()
luna_dir = os.path.join(main_dir, 'Luna')
utilities_dir = os.path.join(luna_dir, 'utilities')

DB = SnowFlakeDW()
DB.set_user('MACK_DAMAVANDI')


def work_order(servicenum):
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
        DW.execute_query(sql[0].format(service_number=str(servicenum)))
        account_information = DW.query_results[0]

        if len(account_information) == 0:
            install_notes['error'] = '{} is not a valid service number.'.format(servicenum)
            return install_notes

    except Exception as e:
        install_notes['error'] = 'Invalid Service Number'
        return install_notes

    try:
        DW.execute_query(sql[1].format(service_number=str(servicenum)))
        column = DW.query_columns
        info = DW.query_results[0]

    finally:
        DB.close_connection()

    install_notes['account_info'] = account_information
    install_notes['organization'] = info[0]
    install_notes['case_number'] = info[1]
    install_notes['roc_name'] = info[2]
    install_notes['is_post_pto'] = info[3]
    install_notes['service_number'] = info[4]
    install_notes['service_name'] = info[5]
    install_notes['system_size_actual_kw'] = info[6]
    install_notes['total_modules'] = info[7]
    install_notes['requested_modules_to_be_removed'] = info[8]
    install_notes['partial_or_complete'] = info[9]
    install_notes['tilt'] = info[10]
    install_notes['azimuth'] = info[11]
    install_notes['inverter'] = info[12]
    install_notes['racking_type'] = info[13]
    install_notes['module_manufacturer'] = info[14]
    install_notes['module_model'] = info[15]
    return install_notes

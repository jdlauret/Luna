import os
from models import SnowflakeConsole, SnowFlakeDW

main_dir = os.getcwd()
luna_dir = os.path.join(main_dir, 'Luna')
utilities_dir = os.path.join(luna_dir, 'utilities')

DB = SnowFlakeDW()
DB.set_user('MACK_DAMAVANDI')

def prepay_calc(servicenum):
    notes = {}

    if 'S-' in servicenum.upper():
        servicenum = servicenum.upper().replace('S-', '')

    try:
        DB.open_connection()
        DW = SnowflakeConsole(DB)
        with open(os.path.join(utilities_dir, 'buyout_calc.sql'), 'r') as file:
            sql = file.read()
        sql = sql.split(';')
    except Exception as e:
        notes['error'] = e
        return notes

    finally:
        DB.close_connection()

    DW.execute_query(sql[0].format(service_number = str(servicenum)))
    query = DW.query_results[0]


    return notes
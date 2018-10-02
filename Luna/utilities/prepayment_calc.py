import os
<<<<<<< HEAD
<<<<<<< Updated upstream
from datetime import datetime as dt
from models import SnowFlakeDW, SnowflakeConsole
=======
from models import SnowflakeConsole, SnowFlakeDW
>>>>>>> Stashed changes
=======
from datetime import datetime as dt
from models import SnowFlakeDW, SnowflakeConsole
>>>>>>> Buyout_PrepayCalc

main_dir = os.getcwd()
luna_dir = os.path.join(main_dir, 'Luna')
utilities_dir = os.path.join(luna_dir, 'utilities')

DB = SnowFlakeDW()
DB.set_user('MACK_DAMAVANDI')

def prepay_calc(servicenum):
    notes = {}

    if 'S-' in servicenum.upper():
<<<<<<< HEAD
<<<<<<< Updated upstream
        servicenum = servicenum.upper().replace('S-','')
=======
        servicenum = servicenum.upper().replace('S-', '')
>>>>>>> Stashed changes
=======
        servicenum = servicenum.upper().replace('S-','')
>>>>>>> Buyout_PrepayCalc

    try:
        DB.open_connection()
        DW = SnowflakeConsole(DB)
<<<<<<< HEAD
<<<<<<< Updated upstream
=======
>>>>>>> Buyout_PrepayCalc
        with open(os.path.join(utilities_dir, 'prepayment_calc.sql'), 'r') as file:
            sql = file.read()
        sql = sql.split(';')

        query = sql[0].format(service_number=str(servicenum))
        DW.execute_query(query)
        results = DW.query_results[0]

        if len(results) == 0:
            notes['error'] = '{} is not a valid service number.'.format(servicenum)
            return notes

<<<<<<< HEAD
=======
        with open(os.path.join(utilities_dir, 'buyout_calc.sql'), 'r') as file:
            sql = file.read()
        sql = sql.split(';')
>>>>>>> Stashed changes
=======
>>>>>>> Buyout_PrepayCalc
    except Exception as e:
        notes['error'] = e
        return notes

    finally:
        DB.close_connection()

<<<<<<< HEAD
<<<<<<< Updated upstream
=======
>>>>>>> Buyout_PrepayCalc
    for i, value in enumerate(results):
        notes[i] = value
    notes['remaining_contract'] = notes.pop(8)
    notes['current_contract'] = 240 - notes['remaining_contract']
    if notes['remaining_contract'] == None:
        notes['error'] = 'Cannot Calculate, no remaining contract date found'
        return notes
    else:
        notes['service_number'] = notes.pop(0)
        notes['escalator'] = notes.pop(1)
        notes['system_size'] = notes.pop(2)
        notes['sun_hours'] = notes.pop(3)
        notes['r_p_k'] = notes.pop(4)
        notes['start_billing'] = notes.pop(5)
        notes['start_billing'] = dt.strftime(notes['start_billing'], '%m/%d/%y')
        notes['record_type'] = notes.pop(6)
        notes['current_annual_usage'] = notes.pop(7)
        notes['contract_version'] = notes.pop(9)
    return notes
<<<<<<< HEAD
=======
    DW.execute_query(sql[0].format(service_number = str(servicenum)))
    query = DW.query_results[0]


    return notes
>>>>>>> Stashed changes
=======
>>>>>>> Buyout_PrepayCalc

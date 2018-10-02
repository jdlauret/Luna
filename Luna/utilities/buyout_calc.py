import os
<<<<<<< Updated upstream
from Luna.models import DataWarehouse
from Luna.models import buyout_calc_model
from models import SnowFlakeDW, SnowflakeConsole
=======
from models import SnowflakeConsole, SnowFlakeDW
from Luna.models import buyout_calc_model
>>>>>>> Stashed changes

main_dir = os.getcwd()
luna_dir = os.path.join(main_dir, 'Luna')
utilities_dir = os.path.join(luna_dir, 'utilities')

DB = SnowFlakeDW()
DB.set_user('MACK_DAMAVANDI')

def buyout_calc(servicenum):
    notes = {
        'account_info': {},
    }

<<<<<<< Updated upstream
    servicenum = servicenum.upper().replace('S-', '')
=======
    if 'S-' in servicenum.upper():
        servicenum = servicenum.upper().replace('S-', '')
>>>>>>> Stashed changes

    try:
        DB.open_connection()
        DW = SnowflakeConsole(DB)
        with open(os.path.join(utilities_dir, 'buyout_calc.sql'), 'r') as file:
            sql = file.read()
        sql = sql.split(';')
<<<<<<< Updated upstream

        query = sql[0].format(service_number=str(servicenum))
        DW.execute_query(sql[0],query)

=======
>>>>>>> Stashed changes
    except Exception as e:
        notes['error'] = e
        return notes

<<<<<<< Updated upstream
=======
    DW.execute_query(sql[0].format(service_number=str(servicenum)))
>>>>>>> Stashed changes
    account_information = DW.query_results[0]

    if len(account_information) == 0:
        notes['error'] = '{} is not a valid service number.'.format(servicenum)
        return notes

<<<<<<< Updated upstream
        notes['account_info'] = account_information
        for h, value in enumerate(account_information):
            notes[h] = value
        notes['name'] = notes.pop(1)
        notes['email'] = notes.pop(2)
        notes['address'] = notes.pop(3)
        notes['city'] = notes.pop(4)
        notes['state'] = notes.pop(5)
        notes['zipcode'] = notes.pop(6)

    try:
        query_2 = sql[1].format(service_number=str(servicenum))
        DW.execute_query(query_2)
        query_results = DW.query_results[0]

        if len(query_results) == 0:
            notes['error'] = '{} is not a valid service number.'.format(servicenum)
            return notes

=======
=======
>>>>>>> Stashed changes
    notes['account_info'] = account_information

    try:
        DW.execute_query(sql[1], format(service_number=str(servicenum)))
        query_results = DW.query_results[0]

<<<<<<< Updated upstream
>>>>>>> Stashed changes
    except Exception as e:
        notes['error'] = e
        return notes

    finally:
        DB.close_connection()

<<<<<<< Updated upstream
=======
=======
>>>>>>> Stashed changes
    if len(query_results) == 0:
        notes['error'] = '{} is not a valid service number.'.format(servicenum)
        return notes

<<<<<<< Updated upstream
>>>>>>> Stashed changes
    for i, value in enumerate(query_results):
        notes[i] = value

    notes['service_number'] = notes.pop(0)
    notes['remaining_contract'] = notes.pop(2)
    notes['actual_system_size'] = notes.pop(1)
<<<<<<< Updated upstream

    if notes['remaining_contract'] is None:
=======
    if notes['remaining_contract'] == None:
>>>>>>> Stashed changes
        notes['error'] = 'Cannot Calculate, no remaining contract date found'
        return notes
    else:
        months = 240 - notes['remaining_contract']
        notes['contract_year'] = int((months/12)+1)
        calculator = buyout_calc_model.objects.get(id=notes['contract_year'])
        notes['transfer'] = calculator.transfer_buyout
        notes['default'] = calculator.default_price
        notes['watts'] = int(notes['actual_system_size'] * 1000)
        notes['transfer_total'] = int(notes['transfer']) * int(notes['watts'])
        notes['default_total'] = int(notes['default']) * int(notes['watts'])
    return notes

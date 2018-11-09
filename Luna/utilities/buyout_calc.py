import os
from BI.data_warehouse.connector import Snowflake
from collections import namedtuple

main_dir = os.getcwd()
luna_dir = os.path.join(main_dir, 'Luna')
utilities_dir = os.path.join(luna_dir, 'utilities')

DB = Snowflake()
DB.set_user('MACK_DAMAVANDI')

unpacker = namedtuple(
    'results',
    'contract_type tax_rate taxable remaining_contract_term contract_year ' \
    'transfer_buyout_price default_price watts transfer_subtotal transfer_total_tax transfer_total default_subtotal ' \
    'default_tax default_total'
)

def buyout_calc(servicenum):
    notes = {}

    if 'S-' in servicenum.upper():
        servicenum = servicenum.upper().replace('S-', '')

    try:
        DB.open_connection()
        with open(os.path.join(utilities_dir, 'buyout_calc.sql'), 'r') as file:
            sql = file.read()
        sql = sql.split(';')
    except Exception as e:
        notes['error'] = e
        return notes

    DB.execute_query(sql[0].format(service_number=str(servicenum)))
    account_information = DB.query_results[0]

    if len(account_information) == 0:
        notes['error'] = '{} is not a valid service number.'.format(servicenum)
        return notes

    notes['account_info'] = account_information

    try:
        DB.execute_query(sql[1], bindvars=[str(servicenum)])
        query_results = DB.query_results[0]

    except Exception as e:
        notes['error'] = e
        return notes

    finally:
        DB.close_connection()

    if len(query_results) == 0:
        notes['error'] = '{} is not a valid service number.'.format(servicenum)
        return notes

    notes['results'] = unpacker._make(query_results)
    return notes

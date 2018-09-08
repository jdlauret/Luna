import os
from Luna.models import DataWarehouse

main_dir = os.getcwd()
luna_dir = os.path.join(main_dir, 'Luna')
utilities_dir = os.path.join(luna_dir, 'utilities')

def prepay_calc(servicenum):
    notes = {}
    dw = DataWarehouse('admin')
    with open(os.path.join(utilities_dir, 'buyout_calc.sql'), 'r') as file:
        sql = file.read()
    sql = sql.split(';')
    if 'S-' in servicenum.upper():
        servicenum = servicenum.upper().replace('S-', '')
    bindvars = {'serviceNum': servicenum}

    try:
        dw.query_results(sql[0], bindvars=bindvars)
        account_information = dw.results[0]

    except Exception as e:
        notes['error'] = e
        return notes

    return notes
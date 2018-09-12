import os
from Luna.models import DataWarehouse
from datetime import datetime as dt

main_dir = os.getcwd()
luna_dir = os.path.join(main_dir, 'Luna')
utilities_dir = os.path.join(luna_dir, 'utilities')

def prepay_calc(servicenum):
    notes = {}
    dw = DataWarehouse('admin')
    with open(os.path.join(utilities_dir, 'prepayment_calc.sql'), 'r') as file:
        sql = file.read()
    sql = sql.split(';')
    if 'S-' in servicenum.upper():
        servicenum = servicenum.upper().replace('S-', '')
    bindvars = {'serviceNum': servicenum}

    try:
        dw.query_results(sql[0], bindvars=bindvars)
        results = dw.results[0]

    except Exception as e:
        notes['error'] = e
        return notes
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

import os
# from datetime import date, timedelta
from Luna.models import DataWarehouse

main_dir = os.getcwd()
luna_dir = os.path.join(main_dir, 'Luna')
utilities_dir = os.path.join(luna_dir, 'utilities')


def notes_wizard (servicenum):

    results = {}

    dw = DataWarehouse('admin')

    with open(os.path.join(utilities_dir, 'RTS_notes_wizard.sql'),'r') as file:
        sql = file.read()

    if 'S-' in servicenum.upper():
        servicenum = servicenum.upper().replace('S-','')

    bindvars = {'serviceNum': servicenum}

    try:
        dw.query_results(sql, bindvars=bindvars)
    except Exception as e:
        results['error'] = e
        return results

    results['notes'] = dw.results

    if len(results['account']) == 0:
        results['error'] = '{} is not a valid service number.'.format(servicenum)
        return results

    bindvars.append({'serviceNum': servicenum})

    # try:
    #     dw.query_results(sql[1], bindvars=bindvars[1])
    # except Exception as e:
    #     results['error'] = e
    #     return results
    #
    # results['savings'] = dw.results
    #
    # if len(results['savings']) == 0:
    #     results['error'] = 'There was no Actual production ' \
    #                                  'found for service number {} in the date range {} ' \
    #                                  'to {}.'.format(servicenum, startdatestring, enddatestring)
    #     return results

    return results

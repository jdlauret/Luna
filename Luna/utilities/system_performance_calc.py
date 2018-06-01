import os
from datetime import date, timedelta
from Luna.models import DataWarehouse

main_dir = os.getcwd()
luna_dir = os.path.join(main_dir, 'Luna')
utilities_dir = os.path.join(luna_dir, 'utilities')


def system_performance(servicenum, startdate, enddate):

    if enddate < startdate:
        results = {'error': 'The start date you entered ({}) must come before the end date you entered ({}).'.format(startdate.strftime('%m/%d/%Y'), enddate.strftime('%m/%d/%Y'))}
        return results

    dw = DataWarehouse('admin')

    file = open(os.path.join(utilities_dir, 'system_performance_calc.sql'),'r')
    sql = file.read()
    file.close()

    sql = sql.split(';')

    if 'S-' in servicenum.upper():
        servicenum = servicenum.upper().replace('S-','')

    bindvars = [{'serviceNum': servicenum}]

    dw.query_results(sql[0], bindvars=bindvars[0])

    results = {'account': dw.results}

    if len(results['account']) == 0:
        results['error'] = '{} is not a valid service number.'.format(servicenum)
        return results
    elif startdate < results['account'][0][7].date():
        results['startdate'] = results['account'][0][7]
        startdatestring = results['startdate'].strftime('%m/%d/%Y')
    else:
        results['startdate'] = startdate
        startdatestring = results['startdate'].replace(day=1).strftime('%m/%d/%Y')


    if enddate >= date.today() and enddate < results['startdate'].date() + timedelta(14) and results['startdate'] == results['account'][0][7]:
        # enddatestring = (date.today().replace(day=1) - timedelta(1)).strftime('%m/%d/%Y')
        # results['enddate'] = date.today().replace(day=1) - timedelta(1)
        results['error'] = "The system has not been PTO'd for at least two weeks."
        return results
        # results['enddate'] = startdate + timedelta(14)
        # enddatestring = results['enddate'].strftime('%m/%d/%Y')
    else:
        results['enddate'] = enddate
        enddatestring = results['enddate'].replace(day=1).strftime('%m/%d/%Y')


    bindvars.append({'serviceNum': servicenum,
                 'startDate': startdatestring,
                 'endDate': enddatestring})

    dw.query_results(sql[1], bindvars=bindvars[1])

    results['production'] = dw.results

    if len(results['production']) == 0:
        results['error'] = 'There were no CAD estimates or Actual production ' \
                             'found for service number {} in the date range {} ' \
                             'to {}.'.format(servicenum, startdatestring, enddatestring)
        return results

    totals = [sum(j) for j in [i for i in zip(*results['production'])][1:3]]
    results['production'].append(['Total',
                                  round(totals[0], 3),
                                  round(totals[1], 3),
                                  round(totals[1]/totals[0], 4)
                                  ])

    return results

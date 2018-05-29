import os
from datetime import date, timedelta
from Luna.models import DataWarehouse

main_dir = os.getcwd()
luna_dir = os.path.join(main_dir, 'Luna')
utilities_dir = os.path.join(luna_dir, 'utilities')


def system_performance(servicenum, startdate, enddate):

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

    if startdate < results['account'][0][7].date():
        startdatestring = results['account'][0][7].strftime('%m/%d/%Y')
        results['startdate'] = results['account'][0][7]
    else:
        startdatestring = startdate.strftime('%m/%d/%Y')

    if enddate.month >= date.today().month and enddate.year >= date.today().year:
        enddatestring = (date.today().replace(day=1) - timedelta(1)).strftime('%m/%d/%Y')
        results['enddate'] = date.today().replace(day=1) - timedelta(1)
    else:
        enddatestring = enddate.strftime('%m/%d/%Y')

    bindvars.append({'serviceNum': servicenum,
                 'startDate': startdatestring,
                 'endDate': enddatestring})

    dw.query_results(sql[1], bindvars=bindvars[1])

    results['production'] = dw.results
    totals = [sum(j) for j in [i for i in zip(*results['production'])][1:3]]
    results['production'].append(['Total',
                                  round(totals[0], 3),
                                  round(totals[1], 3),
                                  round(totals[1]/totals[0], 4)
                                  ])

    return results

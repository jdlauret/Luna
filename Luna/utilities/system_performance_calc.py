import os
import datetime as dt
from datetime import date, timedelta
from decimal import *
from Luna.models import DataWarehouse
from models import SnowFlakeDW, SnowflakeConsole

main_dir = os.getcwd()
luna_dir = os.path.join(main_dir, 'Luna')
utilities_dir = os.path.join(luna_dir, 'utilities')

DB = SnowFlakeDW()
DB.set_user('MACK_DAMAVANDI')


def system_performance(servicenum, startdate, enddate):

    results = {}

    if enddate < startdate:
        results['error'] = 'The start date you entered ({}) must come before the end date you entered ({}).'\
            .format(startdate.strftime('%Y-%m-%d'), enddate.strftime('%Y-%m-%d'))
        return results

    if 'S-' in servicenum.upper():
        servicenum = servicenum.upper().replace('S-','')

    try:
        DB.open_connection()
        DW = SnowflakeConsole(DB)
        with open (os.path.join(utilities_dir, 'system_performance_calc.sql'), 'r') as file:
            sql = file.read()
        sql = sql.split(';')

        query = sql[0].format(service_number = str(servicenum))
        DW.execute_query(query)

    except Exception as e:
        results['error'] = e
        return results

    results['account'] = DW.query_results[0]

    if len(results['account']) == 0:
        results['error'] = '{} is not a valid service number or the associated ' \
                           'Project has been cancelled.'.format(servicenum)
        return results
    elif not results['account'][7]:
        results['error'] = '{} hasn\'t received PTO yet!'.format(servicenum)
        return results
    elif dt.datetime.strptime(startdate, '%Y-%m-%d').date() < results['account'][7]:
        results['startdate'] = results['account'][7]
        startdatestring = results['startdate'].strftime('%Y-%m-%d')
    else:
        results['startdate'] = dt.datetime.strptime(startdate, '%Y-%m-%d').date()
        startdatestring = results['startdate'].replace(day=1).strftime('%Y-%m-%d')

    if dt.datetime.strptime(enddate, '%Y-%m-%d').date() >= date.today() \
            and dt.datetime.strptime(enddate, '%Y-%m-%d').date() < results['startdate']\
            + timedelta(14) and results['startdate'] == results['account'][0][7]:
        # enddatestring = (date.today().replace(day=1) - timedelta(1)).strftime('%m/%d/%Y')
        # results['enddate'] = date.today().replace(day=1) - timedelta(1)
        results['error'] = "The system has not been PTO'd for at least two weeks."
        return results
        # results['enddate'] = startdate + timedelta(14)
        # enddatestring = results['enddate'].strftime('%m/%d/%Y')
    else:
        results['enddate'] = dt.datetime.strptime(enddate, '%Y-%m-%d').date()
        enddatestring = results['enddate'].replace(day=1).strftime('%Y-%m-%d')


    query_2 = sql[1].format(service_number=str(servicenum), start_date=str(startdate), end_date=str(enddate))
    try:
        DW.execute_query(query_2)
    except Exception as e:
        results['error'] = e
        return results

    results['production'] = DW.query_results

    if len(results['production']) == 0:
        results['error'] = 'There were no CAD estimates or Actual production ' \
                             'found for service number {} in the date range {} ' \
                             'to {}.'.format(servicenum, startdatestring, enddatestring)
        return results

    totals = [sum(j) for j in [i for i in zip(* results['production'])][1:4]]
    results['production'].append(['Total',
                                  round(totals[0], 3),
                                  round(totals[1], 3),
                                  round(totals[2], 3),
                                  round(Decimal(totals[2])/totals[0], 4),
                                  round(Decimal(totals[2])/totals[1], 4)
                                  ])

    results['account'][7] = results['account'][7].strftime('%B %#d, %Y')

    for month in results['production']:
        month[1] = '{} kWh'.format(month[1])
        month[2] = '{} kWh'.format(month[2])
        month[3] = '{} kWh'.format(month[3])
        month[4] = '{0:.2%}'.format(month[4])
        month[5] = '{0:.2%}'.format(month[5])

    results['summary'] = [
        'The solar energy system produced {} from {} to {}.'.format(
            results['production'][-1][3],
            results['startdate'].strftime('%m/%d/%Y'),
            results['enddate'].strftime('%m/%d/%Y')
        ),
        'The solar energy system at your home operated at {} of what we expected it to ' \
        'from {} to {}.'.format(
            results['production'][-1][5],
            results['startdate'].strftime('%m/%d/%Y'),
            results['enddate'].strftime('%m/%d/%Y')
        )
    ]

    return results

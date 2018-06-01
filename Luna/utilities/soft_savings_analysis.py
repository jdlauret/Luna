import os
from datetime import date, timedelta
from Luna.models import DataWarehouse

main_dir = os.getcwd()
luna_dir = os.path.join(main_dir, 'Luna')
utilities_dir = os.path.join(luna_dir, 'utilities')


def soft_savings_analysis(servicenum, startdate, enddate):

    if enddate < startdate:
        results = {'error': 'The start date you entered ({}) must come before the end date you entered ({}).'.format(startdate.strftime('%m/%d/%Y'), enddate.strftime('%m/%d/%Y'))}
        return results

    dw = DataWarehouse('admin')

    with open(os.path.join(utilities_dir, 'soft_savings_analysis.sql'),'r') as file:
        sql = file.read()

    sql = sql.split(';')

    if 'S-' in servicenum.upper():
        servicenum = servicenum.upper().replace('S-','')

    bindvars = [{'serviceNum': servicenum}]

    dw.query_results(sql[0], bindvars=bindvars[0])

    results = {'account': dw.results}

    if len(results['account']) == 0:
        results['accounterror'] = '{} is not a valid service number.'.format(servicenum)
        return results
    elif results['account'][0][7].date() > date.today()-timedelta(30):
        results['timeerror'] = 'The system hasn\'t been PTO\'d for more than 30 days.'
        return results
    elif results['account'][0][8] == None:
        results['utilityerror'] = 'There was no utility information found for service ' \
                                    '{}.'.format(servicenum)
        return results
    elif startdate < results['account'][0][7].date():
        results['startdate'] = results['account'][0][7]
        startdatestring = results['startdate'].strftime('%m/%d/%Y')
    else:
        results['startdate'] = startdate
        startdatestring = results['startdate'].replace(day=1).strftime('%m/%d/%Y')


    if enddate >= date.today() and enddate < results['startdate'].date() + timedelta(30) and results['startdate'] == results['account'][0][7]:
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

    results['savings'] = dw.results

    if len(results['savings']) == 0:
        results['savingserror'] = 'There was no Actual production ' \
                                     'found for service number {} in the date range {} ' \
                                     'to {}.'.format(servicenum, startdatestring, enddatestring)
        return results

    totals = [sum(j) for j in [i for i in zip(*results['savings'])][1:5]]
    results['savings'].append(['Total',
                                  round(totals[0], 2),
                                  round(totals[1], 2),
                                  round(totals[2], 2),
                                  round(totals[3], 2)
                                  ])

    results['summary'] ='Your system has produced {} kilowatt hours (kWh) since {}. '\
            'For that energy, you paid Vivint Solar ${}. '\
            'If you had paid your utility company, {}, for that same amount of energy, ' \
            'you would have paid ${}. Your total savings since {} is ${}.'.format(
                results['savings'][-1][1],
                results['startdate'].strftime('%m/%d/%Y'),
                '%.2f' % results['savings'][-1][2],
                results['account'][0][8],
                '%.2f' % results['savings'][-1][3],
                results['startdate'].strftime('%m/%d/%Y'),
                '%.2f' % results['savings'][-1][4]
            )

    return results

import os
from datetime import date, timedelta
from Luna.models import DataWarehouse

main_dir = os.getcwd()
luna_dir = os.path.join(main_dir, 'Luna')
utilities_dir = os.path.join(luna_dir, 'utilities')


def full_benefit_analysis(servicenum, consumption, backfeed, utilitybill):

    dw = DataWarehouse('admin')

    with open(os.path.join(utilities_dir, 'full_benefit_analysis.sql'),'r') as file:
        sql = file.read()

    sql = sql.split(';')

    if 'S-' in servicenum.upper():
        servicenum = servicenum.upper().replace('S-','')

    bindvars = [{'serviceNum': servicenum}]

    dw.query_results(sql[0], bindvars=bindvars[0])

    results = {'account': dw.results, 'error': None}

    if len(results['account']) == 0:
        results['error'] = '{} is not a valid service number.'.format(servicenum)
        return results
    elif results['account'][0][7].date() > date.today()-timedelta(365):
        results['error'] = 'Benefit Analyses can only be performed on systems ' \
            'that have been PTO\'d for at least one year.'
        return results
    elif results['account'][0][8] == None:
        results['error'] = 'There was no utility information found for service ' \
                                    '{}.'.format(servicenum)
        return results

    results['enddate'] = (date.today().replace(day=1) - timedelta(1))
    enddatestring = results['enddate'].strftime('%m/%d/%Y')
    results['startdate'] = (results['enddate'] - timedelta(365)).replace(month=results['enddate'].month % 12 + 1, day=1)
    startdatestring = results['startdate'].strftime('%m/%d/%Y')

    bindvars.append({'serviceNum': servicenum,
                 'startDate': startdatestring,
                 'endDate': enddatestring})

    dw.query_results(sql[1], bindvars=bindvars[1])

    results['production'] = dw.results

    if len(results['production']) == 0:
        results['error'] = 'There was no Actual production ' \
                             'found for service number {} in the date range {} ' \
                             'to {}.'.format(servicenum, startdatestring, enddatestring)
        return results

    i = 0
    while i < len(consumption):
        results['production'][i].append(consumption[i])
        results['production'][i].append(backfeed[i])
        results['production'][i].append(utilitybill[i])
        i += 1

    del i

    for month in results['production']:
        month.append(round(month[1] + month[3] - month[4], 3)) #total consumption
        month.append(round(month[6] * results['account'][0][9], 2)) #bill w/out solar
        month.append(round(month[2] + month[5], 2)) #bill w/solar
        month.append(round(month[7] - month[8], 2)) #savings

    results['header'] = [
        'Month',
        'Actual (kWh)',
        'Vivint Solar Bill',
        'Utility Consumption',
        'Excess Production Sent to Grid (kWh)',
        'Utility Bill',
        'Total Consumption',
        'Bill w/out Solar',
        'Bill w/Solar',
        'Savings'
    ]

    # results['production'] = [
    #     x + [results['production'][x][1] + results['production'][x][3] - results['production'][x][4]] for x in
    #     results['production']]
    # results['production'] = [x + [results['production'][x][6] * production['account'][9]] for x in
    #                          results['production']]
    # results['production'] = [x + [results['production'][x][2] + production['production'][5]] for x in
    #                          results['production']]

    totals = [sum(j) for j in [i for i in zip(*results['production'])][1:10]]
    results['production'].append([
            'Total',
            round(totals[0], 2),
            round(totals[1], 2),
            round(totals[2], 2),
            round(totals[3], 2),
            round(totals[4], 2),
            round(totals[5], 2),
            round(totals[6], 2),
            round(totals[7], 2),
            round(totals[8], 2)
        ]
    )





    # results['summary'] ='Your system has produced {} kilowatt hours (kWh) since {}. '\
    #         'For that energy, you paid Vivint Solar ${}. '\
    #         'If you had paid your utility company, {}, for that same amount of energy, ' \
    #         'you would have paid ${}. Your total savings since {} is ${}.'.format(
    #             results['savings'][-1][1],
    #             results['startdate'].strftime('%m/%d/%Y'),
    #             '%.2f' % results['savings'][-1][2],
    #             results['account'][0][8],
    #             '%.2f' % results['savings'][-1][3],
    #             results['startdate'].strftime('%m/%d/%Y'),
    #             '%.2f' % results['savings'][-1][4]
    #         )

    return results

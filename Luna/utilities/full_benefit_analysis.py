import os
from datetime import date, timedelta
from BI.data_warehouse.connector import Snowflake

main_dir = os.getcwd()
luna_dir = os.path.join(main_dir, 'Luna')
utilities_dir = os.path.join(luna_dir, 'utilities')

DB = Snowflake()
DB.set_user('MACK_DAMAVANDI')

# todo where is consumption, backfeed, and utility bill called?
def full_benefit_analysis(servicenum, consumption, backfeed, utilitybill):

    results = {}

    if 'S-' in servicenum.upper():
        servicenum = servicenum.upper().replace('S-','')

    try:
        DB.open_connection()
        with open (os.path.join(utilities_dir, 'full_benefit_analysis.sql'), 'r') as file:
            sql = file.read()
        sql = sql.split(';')

        query = sql[0].format(service_number=str(servicenum))
        DB.execute_query(query)

    except Exception as e:
        results['error'] = e
        return results

    results['account'] = DB.query_results[0]


    if len(results['account']) == 0:
        results['error'] = '{} is not a valid service number.'.format(servicenum)
        return results
    elif results['account'][7].date() > date.today()-timedelta(365):
        results['error'] = 'Benefit Analyses can only be performed on systems ' \
            'that have been PTO\'d for at least one year.'
        results['account'][7] = results['account'][7].strftime('%B %#d, %Y')
        results['account'][9] = '${} per kWh'.format(results['account'][9])
        results['account'][10] = '{} kWh'.format(results['account'][10])
        return results
    elif results['account'][8] == None:
        results['error'] = 'There was no utility information found for service ' \
                                    '{}.'.format(servicenum)
        results['account'][7] = results['account'][7].strftime('%B %#d, %Y')
        results['account'][10] = '{} kWh'.format(results['account'][10])
        return results

    results['enddate'] = (date.today().replace(day=1) - timedelta(1))
    enddatestring = results['enddate'].strftime('%m/%d/%Y')
    results['startdate'] = (results['enddate'] - timedelta(365)).replace(month=results['enddate'].month % 12 + 1, day=1)
    startdatestring = results['startdate'].strftime('%m/%d/%Y')

    # TODO query is calling start and enddate, but not called in here
    query_2 = sql[1].format(service_number=str(servicenum), start_date=str(startdate), end_date=str(enddate))
    try:
        DB.execute_query(query_2)

    except Exception as e:
        results['error'] = e
        return results

    finally:
        DB.close_connection()

    results['production'] = DB.query_results

    if len(results['production']) == 0:
        results['error'] = 'There was no Actual production ' \
                             'found for service number {} in the date range {} ' \
                             'to {}.'.format(servicenum, startdatestring, enddatestring)
        return results

    # with open(os.path.join(utilities_dir, 'monthly_consumption.sql'),'r') as file:
    #     sql = file.read()
    #
    # sql = sql.split(';')
    #
    # try:
    #     DW.query_results(sql[date.today().month-1], bindvars=bindvars[0])
    # except Exception as e:
    #     results['error'] = e
    #     return results
    #
    # results['presolarconsumption'] = DW.results

    i = 0
    while i < len(consumption):
        results['production'][i].insert(2, backfeed[i])
        results['production'][i].insert(3, consumption[i])
        results['production'][i].append(utilitybill[i])
        i += 1

    del i

    for month in results['production']:
        month.insert(2, month[1] - month[2]) #usage from panels
        month.insert(5, round(month[2] + month[4], 3)) #total consumption
        month.append(round(month[6] + month[7], 2)) #bill w/solar
        month.append(round(month[5] * results['account'][9], 2)) #bill w/out solar
        month.append(round(month[9] - month[8], 2)) #savings

    # results['header'] = [
    #     'Month',
    #     'Actual',
    #     'Usage',
    #     'Excess Production Sent to Grid',
    #     'Utility Consumption',
    #     'Total Consumption',
    #     'Vivint Solar Bill',
    #     'Utility Bill',
    #     'Bill w/Solar',
    #     'Bill w/out Solar',
    #     'Savings'
    # ]

    # results['production'] = [
    #     x + [results['production'][x][1] + results['production'][x][3] - results['production'][x][4]] for x in
    #     results['production']]
    # results['production'] = [x + [results['production'][x][6] * production['account'][9]] for x in
    #                          results['production']]
    # results['production'] = [x + [results['production'][x][2] + production['production'][5]] for x in
    #                          results['production']]

    totals = [sum(j) for j in [i for i in zip(*results['production'])][1:12]]
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
            round(totals[8], 2),
            round(totals[9], 2)
        ]
    )

    results['account'][9] = '${} per kWh'.format(round(results['account'][9], 5))
    results['account'][7] = results['account'][7].strftime('%B %#d, %Y')
    results['account'][10] = '{} kWh'.format(results['account'][10])

    for month in results['production']:
        month[1] = '{} kWh'.format(month[1])
        month[2] = '{} kWh'.format(month[2])
        month[3] = '{} kWh'.format(month[3])
        month[4] = '{} kWh'.format(month[4])
        month[5] = '{} kWh'.format(month[5])
        if month[6] < 0:
            month[6] = '$({})'.format('%.2f' % abs(month[6]))
        else:
            month[6] = '${}'.format('%.2f' % month[6])
        if month[7] < 0:
            month[7] = '$({})'.format('%.2f' % abs(month[7]))
        else:
            month[7] = '${}'.format('%.2f' % month[7])
        if month[8] < 0:
            month[8] = '$({})'.format('%.2f' % abs(month[8]))
        else:
            month[8] = '${}'.format('%.2f' % month[8])
        if month[9] < 0:
            month[9] = '$({})'.format('%.2f' % abs(month[9]))
        else:
            month[9] = '${}'.format('%.2f' % month[9])
        if month[10] < 0:
            month[10] = '$({})'.format('%.2f' % abs(month[10]))
        else:
            month[10] = '${}'.format('%.2f' % month[10])







    # results['summary'] ='Your system has produced {} kilowatt hours (kWh) since {}. '\
    #         'For that energy, you paid Vivint Solar ${}. '\
    #         'If you had paid your utility company, {}, for that same amount of energy, ' \
    #         'you would have paid ${}. Your total savings since {} is ${}.'.format(
    #             results['savings'][-1][1],
    #             results['startdate'].strftime('%m/%d/%Y'),
    #             '%.2f' % results['savings'][-1][2],
    #             results['account'][8],
    #             '%.2f' % results['savings'][-1][3],
    #             results['startdate'].strftime('%m/%d/%Y'),
    #             '%.2f' % results['savings'][-1][4]
    #         )

    return results

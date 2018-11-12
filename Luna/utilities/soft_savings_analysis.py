import os
import datetime as dt
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from BI.data_warehouse.connector import Snowflake

main_dir = os.getcwd()
luna_dir = os.path.join(main_dir, 'Luna')
utilities_dir = os.path.join(luna_dir, 'utilities')

DB = Snowflake()
DB.set_user('MACK_DAMAVANDI')


def soft_savings_analysis(servicenum, startdate, enddate):

    results = {}

    if enddate < startdate:
        results = {'error': 'The start date you entered ({}) must come before the end date you entered ({}).'.format(startdate.strftime('%Y-%m-%d'), enddate.strftime('%Y-%m-%d'))}
        return results

    if 'S-' in servicenum.upper():
        servicenum = servicenum.upper().replace('S-','')

    try:
        DB.open_connection()
        with open(os.path.join(utilities_dir, 'soft_savings_analysis.sql'),'r') as file:
            sql = file.read()
        sql = sql.split(';')

        query = sql[0].format(service_number=str(servicenum))
        DB.execute_query(query)

    except Exception as e:
        results['error'] = e
        return results

    results['account'] = DB.query_results[0]

    if len(results['account']) == 0:
        results['error'] = '{} is not a valid service number or the associated ' \
                           'Solar Project has been cancelled.'.format(servicenum)
        return results
    elif not results['account'][7]:
        results['error'] = 'The system hasn\'t been PTO\'d yet!'
        results['account'][9] = '${}'.format(round(results['account'][9], 5))
        return results
    elif results['account'][7] > date.today()-timedelta(30):
        results['error'] = 'The system hasn\'t been PTO\'d for more than 30 days.'
        return results
    # elif results['account'][0][7].date() > date.today()-timedelta(365):
    #     results['error'] = 'Benefit Analyses can only be performed on systems ' \
    #         'that have been PTO\'d for at least one year.'
    #     results['account'][0][7] = results['account'][0][7].strftime('%B %#d, %Y')
    #     results['account'][0][9] = '${} per kWh'.format(results['account'][0][9])
    #     return results
    elif results['account'][8] == None:
        results['error'] = 'There was no utility information found for service ' \
                                    '{}.'.format(servicenum)
        results['account'][7] = results['account'][7].strftime('%B %#d, %Y')
        return results
    elif results['account'][-1] != 'Solar PPA' and results['account'][-1] != 'Solar Lease':
        results['error'] = 'This calculator is only for PPA and Lease customers! This customer has a' \
                           ' {}. For Loan customers, please refer them to their Loan Documents.' \
                           ''.format(results['account'][-1])
        results['account'][9] = '${}'.format(round(results['account'][9], 5))
        results['account'][7] = results['account'][7].strftime('%B %#d, %Y')
        return results
    elif dt.datetime.strptime(startdate, '%Y-%m-%d').date() < results['account'][7]:
        results['startdate'] = results['account'][7]
        startdatestring = results['startdate'].strftime('%Y-%m-%d')
    else:
        results['startdate'] = dt.datetime.strptime(startdate, '%Y-%m-%d').date()
        startdatestring = results['startdate'].replace(day=1).strftime('%Y-%m-%d')
        # results['enddate'] = (date.today().replace(day=1) - timedelta(1))
        # enddatestring = results['enddate'].strftime('%Y-%m-%d')
        # results['startdate'] = (results['enddate'] - timedelta(365)).replace(month=results['enddate'].month % 12 + 1,
        #                                                                      day=1)
        # startdatestring = results['startdate'].strftime('%Y-%m-%d')

    results['account'][9] = '${}'.format(round(results['account'][9], 5))

    if dt.datetime.strptime(enddate, '%Y-%m-%d').date() >= date.today() \
            and dt.datetime.strptime(enddate, '%Y-%m-%d').date() < results['startdate'] + timedelta(30) \
            and results['startdate'] == results['account'][7]:
        enddatestring = (date.today().replace(day=1) - timedelta(1)).strftime('%Y-%m-%d')
        results['enddate'] = date.today().replace(day=1) - timedelta(1)
        results['error'] = "The system has not been PTO'd for at least two weeks."
        return results
        # results['enddate'] = startdate + timedelta(14)
        # enddatestring = results['enddate'].strftime('%Y-%m-%d')
    else:
        results['enddate'] = dt.datetime.strptime(enddate, '%Y-%m-%d').date()
        enddatestring = results['enddate'].replace(day=1).strftime('%Y-%m-%d')


    # bindvars.append({'serviceNum': servicenum,
    #              'startDate': startdatestring,
    #              'endDate': enddatestring})
    query_2 = sql[1].format(service_number=str(servicenum), start_date=str(startdate), end_date=str(enddate))
    try:
        DB.execute_query(query_2)

    except Exception as e:
        results['error'] = e
        return results

    finally:
        DB.close_connection()

    results['savings'] = DB.query_results

    if len(results['savings']) == 0:
        results['error'] = 'There was no Actual production ' \
                                     'found for service number {} in the date range {} ' \
                                     'to {}.'.format(servicenum, startdatestring, enddatestring)
        return results

    totals = [sum(j) for j in [i for i in zip(*results['savings'])][1:6]]
    results['savings'].append(['Total',
                                  round(totals[0], 2),
                                  '',
                                  round(totals[2], 2),
                                  round(totals[3], 2),
                                  round(totals[4], 2)
                                  ])

    if results['savings'][-1][5] < 0:
        results['summary'] = [
            'The calculation shows that this customer is not saving money with our system. ' \
            'They have paid ${} more to us than they would have paid their utility company ' \
            'for the energy the system produced.'.format(-results['savings'][-1][5])
        ]

        for month in results['savings']:
            month[1] = '{} kWh'.format(month[1])
            if not month[2]:
                pass
            elif month[2] < 0:
                month[2] = '$({})'.format('%.5f' % abs(month[2]))
            else:
                month[2] = '${}'.format('%.5f' % month[2])
            if month[3] < 0:
                month[3] = '$({})'.format('%.2f' % abs(month[3]))
            else:
                month[3] = '${}'.format('%.2f' % month[3])
            if month[4] < 0:
                month[4] = '$({})'.format('%.2f' % abs(month[4]))
            else:
                month[4] = '${}'.format('%.2f' % month[4])
            if month[5] < 0:
                month[5] = '$({})'.format('%.2f' % abs(month[5]))
            else:
                month[5] = '${}'.format('%.2f' % month[5])

        results['summary'].extend(
            [
                'Your system has produced {} kilowatt hours (kWh) since {}.'.format(
                    results['savings'][-1][1].split()[0],
                    results['startdate'].strftime('%Y-%m-%d')
                ),
                'For that energy, you paid Vivint Solar {}.'.format(results['savings'][-1][3]),
                'The average utility customer of your utility, {}, would have paid {} for that same amount of energy.'.format(
                    results['account'][0][8],
                    results['savings'][-1][4]
                ),
                'For the average utility customer with {}, who had {} kilowatt hours (kWh) of production since {},' \
                ' they would have saved {}.'.format(
                    results['account'][0][8],
                    results['savings'][-1][1].split()[0],
                    results['startdate'].strftime('%Y-%m-%d'),
                    results['savings'][-1][5]
                ),
                'From {} to {}, the solar energy system at your home has produced enough energy to offset the carbon ' \
                'emissions of {} miles driven by the average passenger car (according to the EPA\'s Greenhouse Gas ' \
                'Equivalencies Calculator).'.format(
                    results['startdate'].strftime('%Y-%m-%d'),
                    results['enddate'].strftime('%Y-%m-%d'),
                    round(float(results['savings'][-1][1].split()[0])*1.824,1)
                ),
            'From {} to {}, the solar energy system at your home has offset the same amount of carbon ' \
                'emissions as {} newly planted trees (according to the EPA\'s Greenhouse Gas ' \
                'Equivalencies Calculator).'.format(
                    results['startdate'].strftime('%Y-%m-%d'),
                    results['enddate'].strftime('%Y-%m-%d'),
                    int(round(float(results['savings'][-1][1].split()[0])*0.0391,0))
                )
            ]
        )
    else:
        for month in results['savings']:
            month[1] = '{} kWh'.format(month[1])
            if not month[2]:
                pass
            elif month[2] < 0:
                month[2] = '$({})'.format('%.5f' % abs(month[2]))
            else:
                month[2] = '${}'.format('%.5f' % month[2])
            if month[3] < 0:
                month[3] = '$({})'.format('%.2f' % abs(month[3]))
            else:
                month[3] = '${}'.format('%.2f' % month[3])
            if month[4] < 0:
                month[4] = '$({})'.format('%.2f' % abs(month[4]))
            else:
                month[4] = '${}'.format('%.2f' % month[4])
            if month[5] < 0:
                month[5] = '$({})'.format('%.2f' % abs(month[5]))
            else:
                month[5] = '${}'.format('%.2f' % month[5])

        results['summary'] = [
            'Your system has produced {} kilowatt hours (kWh) since {}.'.format(
                results['savings'][-1][1].split()[0],
                results['startdate'].strftime('%Y-%m-%d')
            ),
            'For that energy, you paid Vivint Solar {}.'.format(results['savings'][-1][3]),
            'The average utility customer of your utility, {}, would have paid {} for that same amount of energy.'.format(
                results['account'][0][8],
                results['savings'][-1][4]
            ),
            'For the average utility customer with {}, who had {} kilowatt hours (kWh) of production since {},' \
            ' they would have saved {}.'.format(
                results['account'][0][8],
                results['savings'][-1][1].split()[0],
                results['startdate'].strftime('%Y-%m-%d'),
                results['savings'][-1][5]
            ),
            'From {} to {}, the solar energy system at your home has produced enough energy to offset the carbon ' \
            'emissions of {} miles driven by the average passenger car (according to the EPA\'s Greenhouse Gas ' \
            'Equivalencies Calculator).'.format(
                results['startdate'].strftime('%Y-%m-%d'),
                results['enddate'].strftime('%Y-%m-%d'),
                round(float(results['savings'][-1][1].split()[0])*1.824,1)
            ),
            'From {} to {}, the solar energy system at your home has offset the same amount of carbon ' \
            'emissions as {} newly planted trees (according to the EPA\'s Greenhouse Gas ' \
            'Equivalencies Calculator).'.format(
                results['startdate'].strftime('%Y-%m-%d'),
                results['enddate'].strftime('%Y-%m-%d'),
                round(float(results['savings'][-1][1].split()[0])*0.0391,0)
            )
        ]

    results['account'][7] = results['account'][7].strftime('%B %#d, %Y')

    return results

def silver_soft_savings_analysis(servicenum):

    results = {}

    # if enddate < startdate:
    #     results = {'error': 'The start date you entered ({}) must come before the end date you entered ({}).'.format(startdate.strftime('%Y-%m-%d'), enddate.strftime('%Y-%m-%d'))}
    #     return results

    if 'S-' in servicenum.upper():
        servicenum = servicenum.upper().replace('S-','')

    try:
        DB.open_connection()
        with open(os.path.join(utilities_dir, 'silver_soft_savings_analysis.sql'),'r') as file:
            sql = file.read()
        sql = sql.split(';')

        query = sql[0].format(service_number=str(servicenum))
        DB.execute_query(query)

    except Exception as e:
        results['error'] = e
        return results

    finally:
        DB.close_connection()

    results['account'] = DB.query_results[0][4:]

    if len(results['account']) == 0:
        results['error'] = '{} is not a valid service number or the associated ' \
                           'Solar Project has been cancelled.'.format(servicenum)
        return results
    elif DB.query_results[0][0] < 12:
        results['error'] = '{} has not been PTO\'d for at least 12 months!'.format(servicenum)
        return results
    elif not results['account'][7]:
        results['error'] = 'The system hasn\'t been PTO\'d yet!'
        results['account'][9] = '${}'.format(round(results['account'][9], 5))
        return results
    elif results['account'][7] > date.today()-timedelta(30):
        results['error'] = 'The system hasn\'t been PTO\'d for more than 30 days.'
        return results
    # elif results['account'][0][7].date() > date.today()-timedelta(365):
    #     results['error'] = 'Benefit Analyses can only be performed on systems ' \
    #         'that have been PTO\'d for at least one year.'
    #     results['account'][0][7] = results['account'][0][7].strftime('%B %#d, %Y')
    #     results['account'][0][9] = '${} per kWh'.format(results['account'][0][9])
    #     return results
    elif results['account'][8] == None:
        results['error'] = 'There was no utility information found for service ' \
                                    '{}.'.format(servicenum)
        results['account'][7] = results['account'][7].strftime('%B %#d, %Y')
        return results
    elif results['account'][-1] != 'Solar PPA' and results['account'][-1] != 'Solar Lease':
        results['error'] = 'This calculator is only for PPA and Lease customers! This customer has a' \
                           ' {}. For Loan customers, please refer them to their Loan Documents.' \
                           ''.format(results['account'][-1])
        results['account'][9] = '${}'.format(round(results['account'][9], 5))
        results['account'][7] = results['account'][7].strftime('%B %#d, %Y')
        return results
    # elif dt.datetime.strptime(startdate, '%Y-%m-%d').date() < results['account'][7]:
    #     results['startdate'] = results['account'][7]
    #     startdatestring = results['startdate'].strftime('%Y-%m-%d')
    # else:
    #     results['startdate'] = dt.datetime.strptime(startdate, '%Y-%m-%d').date()
    #     startdatestring = results['startdate'].replace(day=1).strftime('%Y-%m-%d')
        # results['enddate'] = (date.today().replace(day=1) - timedelta(1))
        # enddatestring = results['enddate'].strftime('%Y-%m-%d')
        # results['startdate'] = (results['enddate'] - timedelta(365)).replace(month=results['enddate'].month % 12 + 1,
        #                                                                      day=1)
        # startdatestring = results['startdate'].strftime('%Y-%m-%d')

    results['account'][9] = '${}'.format(round(results['account'][9], 5))

    # if dt.datetime.strptime(enddate, '%Y-%m-%d').date() >= date.today() \
    #         and dt.datetime.strptime(enddate, '%Y-%m-%d').date() < results['startdate'] + timedelta(30) \
    #         and results['startdate'] == results['account'][7]:
    #     enddatestring = (date.today().replace(day=1) - timedelta(1)).strftime('%Y-%m-%d')
    #     results['enddate'] = date.today().replace(day=1) - timedelta(1)
    #     results['error'] = "The system has not been PTO'd for at least two weeks."
    #     return results
    #     # results['enddate'] = startdate + timedelta(14)
    #     # enddatestring = results['enddate'].strftime('%Y-%m-%d')
    # else:
    #     results['enddate'] = dt.datetime.strptime(enddate, '%Y-%m-%d').date()
    #     enddatestring = results['enddate'].replace(day=1).strftime('%Y-%m-%d')

    results['startdate'] = date.today().replace(day=1) - relativedelta(years=1)
    results['enddate'] = date.today().replace(day=1) - relativedelta(days=1)

    # bindvars.append({'serviceNum': servicenum,
    #              'startDate': startdatestring,
    #              'endDate': enddatestring})
    query_2 = sql[1].format(service_number=str(servicenum)) #, start_date=str(startdate), end_date=str(enddate))
    try:
        DB.execute_query(query_2)

    except Exception as e:
        results['error'] = e
        return results

    finally:
        DB.close_connection()

    results['savings'] = DB.query_results

    if len(results['savings']) == 0:
        results['error'] = 'There was no Actual production ' \
                                     'found for service number {} in the date range {} ' \
                                     'to {}.'.format(servicenum, startdatestring, enddatestring)
        return results

    totals = [sum(j) for j in [i for i in zip(*results['savings'])][1:6]]
    results['savings'].append(['Total',
                                  round(totals[0], 2),
                                  '',
                                  round(totals[2], 2),
                                  round(totals[3], 2),
                                  round(totals[4], 2)
                                  ])

    if results['savings'][-1][5] < 0:
        results['summary'] = [
            'The calculation shows that this customer is not saving money with our system. ' \
            'They have paid ${} more to us than they would have paid their utility company ' \
            'for the energy the system produced.'.format(-results['savings'][-1][5])
        ]

        for month in results['savings']:
            month[1] = '{} kWh'.format(month[1])
            if not month[2]:
                pass
            elif month[2] < 0:
                month[2] = '$({})'.format('%.5f' % abs(month[2]))
            else:
                month[2] = '${}'.format('%.5f' % month[2])
            if month[3] < 0:
                month[3] = '$({})'.format('%.2f' % abs(month[3]))
            else:
                month[3] = '${}'.format('%.2f' % month[3])
            if month[4] < 0:
                month[4] = '$({})'.format('%.2f' % abs(month[4]))
            else:
                month[4] = '${}'.format('%.2f' % month[4])
            if month[5] < 0:
                month[5] = '$({})'.format('%.2f' % abs(month[5]))
            else:
                month[5] = '${}'.format('%.2f' % month[5])

        results['summary'].extend(
            [
                'Your system has produced {} kilowatt hours (kWh) since {}.'.format(
                    results['savings'][-1][1].split()[0],
                    results['startdate'].strftime('%Y-%m-%d')
                ),
                'For that energy, you paid Vivint Solar {}.'.format(results['savings'][-1][3]),
                'The average utility customer of your utility, {}, would have paid {} for that same amount of energy.'.format(
                    results['account'][8],
                    results['savings'][-1][4]
                ),
                'For the average utility customer with {}, who had {} kilowatt hours (kWh) of production since {},' \
                ' they would have saved {}.'.format(
                    results['account'][8],
                    results['savings'][-1][1].split()[0],
                    results['startdate'].strftime('%Y-%m-%d'),
                    results['savings'][-1][5]
                ),
                'From {} to {}, the solar energy system at your home has produced enough energy to offset the carbon ' \
                'emissions of {} miles driven by the average passenger car (according to the EPA\'s Greenhouse Gas ' \
                'Equivalencies Calculator).'.format(
                    results['startdate'].strftime('%Y-%m-%d'),
                    results['enddate'].strftime('%Y-%m-%d'),
                    round(float(results['savings'][-1][1].split()[0])*1.824,1)
                ),
            'From {} to {}, the solar energy system at your home has offset the same amount of carbon ' \
                'emissions as {} newly planted trees (according to the EPA\'s Greenhouse Gas ' \
                'Equivalencies Calculator).'.format(
                    results['startdate'].strftime('%Y-%m-%d'),
                    results['enddate'].strftime('%Y-%m-%d'),
                    int(round(float(results['savings'][-1][1].split()[0])*0.0391,0))
                )
            ]
        )
    else:
        for month in results['savings']:
            month[1] = '{} kWh'.format(month[1])
            if not month[2]:
                pass
            elif month[2] < 0:
                month[2] = '$({})'.format('%.5f' % abs(month[2]))
            else:
                month[2] = '${}'.format('%.5f' % month[2])
            if month[3] < 0:
                month[3] = '$({})'.format('%.2f' % abs(month[3]))
            else:
                month[3] = '${}'.format('%.2f' % month[3])
            if month[4] < 0:
                month[4] = '$({})'.format('%.2f' % abs(month[4]))
            else:
                month[4] = '${}'.format('%.2f' % month[4])
            if month[5] < 0:
                month[5] = '$({})'.format('%.2f' % abs(month[5]))
            else:
                month[5] = '${}'.format('%.2f' % month[5])

        results['summary'] = [
            'Your system has produced {} kilowatt hours (kWh) since {}.'.format(
                results['savings'][-1][1].split()[0],
                results['startdate'].strftime('%Y-%m-%d')
            ),
            'For that energy, you paid Vivint Solar {}.'.format(results['savings'][-1][3]),
            'The average utility customer of your utility, {}, would have paid {} for that same amount of energy.'.format(
                results['account'][8],
                results['savings'][-1][4]
            ),
            'For the average utility customer with {}, who had {} kilowatt hours (kWh) of production since {},' \
            ' they would have saved {}.'.format(
                results['account'][8],
                results['savings'][-1][1].split()[0],
                results['startdate'].strftime('%Y-%m-%d'),
                results['savings'][-1][5]
            ),
            'From {} to {}, the solar energy system at your home has produced enough energy to offset the carbon ' \
            'emissions of {} miles driven by the average passenger car (according to the EPA\'s Greenhouse Gas ' \
            'Equivalencies Calculator).'.format(
                results['startdate'].strftime('%Y-%m-%d'),
                results['enddate'].strftime('%Y-%m-%d'),
                round(float(results['savings'][-1][1].split()[0])*1.824,1)
            ),
            'From {} to {}, the solar energy system at your home has offset the same amount of carbon ' \
            'emissions as {} newly planted trees (according to the EPA\'s Greenhouse Gas ' \
            'Equivalencies Calculator).'.format(
                results['startdate'].strftime('%Y-%m-%d'),
                results['enddate'].strftime('%Y-%m-%d'),
                round(float(results['savings'][-1][1].split()[0])*0.0391,0)
            )
        ]

    results['account'][7] = results['account'][7].strftime('%B %#d, %Y')

    return results

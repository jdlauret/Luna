import os
from models import SnowflakeConsole, SnowFlakeDW
from datetime import timedelta, date, datetime
from dateutil.relativedelta import relativedelta
from decimal import Decimal

main_dir = os.getcwd()
luna_dir = os.path.join(main_dir, 'Luna')
utilities_dir = os.path.join(luna_dir, 'utilities')

DB = SnowFlakeDW()
DB.set_user('MACK_DAMAVANDI')

def present_value(future_value, rate_of_return, number_periods):

    return future_value * Decimal((1 + rate_of_return) ** (number_periods * -1))

def net_present_value(future_values, rate_of_return, number_periods):

    total = 0
    counter = 0
    while counter < number_periods:
        total += future_values[counter] / Decimal((1 + rate_of_return) ** counter)
        counter += 1

    return total


def prepay_calc(servicenum):
    notes = {}

    if 'S-' in servicenum.upper():
        servicenum = servicenum.upper().replace('S-', '')

    try:
        DB.open_connection()
        DW = SnowflakeConsole(DB)
        with open(os.path.join(utilities_dir, 'prepayment_calc.sql'), 'r') as file:
            sql = file.read()
        # sql = sql.split(';')
    except Exception as e:
        notes['error'] = e
        return notes

    finally:
        DB.close_connection()

    DW.execute_query(sql.format(service_number = str(servicenum)))
    query = DW.query_results
    header = DW.query_columns
    prepayment_inputs = {}

    i = 0
    while i < 19:
        prepayment_inputs[header[i]] = query[0][i]
        i += 1

    prepayment_inputs['DESIGN_PROD_BY_MONTH'] = []

    while i < 31:
        prepayment_inputs['DESIGN_PROD_BY_MONTH'].append(query[0][i])
        i += 1

    prepayment_inputs[header[i]] = query[0][i]

    pv_of_expected_invoice = 0
    expected_invoice = []
    # expected_prod = []
    # contract_rate = []

    term_left = prepayment_inputs['REMAINING_CONTRACT_TERM']
    term_passed = 240 - term_left
    in_service = prepayment_inputs['IN_SERVICE_DATE'].date().replace(day=1)
    monthly_discount_rate = prepayment_inputs['DISCOUNT_RATE']/100/12
    degradation = prepayment_inputs['DEGRADATION'] / 100
    escalator = prepayment_inputs['ESCALATOR'] / 100
    today = date.today().replace(day=1)
    month = relativedelta(months=1)

    counter = 0
    terms = 1
    while counter < 240:
        first_of_month = in_service + month * counter
        month_of_year = first_of_month.month - 1
        years_pto = ((in_service + month * counter) - in_service).days // 365

        production = prepayment_inputs['DESIGN_PROD_BY_MONTH'][month_of_year] * \
                     (1 - degradation) ** years_pto
        # expected_prod.append(production)

        rate = prepayment_inputs['RATE_PER_KWH'] * (1 + escalator) ** years_pto
        # contract_rate.append(rate)

        invoice = production * Decimal(rate)
        expected_invoice.append(invoice)

        if first_of_month > today:
            pv_of_expected_invoice += present_value(invoice, monthly_discount_rate, terms)
            terms += 1

        counter += 1

    # counter = 0
    # while counter <= term_passed:
    #     month_of_year = (in_service + month * counter).month - 1


    if 'N' != prepayment_inputs['TAXABLE']:
        sales_tax = round(pv_of_expected_invoice * prepayment_inputs['SALES_TAX'], 2)
        pv_of_expected_invoice = round(pv_of_expected_invoice, 2)
        total_prepayment_value = pv_of_expected_invoice + sales_tax
    else:
        sales_tax = 0
        pv_of_expected_invoice = round(pv_of_expected_invoice, 2)
        total_prepayment_value = pv_of_expected_invoice + sales_tax

    estimated_prepayment_price = []

    estimated_prepayment_price.append(net_present_value(expected_invoice, monthly_discount_rate, len(expected_invoice)))

    ((today.replace(day=1) + month * 13) - prepayment_inputs['IN_SERVICE_DATE'].date().replace(day=1))

    test = (today.replace(day=1) - prepayment_inputs['IN_SERVICE_DATE'].date().replace(day=1))
    test1 = test.days // 365
    test2 = ((today.replace(day=1) + month*13) - prepayment_inputs['IN_SERVICE_DATE'].date().replace(day=1))
    test3 = test2.days // 365

    return notes
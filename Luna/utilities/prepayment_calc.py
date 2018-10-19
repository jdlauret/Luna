import os
from models import SnowflakeConsole, SnowFlakeDW
from datetime import timedelta, date, datetime
from dateutil.relativedelta import relativedelta
from decimal import Decimal
from collections import namedtuple

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

class PrepayCalc:
    def __init__(self, servicenum):
        """
        Prepayment Calculator Class for Customer Solutions
        :param servicenum: the account number of the customer for whom the calculation is being performed
        """
        self.servicenum = servicenum.upper()
        self.eligible = True
        self.prepayment_inputs = None
        self.pv_of_expected_invoice = 0
        self.expected_invoice = []
        self.unpacker = namedtuple(
            'inputs',
            'sales_tax taxable service_name project_number full_name service_address service_city service_state ' \
                'service_zip_code escalator degradation discount_rate system_size install_date in_service_date ' \
                'remaining_contract_term contract_type contract_version contract_rate monthly_estimates yearly_estimate'
        )

    def _format_service_num(self):
        if 'S-' in self.servicenum:
                self.servicenum = self.servicenum.replace('S-', '')

    def _unpack_results(self, query):
        results = query[0][0:19]
        results.append(query[0][19:31])
        results.append(query[0][31])

        self.prepayment_inputs = self.unpacker._make(results)

    def _get_query_results(self):
        self._format_service_num()
        try:
            DB.open_connection()
            DW = SnowflakeConsole(DB)
            with open(os.path.join(utilities_dir, 'prepayment_calc.sql'), 'r') as file:
                sql = file.read()
            DW.execute_query(sql.format(service_number = str(self.servicenum)))
            self._unpack_results(DW.query_results)
        except Exception as e:
            return e
        finally:
            DB.close_connection()

    def _calculate_cost(self, contract=self.prepayment_inputs.contract_type):
        if contract == 'Solar PPA':
            self._calculate_for_PPA() #todo: write _calculate_for_PPA with logic below
        else if contract == 'Solar Lease':
            self._calculate_for_Lease() #todo: write _calculate_for_Lease
        else:
            self.eligible = False

        in_service = self.prepayment_inputs.in_service_date.replace(day=1)
        monthly_discount_rate = self.prepayment_inputs.discount_rate / 100 / 12
        degradation = self.prepayment_inputs.degradation / 100
        escalator = self.prepayment_inputs.escalator / 100
        today = date.today().replace(day=1)
        month = relativedelta(months=1)
        expected_invoice = []

        counter = 0
        terms = 1
        while counter < 240:
            first_of_month = in_service + month * counter
            month_of_year = first_of_month.month - 1
            years_pto = ((in_service + month * counter) - in_service).days // 365

            production = self.prepayment_inputs.monthly_estimates[month_of_year] * \
                         (1 - degradation) ** years_pto
            # expected_prod.append(production)

            rate = self.prepayment_inputs.contract_rate * (1 + escalator) ** years_pto
            # contract_rate.append(rate)

            invoice = production * Decimal(rate)
            expected_invoice.append(invoice)

            if first_of_month > today:
                self.pv_of_expected_invoice += present_value(invoice, monthly_discount_rate, terms)
                terms += 1

            counter += 1

    def run(self):
        self._get_query_results()
        self._calculate_cost()


    def prepay_calc(self, servicenum):
        # notes = {}
        #
        # if 'S-' in servicenum.upper():
        #     servicenum = servicenum.upper().replace('S-', '')
        #
        # try:
        #     DB.open_connection()
        #     DW = SnowflakeConsole(DB)
        #     with open(os.path.join(utilities_dir, 'prepayment_calc.sql'), 'r') as file:
        #         sql = file.read()
        #     # sql = sql.split(';')
        # except Exception as e:
        #     notes['error'] = e
        #     return notes
        #
        # finally:
        #     DB.close_connection()
        #
        # DW.execute_query(sql.format(service_number = str(servicenum)))
        # query = DW.query_results
        # header = DW.query_columns
        # prepayment_inputs = {}
        #
        # i = 0
        # while i < 19:
        #     prepayment_inputs[header[i]] = query[0][i]
        #     i += 1
        #
        # prepayment_inputs['DESIGN_PROD_BY_MONTH'] = []
        #
        # while i < 31:
        #     prepayment_inputs['DESIGN_PROD_BY_MONTH'].append(query[0][i])
        #     i += 1
        #
        # prepayment_inputs[header[i]] = query[0][i]
        #
        # pv_of_expected_invoice = 0
        # expected_invoice = []
        # # expected_prod = []
        # # contract_rate = []

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



# class Inputs(PrepayCalc.NamedTuple):
#     sales_tax: float
#     taxable: str
#     service_name: str
#     project_number: str
#     full_name: str
#     service_address: str
#     service_city: str
#     service_state: str
#     service_zip_code: str
#     escalator: float
#     degradation: float
#     discount_rate: float
#     system_size: float
#     install_date: datetime.date
#     in_service_date: datetime.date
#     remaining_contract_term: int
#     contract_type: str
#     contract_version: str
#     contract_rate: float
#     monthly_estimates: list
#     yearly_estimate: float
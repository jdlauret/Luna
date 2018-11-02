import os
from models import SnowflakeConsole, SnowFlakeDW
# from BI.data_warehouse.connector import Snowflake
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
        total += future_values[counter] / Decimal((1 + rate_of_return) ** (counter + 1))
        counter += 1

    return total

# def prepay_calc(service_num):
#     pass

class PrepayCalc:
    def __init__(self, servicenum):
        """
        Prepayment Calculator Class for Customer Solutions
        :param servicenum: the account number of the customer for whom the calculation is being performed
        """
        self.servicenum = servicenum.upper()
        self.contract_type_eligible = True
        self.contract_version_eligible = True
        self.calc_error = None
        self.prepayment_inputs = None
        self.yearly_estimated_prepayment_amounts = None
        self.pv_of_expected_invoice = 0
        self.pv_of_expected_SRECs = 0
        self.tax = 0
        self.total_prepayment_price = 0
        self.expected_invoice = []
        self.unpacker = namedtuple(
            'inputs',
            'sales_tax taxable service_name project_number full_name service_address service_city service_state ' \
                'service_zip_code escalator degradation discount_rate system_size install_date in_service_date ' \
                'remaining_contract_term current_contract_month contract_type contract_version contract_rate ' \
                'monthly_estimates yearly_estimate'
        )
        self.unpack_yearly_prepayment = namedtuple(
            'prepayment_estimates',
            'year1 year2 year3 year4 year5 year6 year7 year8 year9 year10 ' \
            'year11 year12 year13 year14 year15 year16 year17 year18 year19 year20'
        )
        self.error_creator = namedtuple(
            'error',
            'error_flag error_note'
        )

    def _format_service_num(self):
        if 'S-' in self.servicenum:
                self.servicenum = self.servicenum.replace('S-', '')

    def _unpack_results(self, query):
        results = query[0][0:20]
        results.append(query[0][20:32])
        results.append(query[0][32])

        self.prepayment_inputs = self.unpacker._make(results)

    def _get_query_results(self):
        if not self.prepayment_inputs:
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
        else:
            pass

    def _calculate_cost(self):
        if self.pv_of_expected_invoice or \
                self.pv_of_expected_SRECs or \
                self.expected_invoice or \
                self.total_prepayment_price or \
                self.tax:
            self.pv_of_expected_invoice = \
                self.pv_of_expected_SRECs = \
                self.total_prepayment_price = \
                self.tax = 0
            self.expected_invoice = []

        if self.prepayment_inputs.contract_type == 'Solar PPA':
            self._calculate_for_PPA()
        elif self.prepayment_inputs.contract_type == 'Solar Lease':
            self._calculate_for_Lease()
        else:
            self.contract_type_eligible = False

        self._calculate_SREC()
        self._calculate_total()

    def _calculate_for_PPA(self):
        in_service = self.prepayment_inputs.in_service_date.replace(day=1)
        monthly_discount_rate = self.prepayment_inputs.discount_rate / 100 / 12
        degradation = self.prepayment_inputs.degradation / 100
        escalator = self.prepayment_inputs.escalator / 100
        today = date.today().replace(day=1)
        month = relativedelta(months=1)

        counter = 0
        terms = 1
        while counter < 240:
            first_of_month = in_service + month * counter
            month_of_year = first_of_month.month - 1
            years_pto = ((in_service + month * counter) - in_service).days // 365

            production = self.prepayment_inputs.monthly_estimates[month_of_year] * \
                         (1 - degradation) ** years_pto

            rate = self.prepayment_inputs.contract_rate * (1 + escalator) ** years_pto

            invoice = production * Decimal(rate)
            self.expected_invoice.append(round(invoice, 2))

            if first_of_month > today:
                self.pv_of_expected_invoice += present_value(invoice, monthly_discount_rate, terms)
                terms += 1

            counter += 1

    def _calculate_for_Lease(self):
        in_service = self.prepayment_inputs.in_service_date.replace(day=1)
        monthly_discount_rate = self.prepayment_inputs.discount_rate / 100 / 12
        production = self.prepayment_inputs.yearly_estimate
        escalator = self.prepayment_inputs.escalator / 100
        today = date.today().replace(day=1)
        month = relativedelta(months=1)

        counter = 0
        terms = 1
        while counter < 240:

            first_of_month = in_service + month * counter
            years_pto = ((in_service + month * counter) - in_service).days // 365

            rate = self.prepayment_inputs.contract_rate * (1 + escalator) ** years_pto

            invoice = production * Decimal(rate) / 12
            self.expected_invoice.append(round(invoice, 2))

            if first_of_month > today:
                self.pv_of_expected_invoice += present_value(invoice, monthly_discount_rate, terms)
                terms += 1

            counter += 1

    def _calculate_SREC(self):
        #todo: write SREC calculation function
        pass

    def _calculate_tax(self):
        if self.prepayment_inputs.taxable == 'Y':
            self.tax = round((self.pv_of_expected_invoice + self.pv_of_expected_SRECs) * \
                       (self.prepayment_inputs.sales_tax), 2)
        else:
            pass

    def _calculate_total(self):
        self._calculate_tax()
        self.total_prepayment_price = round(self.pv_of_expected_SRECs + self.pv_of_expected_invoice + self.tax, 2)
        self.pv_of_expected_invoice = round(self.pv_of_expected_invoice, 2)

    def _generate_beginning_year_estimates(self):
        yearly_estimates = []

        i = 0
        while i < 20:
            yearly_estimates.append(
                round(
                    net_present_value(
                    self.expected_invoice[i*12:240],
                    self.prepayment_inputs.discount_rate/100/12,
                    len(self.expected_invoice[i*12:240])
                    ),
                    2
                )
            )
            i += 1

        self.yearly_estimated_prepayment_amounts = self.unpack_yearly_prepayment._make(yearly_estimates)

    def _error_checking(self):
        #todo: write this function to check for data errors from the SQL query
        # pass
        error = False
        error_notes = None
        if not self.prepayment_inputs:
            error = True
            error_notes = self.servicenum + ' is not a valid service number.'
        elif not self.prepayment_inputs.in_service_date:
            error = True
            error_notes = 'This account has not been PTO\'d yet.'

        self.calc_error = self.error_creator(error, error_notes)

    def run(self):
        self._get_query_results()
        self._error_checking()
        if self.calc_error.error_flag:
            return
        self._calculate_cost()
        self._generate_beginning_year_estimates()

    # def prepay_calc(self, servicenum):
    #     if 'N' != prepayment_inputs['TAXABLE']:
    #         sales_tax = round(pv_of_expected_invoice * prepayment_inputs['SALES_TAX'], 2)
    #         pv_of_expected_invoice = round(pv_of_expected_invoice, 2)
    #         total_prepayment_value = pv_of_expected_invoice + sales_tax
    #     else:
    #         sales_tax = 0
    #         pv_of_expected_invoice = round(pv_of_expected_invoice, 2)
    #         total_prepayment_value = pv_of_expected_invoice + sales_tax
    #
    #     estimated_prepayment_price = []
    #
    #     estimated_prepayment_price.append(net_present_value(expected_invoice, monthly_discount_rate, len(expected_invoice)))
    #
    #     ((today.replace(day=1) + month * 13) - prepayment_inputs['IN_SERVICE_DATE'].date().replace(day=1))
    #
    #     test = (today.replace(day=1) - prepayment_inputs['IN_SERVICE_DATE'].date().replace(day=1))
    #     test1 = test.days // 365
    #     test2 = ((today.replace(day=1) + month*13) - prepayment_inputs['IN_SERVICE_DATE'].date().replace(day=1))
    #     test3 = test2.days // 365
    #
    #     return notes

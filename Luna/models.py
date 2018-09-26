import os
import re
import json
import django
import cx_Oracle
import datetime as dt
from dateutil.parser import parse
from django.db import models
from django.conf import settings

"""
Setup class with all column definitions

import class in Luna/admin.py
admin.site.register(<ClassName>) to Luna/admin.py

Then type in the following Command Prompt lines setup New Table

python manage.py makemigrations Luna
python manage.py sqlmigrate Luna 0001
python manage.py migrate
"""


class CareerPath(models.Model):
    # Department Codes
    # REAL_TIME_SCHEDULING = 'real_time_scheduling'
    CENTRAL_SCHEDULING = 'central_scheduling'
    CUSTOMER_SERVICE = 'customer_service'
    CUSTOMER_SOLUTIONS = 'customer_solutions'
    RECS_AND_REBATES = 'RECs_&_rebates'
    CUSTOMER_RELATIONS = 'customer_relations'

    # Function Codes
    INBOUND = 'inbound'
    AUXILIARY = 'auxiliary'
    SUPER_AGENT = 'super_agent'
    CUSTOMER_SOLUTIONS = 'customer_solutions'
    SERVICE = 'service'
    CUSTOMER_SOLUTIONS_ADMIN = 'customer_solutions_admin'
    TRANSFER = 'transfer'
    RESOLUTION = 'resolution'
    INBOUND_OUTBOUND = 'inbound_outbound'
    EMAIL_ADMIN = 'email_admin'
    DOCUMENTS = 'documents'

    # Position Codes
    REP_1 = 'rep_1'
    REP_2 = 'rep_2'
    REP_3 = 'rep_3'
    SPECIALIST_1 = 'specialist_1'
    SPECIALIST_2 = 'specialist_2'
    SPECIALIST_3 = 'specialist_3'
    TEAM_LEAD = 'team_lead'

    # Pay Tiers
    TIER_1_1 = 12.00
    TIER_2_1 = 13.00
    TIER_2_2 = 13.25
    TIER_2_3 = 13.75
    TIER_3_1 = 14.00
    TIER_3_2 = 14.25
    TIER_3_3 = 14.50

    DEPARTMENTS = (
        # (REAL_TIME_SCHEDULING, 'real time scheduling'),
        (CENTRAL_SCHEDULING, 'Central Scheduling'),
        (CUSTOMER_SERVICE, ''),
        (CUSTOMER_SOLUTIONS, ''),
        (RECS_AND_REBATES, ''),
        (CUSTOMER_RELATIONS, 'Customer Relations')
    )

    FUNCTIONS = (
        (INBOUND, ' - Inbound'),
        (AUXILIARY, ' - Auxiliary'),
        (SUPER_AGENT, ' - Super Agent'),
        (CUSTOMER_SOLUTIONS, 'Customer Solutions'),
        (SERVICE, ' - Service'),
        (CUSTOMER_SERVICE, 'Customer Service'),
        (TRANSFER, 'Transfer'),
        (RESOLUTION, 'Resolution'),
        (CUSTOMER_SOLUTIONS_ADMIN, 'Customer Solutions Admin'),
        (RECS_AND_REBATES, 'RECs & Rebates'),
        (INBOUND_OUTBOUND, ' - Inbound/Outbound'),
        (EMAIL_ADMIN, ' - Email Admin'),
        (DOCUMENTS, ' - Documents'),
    )

    POSITIONS = (
        (REP_1, 'Rep 1'),
        (REP_2, 'Rep 2'),
        (REP_3, 'Rep 3'),
        (SPECIALIST_1, 'Specialist 1'),
        (SPECIALIST_2, 'Specialist 2'),
        (SPECIALIST_3, 'Specialist 3'),
        (TEAM_LEAD, 'Team Lead'),
    )

    PAY_RATES = (
        (TIER_1_1, '$12.00'),
        (TIER_2_1, '$13.00'),
        (TIER_2_2, '$13.25'),
        (TIER_2_3, '$13.75'),
        (TIER_3_1, '$14.00'),
        (TIER_3_2, '$14.25'),
        (TIER_3_3, '$14.50'),
    )

    TIER_LEVELS = (
        (1.1, 'Tier 1.1'),
        (2.1, 'Tier 2.1'),
        (2.2, 'Tier 2.2'),
        (2.3, 'Tier 2.3'),
        (3.1, 'Tier 3.1'),
        (3.2, 'Tier 3.2'),
        (3.3, 'Tier 3.3'),
    )

    PERCENTAGES = (
        (0, '0%'),
        (2.5, '2.5%'),
        (3, '3%'),
        (5, '5%'),
        (7, '7%'),
        (10, '10%'),
        (20, '20%'),
        (30, '30%'),
        (40, '40%'),
        (50, '50%'),
        (60, '60%'),
        (70, '70%'),
        (75, '75%'),
        (80, '80%'),
        (85, '85%'),
        (90, '90%'),
        (100, '100%'),
    )

    tier_level = models.FloatField(
        choices=TIER_LEVELS
    )
    pay_rate = models.FloatField(
        choices=PAY_RATES
    )
    department = models.CharField(
        max_length=200,
        choices=DEPARTMENTS,
    )
    function = models.CharField(
        max_length=200,
        choices=FUNCTIONS,
        null=True,
        blank=True,
    )
    position = models.CharField(
        max_length=200,
        choices=POSITIONS
    )
    qa = models.FloatField(
        choices=PERCENTAGES,
        null=True,
        blank=True
    )
    productivity = models.FloatField(
        choices=PERCENTAGES,
        null=True,
        blank=True
    )
    aht = models.FloatField(
        null=True,
        blank=True,
    )
    aph = models.FloatField(
        null=True,
        blank=True
    )
    adh = models.FloatField(
        null=True,
        blank=True,
        choices=PERCENTAGES,
    )
    availability = models.FloatField(
        null=True,
        blank=True
    )
    error_rate = models.CharField(
        max_length=500,
        blank=True,
        null=True,
    )
    efficiency = models.FloatField(
        null=True,
        blank=True
    )
    duration = models.FloatField(
        default=90.0,
        blank=True,
        null=True,
    )
    nps = models.FloatField(
        null=True,
        blank=True
    )
    field_qa_nps_score = models.FloatField(
        null=True,
        blank=True
    )
    job_description = models.TextField()

    def position_display(self):
        return dict(CareerPath.POSITIONS)[self.position]

    def department_display(self):
        return dict(CareerPath.DEPARTMENTS)[self.department]

    def function_display(self):
        return dict(CareerPath.FUNCTIONS)[self.function]

    def pay_rate_display(self):
        return dict(CareerPath.PAY_RATES)[self.pay_rate]

    def tier_display(self):
        return dict(CareerPath.TIER_LEVELS)[self.tier_level]

    def qa_display(self):
        return dict(CareerPath.PERCENTAGES)[self.qa]

    def adh_display(self):
        return dict(CareerPath.PERCENTAGES)[self.adh]

    def availability_display(self):
        return dict(CareerPath.PERCENTAGES)[self.availability]

    def efficiency_display(self):
        return dict(CareerPath.PERCENTAGES)[self.efficiency]

    # def error_rate_display(self):
    #     return dict(CareerPath.ERROR_RATE)[self.error_rate]

    def productivity_display(self):
        return dict(CareerPath.PERCENTAGES)[self.productivity]


class AutomatorTask(models.Model):
    # TODO create AutomatorTask model once requirements are scoped out
    day = models.DateField(
        blank=True,
        null=True
    )
    hour = models.IntegerField(
        blank=True,
        null=True
    )


class Idea(models.Model):
    concept = models.TextField()
    up_votes = models.IntegerField(default=0)
    down_votes = models.IntegerField(default=0)
    submit_date = models.DateField(default=django.utils.timezone.now)


class DataWarehouse:
    """
    DataWarehouse class is used for interacting with the Vivint Solar Data Warehouse
    """

    # Unversal Character set to remove from strings and replace with a regular space
    bad_characters = [chr(9), chr(10), chr(13)]

    def __init__(self, user, connection_type='prod', encoding='utf-8'):
        """
        Initialize DataWarehouse Class
        :param user: User key to access credentials
        :param connection_type: Connect to the Production or Dev
        :param encoding: Select the Type of encoding for data coming out
                         of and into the data warehouse
        """
        # Set Submitted Parameters
        self.user = user
        self.connection_type = connection_type
        self.encoding = encoding

        # Setup all basic variables
        self.results = None
        self.column_data = None
        self.column_names = None
        self.data_for_upload = None
        self.results_with_header = None
        self.batch_errors = []
        self.failed_to_format = []

        # Used to ignore the id column when sending information to the data warehouse
        self.ignore_id_col = True

    def open_connection(self):
        """
        Open credentials file and create a new connection to the Database
        """
        connection_info = json.loads(os.environ.get('DATA_WAREHOUSE'))

        # Values retrieved from credentials file
        user = connection_info['credentials'][self.user]
        host = connection_info['connections'][self.connection_type].get('host')
        port = connection_info['connections'][self.connection_type].get('port')
        sid = connection_info['connections'][self.connection_type].get('sid')

        # Setup DNS_TNS connection info
        dns_tns = cx_Oracle.makedsn(host, port, sid)

        try:
            # Open Connection
            self.db = cx_Oracle.connect(user.get('username'), user.get('password'), dns_tns,
                                        encoding=self.encoding, nencoding=self.encoding)
        except cx_Oracle.DatabaseError as e:
            # TODO create Exception Handling
            # Log error as appropriate
            raise

        # If the database connection succeeded create the cursor for use.
        self.cursor = self.db.cursor()

    def close_connection(self):
        """
        Close Database Connection
        """
        try:
            self.cursor.close()
            self.db.close()
        except cx_Oracle.DatabaseError:
            raise

    def execute(self, sql, bindvars=None, commit=True):
        """
        Executes a SQL statement
        Example bindvars {"myField": aValue, "anotherOne": anotherValue}
        :param sql: SQL statement to Execute
        :param bindvars: Dictionary of variables passed to execute.
        :param commit: Commit to Database
        """

        self.open_connection()

        # Format SQL Statement for better results
        query = self.format_query(sql)
        try:
            # Execute Statement
            self.cursor.execute(query, bindvars)

            if commit:
                # Commit to Database
                self.db.commit()
        except cx_Oracle.DatabaseError as e:
            # TODO create Exception Handling
            # Log error as appropriate
            raise

        self.close_connection()

    def set_results_with_header(self):
        """
        Adds column_names to the top of results
        """
        self.results_with_header = self.column_names + self.results

    def update_task(self, task_id, column_name, new_value, table_name='JDLAURET.T_AUTO_TASKS'):
        query = """UPDATE {table_name}
                SET {column_name} = {new_value}
                WHERE ID = {task_id}""".format(table_name=table_name,
                                               column_name=column_name,
                                               new_value=new_value,
                                               task_id=task_id)
        self.open_connection()
        try:
            self.cursor.execute(query)
        except:
            # TODO create Exception Handling (probably as it's own function)
            pass
        self.close_connection()

    def get_columns_data(self, table_name, ignore_id_col=True):
        """
        Sets column data for the table name submitted
        :param table_name: schema.table_name to access
        :param ignore_id_col: set self.ignore_id_col value
        """
        self.ignore_id_col = ignore_id_col
        # Select Statement
        query = "SELECT * FROM {0} WHERE 1=0".format(table_name)

        self.open_connection()
        # Execute Query
        self.cursor.execute(query)
        # Retrieve Column Data and convert to list of tuples
        self.column_data = list(self.cursor.description)
        # If self.ignore_id_col is True create column names minus the 'ID' Column
        # Otherwise set all column names
        if self.ignore_id_col:
            self.column_names = [x[0] for x in self.column_data if x[0].lower() != 'id']
        else:
            self.column_names = [x[0] for x in self.column_data]

    def format_query_results(self):
        """
        Converts all LOB types to strings for easier use
        """
        for i, row in enumerate(self.results):
            for j, cell in enumerate(row):
                if isinstance(cell, cx_Oracle.LOB):
                    self.results[i][j] = str(cell)

    def query_results(self, sql, bindvars=None):
        """
        Sets self.results to the results of the SQL query
        :param sql: SQL Query to be executed
        :param bindvars: Dictionary of variables passed to execute.
        """
        self.open_connection()
        # Formats query to remove help execution
        query = self.format_query(sql)
        try:
            if bindvars is not None:
                # Prepare the Query for execution
                self.cursor.prepare(query)
                # Execute Query with bindvars
                self.cursor.execute(query, bindvars)
            else:
                # Execute Query without bindvars
                self.cursor.execute(query)
            # Set column data, column names, and results
            self.column_data = list(self.cursor.description)
            self.column_names = [x[0] for x in self.column_data]
            self.results = [list(x) for x in self.cursor.fetchall()]
            self.set_results_with_header()

        except cx_Oracle.DatabaseError as e:
            # TODO Create Exception Handling
            raise

        finally:
            self.close_connection()

    def format_query(self, sql):
        """
        Format a SQL Query to make running it with cx_Oracle a little easier
        :param sql: SQL Query to format
        :return: String of formatted SQL Query
        """
        return re.sub(' +', ' ', sql).replace(';', '')

    def get_table_data(self, table_name):
        """
        Get all data from a table
        Set self.results to list of lists containing entire table data
        :param table_name: schema.table_name
        """
        query = "SELECT * FROM {table_name}".format(table_name=table_name)
        self.query_results(query)

    def remove_characters(self, string):
        """
        Remove characters from a string
        :param string: String to be evaluated
        :return: String with removed characters
        """
        new_string = string
        for word in self.bad_characters:
            new_string.replace(word, ' ')
        return new_string

    def format_data(self):
        """
        Loop through data that is going into the Data Warehouse and format the data
        This step helps with mis-matched data types in columns
        """

        # loop through every row and column of data
        for i, row in enumerate(self.data_for_upload):

            for j, item in enumerate(row):
                # get current column type (STRING, NUMBER, DATE, etc.)
                column_type = self.column_data[j][1].__name__
                # Set all Nones to Blank string, cx_Oracle will turn this into a null value
                if item is None:
                    self.data_for_upload[i][j] = ''

                # Evaluate all non-blank cells
                if item != '':
                    # If item not a datetime type attempt to parse and create datetime object
                    if column_type == 'DATETIME' \
                            or column_type == 'TIMESTAMP':
                        if not isinstance(item, dt.datetime):
                            try:
                                self.data_for_upload[i][j] = parse(item).strftime("%Y-%m-%d %H:%M:%S")
                            except (TypeError, ValueError) as e:
                                self.failed_to_format.append([self.data_for_upload[i], e])
                        else:
                            try:
                                self.data_for_upload[i][j] = item.strftime("%Y-%m-%d %H:%M:%S")
                            except (TypeError, ValueError) as e:
                                self.failed_to_format.append([self.data_for_upload[i], e])
                    # If item not String change to string
                    if column_type == 'STRING' or \
                            column_type == 'LOB':
                        if not isinstance(item, str):
                            self.data_for_upload[i][j] = str(item)
                        self.data_for_upload[i][j] = self.remove_characters(self.data_for_upload[i][j])
                    # if item not integer convert to integer
                    if column_type == 'NUMBER':
                        self.data_for_upload[i][j] = str(item)

    def insert_data_to_table(self, table_name, data, column_map=False, ignore_id_col=True, header_included=False):
        """
        Insert data into a table
        :param table_name: schema.table to insert data into
        :param data: A list of lists to insert
        :param column_map: A list of the Columns in the order they are associated with the data
        :param ignore_id_col: If something is being inserted into the ID col set to False
        :param header_included: If the first line in the data is the header set to True
        """
        self.ignore_id_col = ignore_id_col

        self.data_for_upload = data
        self.get_columns_data(table_name)

        # Setup column map for upload
        if column_map:
            self.column_data = [x for x in self.column_data if x[0] in column_map]
            self.column_names = column_map

        self.format_data()

        # Remove header from data set
        if header_included:
            del data[0]

        # Set data size variables
        data_row_count = len(data)
        data_column_count = max(len(x) for x in data)
        print('Data Column Count:', data_column_count)
        print('Column Map Count:', len(self.column_names))

        # Check if there is more data columns than columns in the table
        if data_column_count != len(self.column_names):
            raise ValueError('Number of Columns submitted does not match Table or Column Map')

        if data_row_count > 0:
            # Rows of data found
            bind_variables = []
            # setup required variables for Insert Statement
            for i, column_name in enumerate(self.column_names):
                new_bind_name = ':' + column_name
                class_name = self.column_data[i][1].__name__
                if class_name == 'TIMESTAMP':
                    new_bind_name = 'TO_TIMESTAMP(:{0}, \'{1}\')'.format(column_name, 'yyyy-mm-dd hh24:mi:ss')
                    bind_variables.append(new_bind_name)
                elif class_name == 'DATETIME':
                    new_bind_name = 'TO_DATE(:{0}, \'{1}\')'.format(column_name, 'yyyy-mm-dd hh24:mi:ss')
                    bind_variables.append(new_bind_name)
                else:
                    bind_variables.append(new_bind_name)
            print(', '.join(bind_variables))
            # Format Insert Statement
            query = """INSERT INTO {table_name} ({column_names}) VALUES ({values})
                    """.format(table_name=table_name,
                               column_names=', '.join(self.column_names),
                               values=', '.join(bind_variables))
            self.open_connection()
            # Prepare Query and Setup Bindnames
            self.cursor.prepare(query)
            self.cursor.bindnames()

            try:
                # Execute Insert Statement
                self.cursor.executemany(None, self.data_for_upload,
                                        batcherrors=True)
                # Store Batch Errors
                self.batch_errors = self.cursor.getbatcherrors()
                number_of_errors = len(self.batch_errors)
                if number_of_errors > 0:
                    print('{0} batch errors encountered'.format(number_of_errors))
                    print('Error Preview')
                    for j in range(number_of_errors):
                        print(self.batch_errors[j].message)
                        if j > 2:
                            break
                # Commit To Data base
                self.db.commit()

            except:
                # TODO setup Exception handling
                raise

            self.close_connection()

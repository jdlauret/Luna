import os
import datetime as dt
import pytz
from django.core.exceptions import ObjectDoesNotExist
from BI.data_warehouse.connector import Snowflake
# from BI.luna_db.connector import Postgres
from Soft_Skills.models import Employee_List as elist

main_dir = os.getcwd()
soft_dir = os.path.join(main_dir, 'Soft_Skills')
utilities_dir = os.path.join(soft_dir, 'utilities')


def supervisor_list():
	DB = Snowflake()
	DB.set_user('MACK_DAMAVANDI')
	# luna = Postgres()
	# luna.set_user('POSTGRES_HOST')

	the_list = {}

	"""
	THIS PULLS A LIST OF ALL THE SUPERVISORS UNDER 2ND FLOOR MANAGER, AND FROM
	CARISSA, KELSEY, KRISTEN, TALI AND ROBERT 
	 """

	try:
		DB.open_connection()
		with open(os.path.join(utilities_dir, 'supervisor_list.sql'), 'r') as file:
			sql = file.read().split(';')
		DB.execute_query(sql[0])
		results = DB.query_results

		if len(results) == 0:
			the_list['error'] = 'List is not generating, please check is SQL is correct'
			return the_list
	except Exception as e:
		raise e
	finally:
		DB.close_connection()

	"""
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	# value[0]: SUPERVISOR BADGE ID
	# value[1]: SUPERVISOR NAME
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	"""

	now = dt.datetime.now()
	now = now.replace(tzinfo=pytz.timezone('US/Mountain'))

	# THIS SECTION PULLS A LIST OF ALL THE SUPERVISORS UNDER CHUCK AND ALLOWS THEM TO BE DISPLAYED
	for j, value in enumerate(results):
		the_list[value[0]] = value[1]

	return the_list

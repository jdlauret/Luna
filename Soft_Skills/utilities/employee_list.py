import os
import datetime as dt
import pytz
from django.core.exceptions import ObjectDoesNotExist
from BI.data_warehouse.connector import Snowflake
from BI.luna_db.connector import Postgres
from Soft_Skills.models import Employee_List as elist

main_dir = os.getcwd()
soft_dir = os.path.join(main_dir, 'Soft_Skills')
utilities_dir = os.path.join(soft_dir, 'utilities')

# TODO NEED PUT THIS INTO THE AUTOMATOR

def employee_list():
	DB = Snowflake()
	DB.set_user('MACK_DAMAVANDI')
	luna = Postgres()
	luna.set_user('POSTGRES_HOST')

	the_list = {}

	# THIS PULLS A LIST OF ALL THE EMPLOYEES UNDER CHUCK AND SPECIFIC MANAGERS
	try:
		DB.open_connection()
		with open(os.path.join(utilities_dir, 'employee_list.sql'), 'r') as file:
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

	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	# value[0]: Name
	# value[1]: badge id
	# value[2]: business title
	# value[3]: supervisor badge id
	# value[4]: supervisor name
	# value[5]: hire date
	# value[6]: Team
	# value[7]: Sub team
	# value[8]: tier
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	now = dt.datetime.now()
	now = now.replace(tzinfo=pytz.timezone('US/Mountain'))

	# CREATE NEW EMPLOYEES
	# TODO CHANGE FROM .MODELS TO BI.LUNA_DB SECTION
	# TODO UPDATE SUPERVISOR LIST IF WRONG
	for j, value in enumerate(results):
		# IF BADGE ID IS FOUND IN EMPLOYEE_LIST
		try:
			elist.objects.get(badge_id=value[1])
		# IF BADGE ID IS NOT FOUND IN EMPLOYEE_LIST
		except ObjectDoesNotExist:
			elist.objects.create(badge_id=value[1], name=value[0], business_title=value[2],
			                     supervisor_badge=value[3], supervisor_name=value[4], hire_date=value[5],
			                     team=value[6], sub_team=value[7], tier=value[8], terminated=False,
			                     created_at=now, edited_at=now.save()
			                     )
	# TERMINATED SECTION
	luna.execute_sql_command()

	return 'Added New Users'

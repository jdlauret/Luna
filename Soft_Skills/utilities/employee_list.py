import os
import datetime as dt
from BI.data_warehouse.connector import Snowflake
from Soft_Skills.models import Employee_List as elist

main_dir = os.getcwd()
soft_dir = os.path.join(main_dir, 'Soft_Skills')
utilities_dir = os.path.join(soft_dir, 'utilities')


def employee_list():
	DB = Snowflake()
	DB.set_user('MACK_DAMAVANDI')
	the_list = {}

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

	for j, value in enumerate(results):
		try:
			elist.objects.get()
			elist.objects.create(badge_id=value[1], name=value[0], business_title=value[2],
			                             supervisor_badge=value[3], supervisor_name=value[4], hire_date=value[5],
			                             team=value[6], sub_team=value[7], tier=value[8], terminated=False,
			                             created_at=dt.datetime.now(), edited_at=dt.datetime.now()).save()

	return the_list

# work on building employee list

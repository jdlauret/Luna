import os
from BI.data_warehouse.connector import Snowflake

main_dir = os.getcwd()
soft_dir = os.path.join(main_dir, 'Soft_Skills')
utilities_dir = os.path.join(soft_dir, 'utilities')

def generate_list():
	DB = Snowflake()
	DB.set_user('MACK_DAMAVANDI')

	the_list = {}

	try:
		DB.open_connection()
		with open(os.path.join(utilities_dir, 'employee_list.sql'), 'r') as file:
			sql=file.read().split(';')
		DB.execute_query(sql[0])
		results = DB.query_results[0]
		DB.execute_query(sql[1])
		results2 = DB.query_results[1]

		if len(results) == 0 or len(results2) == 0:
			the_list['error'] = 'List is not generating, please check is SQL is correct'
			return the_list
	except Exception as e:
		raise e

	finally:
		DB.close_connection()

	return 'The LIST'
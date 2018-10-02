import os
from models import SnowflakeConsole, SnowFlakeDW

main_dir = os.getcwd()
tracker_dir = os.path.join(main_dir, 'P_Tracker')
utilities_dir = os.path.join(tracker_dir, 'utilities')

DB = SnowFlakeDW()
DB.set_user('MACK_DAMAVANDI')

def auth():
	auth_list = {}

	try:
		DB.open_connection()
		DW = SnowflakeConsole(DB)
		with open(os.path.join(utilities_dir, 'auth_tracker.sql'), 'r') as file:
			sql = file.read()
		DW.execute_query(sql, bindvars=None)
		results = DW.query_results

		if len(results) == 0:
			auth_list['error'] = 'Invalid Badge ID'
			return auth_list

	except Exception as e:
		auth_list['error'] = e
		return auth_list

	finally:
		DB.close_connection()

	for j, value in enumerate(results):
		auth_list[value[0]] = value[1]
	return auth_list


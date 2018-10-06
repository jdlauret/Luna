import os
from models import SnowflakeConsole, SnowFlakeDW

main_dir = os.getcwd()
tracker_dir = os.path.join(main_dir, 'P_Tracker')
utilities_dir = os.path.join(tracker_dir, 'utilities')

DB = SnowFlakeDW()
DB.set_user('MACK_DAMAVANDI')

def tracker_list(badge):
	auth_list = {}
	#   SQL ZERO SECTION
	try:
		DB.open_connection()
		DW = SnowflakeConsole(DB)
		with open(os.path.join(utilities_dir, 'productivity_tracker.sql'), 'r') as file:
			sql = file.read()
		sql = sql.split(';')
		DW.execute_query(sql[0].format(badge=str(badge)))
		results = DW.query_results

		if len(results) == 0:
			auth_list['error'] = 'Invalid Badge ID'
			return auth_list

	except Exception as e:
		auth_list['error'] = e
		return auth_list

	#   SQL ONE SECTION
	try:
		DW.execute_query(sql[1].format(badge=str(badge)))
		results1 = DW.query_results

	except Exception as e:
		auth_list['error'] = e
		return auth_list

	#   SQL TWO SECTION
	try:
		DW.execute_query(sql[2].format(badge=str(badge)))
		results2 = DW.query_results


	except Exception as e:
		auth_list['error'] = e
		return auth_list

	finally:
		DB.close_connection()

	auth_list['badge'] = results[0][0]
	auth_list['name'] = results[0][1]
	auth_list['supervisor'] = results[0][2]
	auth_list['hrs_worked'] = round((int(results[0][3])/60), 2)
	auth_list['breaks'] = round((int(results[0][4])/60), 2)
	auth_list['activity'] = round((int(results[0][5])/60), 2)
	auth_list['training'] = round((int(results[0][6])/60), 2)
	auth_list['meeting'] = round((int(results[0][7] + results[0][8])/60), 2)
	auth_list['project'] = round((int(results[0][9])/60), 2)
	auth_list['date1'] = results1[0][0]
	auth_list['date2'] = results2[0][0]
	return auth_list


import os
from decimal import Decimal
from BI.data_warehouse.connector import Snowflake

main_dir = os.getcwd()
tracker_dir = os.path.join(main_dir, 'P_Tracker')
utilities_dir = os.path.join(tracker_dir, 'utilities')


def tracker_list(badge):
	DB = Snowflake()
	DB.set_user('MACK_DAMAVANDI')

	auth_list = {}
	badge = str(badge)

	try:
		DB.open_connection()
		with open(os.path.join(utilities_dir, 'productivity_tracker.sql'), 'r') as file:
			sql = file.read()
		# sql = sql.split(';')
		DB.execute_query(sql.format(badge=str(badge)))
						 #% {'badge': str(badge)})
		results = [Decimal(0) if x is None else x for x in DB.query_results[0]]

		if len(results) == 0:
			auth_list['error'] = 'Information not found'
			return auth_list

	except Exception as e:
		auth_list['error'] = e
		return auth_list

	finally:
		DB.close_connection()

	auth_list['badge'] = results[0]
	auth_list['name'] = results[1]
	auth_list['supervisor'] = results[2]
	auth_list['hrs_worked'] = round(results[3]/60, 2)
	auth_list['breaks'] = round(results[4]/60, 2)
	auth_list['activity'] = round(results[5]/60, 2)
	auth_list['training'] = round(results[6]/60, 2)
	auth_list['meeting'] = round(results[7] + results[8]/60, 2)
	auth_list['project'] = round(results[9]/60, 2)
	auth_list['date1'] = results[10]
	auth_list['date2'] = results[11]

	return auth_list

